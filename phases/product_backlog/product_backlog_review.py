from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the new user's task and our software designs listed below: 

Task: {task}

Modality: {modality}

Programming Language: {language}

We have decided to complete the task through a executable software with multiple files implemented via {language}. \
As the {assistant_role}, to satisfy the user's demands, I suggest the following product backlog and acceptance criteria:

Product backlog:
{product_backlog}

Backlog Acceptance Criteria:
{product_acceptance_criteria}

As the development team, you should review and provide useful feedback about tasks to make the software run flawlessly by obeying the regulations below
1) considering the proficiency of the members, all the tasks are feasible and finished by at least one member
2) the product backlog SHOULD NOT incorporate enhanced features like AI, animations and sound effects unless explicitly specified in the user's task.
Now, you MUST check the above regulations one by one and review the product backlog in detail, \
propose one comment with the highest priority about the product backlog, and give me instructions on how to fix. \
Tell me your comment with the highest priority and corresponding suggestions on revision. \
If the product backlog is perfect and you have no comment on them, return only one line like \"<INFO> Finished\"
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
Here is a new customer's task: {task}.
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class ProductBacklogReview(BasePhaseRepositoryImpl):
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
        self.states.product_backlog = "\n".join(env.states.product_backlog)
        self.states.product_acceptance_criteria = "\n".join(env.states.product_acceptance_criteria)

    def update_env_states(self, env):
        env.states.product_backlog_comments = self.seminar_conclusion
        return env
