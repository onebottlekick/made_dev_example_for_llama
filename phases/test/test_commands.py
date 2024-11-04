import re

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the user's task, our designed product modality, the sprint goals and the sprint backlog, \
our developed first-edition source codes are listed below: ",

User's task: {task}

Modality: {modality}

Programming Language: {language}

Sprint goals:
{current_sprint_goals}

Sprint backlog:
{current_sprint_backlog}

Sprint acceptance criteria:
{current_sprint_acceptance_criteria}

Codes:
{raw_codes}

As the {assistant_role}, to make that the code above satisfies the sprint goals and backlog and runs flawlessly, \
you MUST write commands to start the UI of the software and test the correctness of the code above. \
Also, you MUST strictly follow the format:

Commands:
$commands

Here, $commands are necessary commands for starting the software and testing the code above.
You SHOULD NOT response any other texts except for commands in format.
"""


ASSISTANT_ROLE_PROMPT = """
{background_prompt} You are Software Test Engineer. we are both working at SI-follow. We share a common interest in collaborating \
to successfully complete a task assigned by a new customer. \
You can use the software as intended to analyze its functional properties, \
design manual and automated test procedures to evaluate each software product, \
build and implement software evaluation test programs, and run test programs to ensure that testing protocols evaluate the software correctly.
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


USER_ROLE_PROMPT = """
{background_prompt} You are Programmer. we are both working at SI-follow. We share a common interest in collaborating to \
successfully complete a task assigned by a new customer.
You can write/create computer software or applications by providing a specific programming language to the computer. \
You have extensive computing and coding experience in many varieties of programming languages and platforms, such as Python, Java, C, C++, HTML, CSS, JavaScript, XML, SQL, PHP, etc,.
Here is a new customer's task: {task}.
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class TestCommands(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Software Test Engineer",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Programmer",
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
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality
        self.states.language = env.states.language
        self.states.raw_codes = env.states.raw_codes
        self.states.current_sprint_goals = env.states.current_sprint_goals
        self.states.current_sprint_backlog = env.states.current_sprint_backlog
        self.states.current_sprint_acceptance_criteria = env.states.current_sprint_acceptance_criteria

    def update_env_states(self, env):
        commands = re.findall(r"python (.*?\.py)", self.seminar_conclusion)
        print("#"*30)
        print(commands)
        print("#"*30)
        env.states.commands = commands
        return env
