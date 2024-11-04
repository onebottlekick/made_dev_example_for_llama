from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the user's task, our software designs, product backlog listed below: 

Task: {task}

Modality: {modality}

Programming Language: {language}

Product backlog:
{product_backlog}

Product acceptance criteria:
{product_acceptance_criteria}

We have decided to complete the task through a executable software with multiple files implemented via {language}. \
We are using Agile Scrum for software development. We finished some sprints with done tasks and undone tasks as below:

Done tasks: 
{done_works}

Undone tasks:
{undone_works}

As the {assistant_role}, to satisfy the user's demands, you must create the a next sprint backlog, acceptance criteria and the goals of this sprint \
from the product backlog, done tasks and undone tasks. \
You MUST meticulously consider undone tasks when creating the next sprint. Think step by step and reason yourself to the right decisions to make sure we get it right.
Importantly, when done tasks are exactly the product backlog, just return a single line with the content: "<INFO> DONE." and do nothing.
You must create a next sprint backlog and MUST strictly obeys the following format:

Sprint Goals:
$sprint_goals
Sprint Backlog:
$sprint_backlog
Sprint acceptance Criteria:
$sprint_acceptance_criteria

where $sprint_goals are the goals of the sprint, and $sprint_backlog is the sprint backlog whose items are from the product backlog, \
$sprint_acceptance_criteria is the sprint acceptance criteria that satisfy sprint backlog, meaning that you SHOULD NOT devise new tasks or non-practical features.
You must ensure that $sprint_goals and $sprint_backlog, $sprint_acceptance_criteria SHOULD NOT be empty and \
$sprint_acceptance_criteria aligns with $sprint_backlog and $sprint_backlog aligns with $sprint_goals.
As the Product Owner, you MUST adhere to the following regulations:
1) considering the proficiency of the members, all the tasks are feasible and finished by at least one member,
2) the sprint backlog SHOULD NOT include enhanced features like AI, animations and sound effects,
3) the sprint backlog chosen sets the stage for next sprints.
Note that the product backlog is divided into multiple sprints and each sprint should contain enough workload.
"""


ASSISTANT_ROLE_PROMPT = """
{background_prompt} You are Product Owner. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You are responsible for all product-related matters in SI-follow. \
Usually includes product design, product strategy, product vision, product innovation, project management and product marketing.
Here is a new customer's task: {task}
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
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class NextSprintBacklogCreate(BasePhaseRepositoryImpl):
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
        self.states.product_backlog = "\n".join(env.states.product_backlog)
        self.states.product_acceptance_criteria = "\n".join(env.states.product_acceptance_criteria)
        self.states.done_works = "\n".join(env.states.done_works)
        self.states.undone_works = "\n".join(env.states.undone_works)

    def update_env_states(self, env):
        sprint_results = self.seminar_conclusion
        sprint_results = sprint_results.split("###")
        for sprint_result in sprint_results:
            sprint_goals_text = (
                sprint_result.split("**Sprint Goals:**")[1]
                .split("**Sprint Backlog:**")[0]
                .strip()
            )
            sprint_backlog_text = (
                sprint_result.split("**Sprint Backlog:**")[1]
                .split("**Sprint Acceptance Criteria:**")[0]
                .strip()
            )
            sprint_acceptance_criteria_text = sprint_result.split(
                "**Sprint Acceptance Criteria:**"
            )[1].strip()
            sprint_goals = [
                item.strip() for item in sprint_goals_text.split("\n") if item.strip()
            ]
            sprint_backlog = [
                item.strip() for item in sprint_backlog_text.split("\n") if item.strip()
            ]
            sprint_acceptance_criteria = [
                item.strip()
                for item in sprint_acceptance_criteria_text.split("\n")
                if item.strip()
            ]

        env.states.all_sprint_goals.append(sprint_goals)
        env.states.current_sprint_goals = sprint_goals

        env.states.all_sprint_backlog.append(sprint_backlog)
        env.states.current_sprint_backlog = sprint_backlog

        env.states.all_sprint_acceptance_criteria.append(sprint_acceptance_criteria)
        env.states.current_sprint_acceptance_criteria = sprint_acceptance_criteria

        env.states.num_sprints += 1

        return env
