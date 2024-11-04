from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the user's task, our software designs, the sprint goals, the sprint backlog, the acceptance criteria, \
our developed source code, and corresponding test reports and summaries are listed below: 

Task: {task}

Modality: {modality}

Programming Language: {language}

Sprint goals:
{current_sprint_goals}

Sprint backlog:
{current_sprint_backlog}

Sprint acceptance criteria:
{current_sprint_acceptance_criteria}

Source Codes:
{raw_codes}

Test Reports of Source Codes:
{test_reports}

Error Summary of Test Reports:
{error_summary}

To satisfy the sprint goals, we have decided to complete the sprint backlog. As the {assistant_role}, \
you implemented source code and tested source code, then you wrote test reports and error summaries. \
Now is at the end of the sprint, you should review all the work, what has been done, what has not. \
You MUST answer according to the following format:

Done Work:
$done_work
Undone Work:
$undone_work

where $done_work are carefully completed and tested works, $undone_work includes unfinished works or existing bugs.
You MUST put response in format above, done work and undone_work should be numbered list.
You SHOULD NOT include any other texts.
"""


ASSISTANT_ROLE_PROMPT = """
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
{background_prompt} You are Product Owner. we are both working at SI-follow. \
We share a common interest in collaborating to successfully complete a task assigned by a new customer. \
You are responsible for all product-related matters in SI-follow. \
Usually includes product design, product strategy, product vision, product innovation, project management and product marketing.
Here is a new customer's task: {task}.
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
{task}
"""


USER_ROLE_PROMPT = """
{background_prompt} You are a development team of 3 members, including a programmer, a software test engineer, and a code reviewer. \
All work at the SI-follow where the people are using Agile Scrum for managing software development. \
You are a team with diverse skills from programming to testing and reviewing where each member has a certain set of skills and supports other members.
For example, the programmer is strong on programming and implementing functions, \
the software test engineer is good at testing and fixing source code written by the programmer.
You are responsible for completing all sprints by finishing all sprint backlogs correctly, thereby accomplishing the product backlog.
Here is a new customer's task:
"""


@PhaseRegistry.register()
class SprintReview(BasePhaseRepositoryImpl):
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
        self.states.raw_codes = env.states.raw_codes
        self.states.current_sprint_goals = "\n".join(env.states.current_sprint_goals)
        self.states.current_sprint_backlog = "\n".join(env.states.current_sprint_backlog)
        self.states.current_sprint_acceptance_criteria = "\n".join(env.states.current_sprint_acceptance_criteria)
        self.states.raw_codes = env.states.raw_codes
        self.states.test_reports = env.states.test_reports
        self.states.error_summary = env.states.error_summary

    def update_env_states(self, env):
        done_works = self.seminar_conclusion.split("Done Work:")[-1].split("Undone Work:")[0].split("\n")
        env.states.done_works = [done_work for done_work in done_works if done_works]
        undone_works = self.seminar_conclusion.split("Undone Work:")[-1].split("\n")
        env.states.undone_works = [undone_work for undone_work in undone_works if undone_work]
        print('#'*40)
        print(self.seminar_conclusion)
        print('#'*40)
        return env
