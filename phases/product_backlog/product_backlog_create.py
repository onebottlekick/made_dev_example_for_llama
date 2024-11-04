from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
According to the new user's task and our software designs listed below:

Task: {task}

Modality: {modality}

Programming Language: {language}

We have decided to complete the task through a executable software with multiple files implemented via {language}. \
As the {assistant_role}, to satisfy the user's demands, you must write the Product Backlog and the corresponding Acceptance Criteria. \
Think step by step and reason yourself to the right decisions to make sure we get it right. \
You must also prioritize product backlog items with the important items appearing at the first. \
Your answer must adhere to the following format:

Product Backlog:
$PRODUCT_BACKLOG
Acceptance Criteria:
$ACCEPTANCE_CRITERIA

where $PRODUCT_BACKLOG is the product backlog for the user's task and \
$ACCEPTANCE_CRITERIA is the corresponding acceptance criteria of the product backlog.
Importantly, you must consider the skills of the development team to write the feasible product backlog. \
Advanced features like AI and sounds can not be implemented properly.
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
You are a customer. You employ SI-follow, a software development company, to develop a product based on the following task description:
{task}.
You also require SI-follow to obey the following requirements:
1. The proposed features can be implementable,
2. The product successfully runs without any errors,
3. The product is be designed for ease of use,
4. The product has a full of manual and relevant documentation.
To achieve your goal, you must write a response based on your needs.
"""


@PhaseRegistry.register()
class ProductBacklogCreate(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Product Owner",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Custormer",
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

    def update_env_states(self, env):
        product_backlog = self.seminar_conclusion
        from made.role_playing.service.role_playing_service_impl import (
            RolePlayingServiceImpl,
        )
        from made.messages.entity.chat_message.user_message import UserChatMessage

        summary_assistant = RolePlayingServiceImpl(
            self.model_config,
            task_prompt="",
            assistant_role_name="assistant",
            assistant_role_prompt="You are a helpful assistant",
            user_role_name="user",
            user_role_prompt="",
        )

        result = summary_assistant.step(
            UserChatMessage(
                content=f"text: {product_backlog}\nfrom text above ONLY answer backlog, acceptance criteria in numbered list. \
            You SHOULD NOT contain any other text in response. You MUST answer in format:\n**Product Backlog:**\n$product_backlogs\n**Acceptance Criteria:**\n$acceptance_criteria"
            ),
            assistant_only=True,
        )[0].message.content
        product_backlog_text = (
            result.split("**Product Backlog:**")[1]
            .split("**Acceptance Criteria:**")[0]
            .strip()
        )
        acceptance_criteria_text = result.split("**Acceptance Criteria:**")[1].strip()

        product_backlog = [
            item.strip() for item in product_backlog_text.split("\n") if item.strip()
        ]

        acceptance_criteria = [
            item.strip()
            for item in acceptance_criteria_text.split("\n")
            if item.strip()
        ]
        env.states.product_backlog = product_backlog
        env.states.product_acceptance_criteria = acceptance_criteria
        return env
