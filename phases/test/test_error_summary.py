import os
import signal
import subprocess
import time

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.docker.repository.docker_tool_repository_impl import (
    DockerToolRepositoryImpl,
)

from states.phase_states import PhaseStates


PHASE_PROMPT = """
Our developed source codes and corresponding test reports are listed below:

Programming Language: {language}

Source Codes:
{raw_codes}

Test Reports of Source Codes:
{test_reports}

According to my test reports, please locate and summarize the bugs that cause the problem.
"""


ASSISTANT_ROLE_PROMPT = """
{background_prompt} You are Programmer. we are both working at SI-follow. We share a common interest in collaborating to \
successfully complete a task assigned by a new customer.
You can write/create computer software or applications by providing a specific programming language to the computer. \
You have extensive computing and coding experience in many varieties of programming languages and platforms, such as Python, Java, C, C++, HTML, CSS, JavaScript, XML, SQL, PHP, etc,.
Here is a new customer's task: {task}.
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


USER_ROLE_PROMPT = """
{background_prompt} You are Software Test Engineer. we are both working at SI-follow. We share a common interest in collaborating \
to successfully complete a task assigned by a new customer. \
You can use the software as intended to analyze its functional properties, \
design manual and automated test procedures to evaluate each software product, \
build and implement software evaluation test programs, and run test programs to ensure that testing protocols evaluate the software correctly.
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class TestErrorSummary(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Programmer",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Software Test Engineer",
        user_role_prompt=USER_ROLE_PROMPT,
        chat_turn_limit=1,
        conversation_rag=False,
        temperature=0.2,
        top_p=1.0,
        states=PhaseStates(),
        **kwargs,
    ):
        super().__init__(
            model_config=model_config,
            phase_prompt=phase_prompt,
            assistant_role_name=assistant_role_name,
            assistant_role_prompt=assistant_role_prompt,
            user_role_name=user_role_name,
            user_role_prompt=user_role_prompt,
            chat_turn_limit=chat_turn_limit,
            conversation_rag=conversation_rag,
            temperature=temperature,
            top_p=top_p,
            **kwargs,
        )

    def update_phase_states(self, env):
        # container = DockerToolRepositoryImpl.get_container("si_follow_test")
        # output, exit_code = DockerToolRepositoryImpl.exec_command(
        #     container,
        #     f"bash -c export PYTHONPATH={env.config.directory} && export DISPLAY=:0.0 && python {env.config.directory}/main.py",
        # )
        process = subprocess.Popen(
            f"cd {env.config.directory}; python main.py",
            shell=True,
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(3)
        exit_code = process.returncode
        if process.poll() is None:
            if "killpg" in dir(os):
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            else:
                os.kill(process.pid, signal.SIGTERM)
                if process.poll() is None:
                    os.kill(process.pid, signal.CTRL_BREAK_EVENT)
        output = process.stderr.read().decode("utf-8")
        if exit_code != 0 and "Traceback" in output:
            self.states.test_reports = output
            if self.conversation_logging:
                from made.utils.logger import Logger

                error_logger = Logger(
                    f"{self.__class__.__name__}_{env.config.directory}",
                    f'{os.path.join(env.config.directory, "logs", "test_error.log")}',
                ).get_logger()
                error_logger.info(output)
        else:
            self.states.test_reports = "No bugs"
        self.states.language = env.states.language
        self.states.raw_codes = env.states.raw_codes

    def update_env_states(self, env):
        env.states.error_summary.append(self.seminar_conclusion)
        env.states.test_reports.append(self.states.test_reports)
        return env
