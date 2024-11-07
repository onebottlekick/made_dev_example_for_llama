import os

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the new user's task and our software designs listed below:

User's task: {task}

Modality: {modality}

Programming Language: {language}

Sprint goals:
{current_sprint_goals}

Sprint backlog:
{current_sprint_backlog}

Sprint Acceptance Criteria:
{current_sprint_acceptance_criteria}

To satisfy the sprint goals, we have decided to complete the sprint backlog through a executable software with multiple files implemented via {language}. \
As the {assistant_role}, to satisfy the user's demands and the sprint goals, you should accomplish the sprint backlog \
by writing one or multiple files and make sure that every detail of the architecture is, in the end, implemented as code. {gui} \
Think step by step and reason yourself to the right decisions to make sure we get it right. \
You will first lay out the names of the core classes, functions, methods that will be necessary, as well as a quick comment on their purpose.
Then you will output the content of each file including complete code. \
Each file MUST strictly follow a markdown code block format:

$file_name
```$language
'''
$docstring
'''
$code
```

You will start with the "main" file, then go to the ones that are imported by that file, and so on.
Please note that the code should be fully functional. Ensure to implement all functions. No placeholders (such as 'pass' in Python).
You SHOULD NOT response other texts but the code.
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
{background_prompt} You are Product Owner. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You are responsible for all product-related matters in SI-follow. \
Usually includes product design, product strategy, product vision, product innovation, project management and product marketing.
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class Coding(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Programmer",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Product Owner",
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
        gui = (
            ""
            if not env.config.gui_design
            else "The software should be equipped with graphical user interface (GUI) so that user can visually and graphically use it; so you must choose a GUI framework (e.g., in Python, you can implement GUI via tkinter, Pygame, Flexx, PyGUI, etc,)."
        )
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality
        self.states.language = env.states.language
        self.states.current_sprint_goals = "\n".join(env.states.all_sprint_goals[-1])
        self.states.current_sprint_backlog = "\n".join(env.states.all_sprint_backlog[-1])
        self.states.current_sprint_acceptance_criteria = "\n".join(env.states.all_sprint_acceptance_criteria[-1])
        self.states.gui = gui

    def update_env_states(self, env):
        env.states.raw_codes = self.seminar_conclusion
        return env
