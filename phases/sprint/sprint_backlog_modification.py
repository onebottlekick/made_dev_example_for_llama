import re

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the new user's task and our software designs listed below: 

Task: {task}

Modality: {modality}

Programming Language: {language}

Product backlog:
{product_backlog}

Product Acceptance Criteria:
{product_acceptance_criteria}

We have decided to incorporate Agile Scrum with multiple sprints to complete the task \
through a executable software with multiple files implemented via {language}. As the {user_role}, to satisfy the user's demands, \
I suggest the following sprint goals and sprint backlog:

Sprint goals:
{current_sprint_goals}

Sprint backlog:
{current_sprint_backlog}

Sprint acceptance criteria:
{current_sprint_acceptance_criteria}

As the {assistant_role}, you should review and provide useful feedback about sprint goals and sprint backlog \
to make the software run flawlessly by obeying the regulations below
1) considering the proficiency of the members, all the tasks are feasible and finished by at least one member,
2) the sprint backlog must not incorporate enhanced features like AI and sound effects unless explicitly specified in the user's task,
3) all the items in sprint backlog are from the product backlog.
Now, you should check the above regulations one by one and review the sprint goals and sprint backlog in detail, \
propose one comment with the highest priority about them, and \
give me instructions on how to fix to ensure the sprint backlog aligns well with the regulations above. \
You should modify corresponding product backlog according to the comments.
You MUST reponse in format below:

**Sprint Backlog:**
$sprint_backlog
**Acceptance Criteria:**
$acceptance_criteria

You SHOULD ONLY answer sprint backlog, sprint acceptance criteria in numbered list.
If the sprint goals and sprint backlog are perfect and you have no comment on them, SHOULD ONLY return one line like "<INFO> Finished".
"""


ASSISTANT_ROLE_PROMPT = """
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
{background_prompt} You are Product Owner. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You are responsible for all product-related matters in SI-follow. \
Usually includes product design, product strategy, product vision, product innovation, project management and product marketing.
Here is a new customer's task: {task}.
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


USER_ROLE_PROMPT = """
{background_prompt} You are a development team of 3 members, including a programmer, a software test engineer, and a code reviewer. \
All work at the SI-follow where the people are using Agile Scrum for managing software development. \
You are a team with diverse skills from programming to testing and reviewing where each member has a certain set of skills and supports other members.
For example, the programmer is strong on programming and implementing functions, \
the software test engineer is good at testing and fixing source code written by the programmer.
You are responsible for completing all sprints by finishing all sprint backlogs correctly, thereby accomplishing the product backlog.
Here is a new customer's task:
{task}
"""


@PhaseRegistry.register()
class SprintBacklogModification(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Product Owner",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Development Team",
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
        self.states.plain_product_backlog = "\n".join(env.states.product_backlog)
        self.states.product_acceptance_criteria = "\n".join(env.states.product_acceptance_criteria)
        self.states.product_backlog_comments = env.states.product_backlog_comments
        self.states.current_sprint_acceptance_criteria = "\n".join(env.states.current_sprint_acceptance_criteria)
        self.states.current_sprint_goals = "\n".join(env.states.current_sprint_goals)
        self.states.current_sprint_backlog = "\n".join(env.states.current_sprint_backlog)

    def update_env_states(self, env):
        print(self.seminar_conclusion)
        return env
