import os

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
The new user's task and our developed codes are listed:

Task: {task}

Modality: {modality}

Programming Language: {language}

Codes: 
{raw_codes}

As the {assistant_role}, you should write a requirements.txt file, which is commonly used in Python projects \
to specify the dependencies or packages required for the project to run properly. \
It serves as a way to document and manage the project's dependencies in a standardized format. For example:

numpy==1.23.0
pytorch==2.1.0

According to the codes and file format listed above, write a requirements.txt file to specify the dependencies or packages required for the project to run properly.
You MUST put response in the format above.
You SHOULD NOT include any other texts in response except for requirements.
If no packages are needed, just response <INFO>None
"""


ASSISTANT_ROLE_PROMPT = """
{background_prompt} You are a development team of 3 members, including a programmer, a software test engineer, and a code reviewer. \
All work at the SI-follow where the people are using Agile Scrum for managing software development. \
You are a team with diverse skills from programming to testing and reviewing where each member has a certain set of skills and supports other members.
For example, the programmer is strong on programming and implementing functions, \
the software test engineer is good at testing and fixing source code written by the programmer.
You are responsible for completing all sprints by finishing all sprint backlogs correctly, thereby accomplishing the product backlog.
Here is a new customer's task:
{task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


USER_ROLE_PROMPT = """
{background_prompt} You are Product Owner. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You are responsible for all product-related matters in SI-follow. \
Usually includes product design, product strategy, product vision, product innovation, project management and product marketing.
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class EnvironmentDoc(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Development Team",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Product Owner",
        user_role_prompt=USER_ROLE_PROMPT,
        chat_turn_limit=1,
        conversation_rag=False,
        temperature=0.5,
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

    def update_env_states(self, env):
        requirements = self.seminar_conclusion
        if "None" not in requirements:
            FileToolRepositoryImpl.write_file(os.path.join(env.config.directory, "requirements.txt"), requirements)
            env.states.requirements = requirements.split("\n")
            env.states.codes["reqirements.txt"] = env.states.requirements
        return env
