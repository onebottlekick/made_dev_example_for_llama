from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.docker.repository.docker_tool_repository_impl import (
    DockerToolRepositoryImpl,
)
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
Our developed source codes and corresponding test reports are listed below: 

Programming Language: {language}

Source Codes:
{raw_codes}

Test Reports of Source Codes:
{test_reports}

Error Summary of Test Reports:
{error_summary}

As the {assistant_role}, to satisfy the new user's demand and make the software execute smoothly and robustly, \
you MUST modify the codes based on the error summary.
Now, use the format exemplified above and modify the problematic codes based on the error summary. \
If you cannot find the assets from the existing paths, you should consider remove relevant code and features. \
Fix the codes and Output all the codes that you fixed or not, based on the test reported and corresponding explanations. \
You MUST follow the format defined below, including $file_name, $language, $doc_string and $code
You SHOULD NOT response incomplete TODO codes.

$fie_name
```$language
'''
$doc_string
'''
$code
```

You MUST response all the codes put in format above.
You SHOULD NOT contain any other text execpt for code.
If no bugs are reported, please return only one line like "<INFO> Finished".
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
class TestModification(BasePhaseRepositoryImpl):
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
        self.states.language = env.states.language
        self.states.raw_codes = env.states.raw_codes
        self.states.test_reports = env.states.test_reports[-1]
        self.states.error_summary = env.states.error_summary[-1]

    def update_env_states(self, env):
        modified_code = self.seminar_conclusion
        if "Finished" in modified_code:
            return env
        env.states.raw_codes = modified_code
        return env
