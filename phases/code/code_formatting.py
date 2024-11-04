import os

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the code, required code format and comments below:

Codes:
"{raw_codes}"

Required Code Format:
$file_name
```$language
'''
$docstring
'''
$code
```
Comments:

The code above contains enough values for the required fields: "$file_name", "$language", "$docstring" and  "$code". \
If codes are formatted unproperly, you should rearrange them to satisfy the requirement.
As the {assistant_role}, to make the code satisfy the required format, if you should modify corresponding codes according to the comments \
and then return all codes strictly following the required format. \
You SHOULD NOT to write new code or change the values of any fields, \
meaning that the new code is only different from the original code in terms of the format.
You MUST response all codes even if codes are not modified and SHOULD NOT response any other texts.
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
{background_prompt} You are Code Reviewer. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You can help programmers to assess source codes for software troubleshooting, fix bugs to increase code quality and robustness, \
and offer proposals to improve the source codes.
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class CodeFormatting(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Development Team",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Code Reviewer",
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
        self.states.raw_codes = env.states.raw_codes

    def update_env_states(self, env):
        contents = FileToolRepositoryImpl.abstract_contents_from_text(
            self.seminar_conclusion, regex=r"(.+?)\n```.*?\n(.*?)```"
        )
        for k, v in contents.items():
            env.states.codes[k] = v
            FileToolRepositoryImpl.write_file(os.path.join(env.config.directory, k), v)
        return env
