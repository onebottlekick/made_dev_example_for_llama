from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the user's task, the sprint backlog and our software designs: 

User's task: {task}

Modality: {modality}

Programming Language:{language}

Sprint goals:
{current_sprint_goals}

Sprint backlog:
{current_sprint_backlog}

Sprint acceptance criteria:
{current_sprint_acceptance_criteria}

Codes:
{raw_codes}

Assets' paths:
"{workspace}"

As the {assistant_role}, to make the software directly operable without further coding, SI-follow have formulated the following regulations:
1) all referenced classes should be imported;
2) all methods should be implemented;
3) all methods need to have the necessary comments;
4) no potential bugs;
5) The entire project conforms to the tasks proposed by the user;
6) To satisfy the sprint goals, the code implements all the tasks in the sprint backlog;
7) Make sure the used assets like images must exist and be referred properly
8) Ensure that the colors used are easy on the eye
9) prohibitively put code in a try-exception in the main.py
10) most importantly, do not only check the errors in the code, but also the logic of code. \
Make sure that user can interact with generated software without losing any feature in the requirement
Now, you should check the above regulations one by one and review the codes in detail, and give me instructions on how to fix. \
If the codes are perfect and you have no comment on them, you MUST only return one line like "<INFO> Finished".
"""


ASSISTANT_ROLE_PROMPT = """
{background_prompt} You are Code Reviewer. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You can help programmers to assess source codes for software troubleshooting, fix bugs to increase code quality and robustness, \
and offer proposals to improve the source codes.
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
class CodeReviewComment(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Code Reviewer",
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
        self.states.workspace = env.config.directory
        self.states.codes = env.states.codes
        self.states.current_sprint_goals = env.states.current_sprint_goals
        self.states.current_sprint_backlog = env.states.current_sprint_backlog
        self.states.current_sprint_acceptance_criteria = env.states.current_sprint_acceptance_criteria

    def update_env_states(self, env):
        env.states.review_comments = self.seminar_conclusion
        return env
