from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the user's task, our designed product modality, languages, the sprint goals and the sprint backlog, \
our developed first-edition source codes are listed below: 

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

Comments on Codes:
{review_comments}

In the software, each file MUST strictly follow a markdown code block format:

$file_name
```$language
'''
$docstring
'''
$code
```

As the {assistant_role}, to satisfy the user's demand and the sprint goals, \
make the software creative, executive and robust, and \
ensure that the code resolves the sprint backlog, you should modify corresponding codes according to the comments. \
Then, output the full and complete codes with all bugs fixed based on the comments. Return full codes strictly following the required format.
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
{background_prompt} You are Code Reviewer. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You can help programmers to assess source codes for software troubleshooting, fix bugs to increase code quality and robustness, \
and offer proposals to improve the source codes.
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class CodeReviewModification(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Programmer",
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
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality
        self.states.language = env.states.language
        self.states.raw_codes = env.states.raw_codes
        self.states.current_sprint_goals = "\n".join(env.states.all_sprint_goals[-1])
        self.states.current_sprint_backlog = "\n".join(env.states.all_sprint_backlog[-1])
        self.states.current_sprint_acceptance_criteria = "\n".join(env.states.all_sprint_acceptance_criteria[-1])
        self.states.review_comments = env.states.review_comments[-1]

    def update_env_states(self, env):
        env.states.raw_codes = self.seminar_conclusion
        return env
