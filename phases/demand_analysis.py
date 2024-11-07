from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
SI-follow has made many products before. To satisfy customer's demand and the product should be realizable, \
we MUST keep discussing with each other to decide which product modality to be.
Note that we SHOULD ONLY discuss the product modality and do not discuss anything else! \
Once we all have expressed our opinion(s) and agree with the results of the discussion unanimously, \
any of us must actively terminate the discussion by replying with only one line, \
which starts with a single word <INFO>, followed by our final product modality without any other words, e.g.,"<INFO> Application".
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
class DemandAnalysis(BasePhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phase_prompt=PHASE_PROMPT,
        assistant_role_name="Product Owner",
        assistant_role_prompt=ASSISTANT_ROLE_PROMPT,
        user_role_name="Customer",
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
        pass

    def update_env_states(self, env):
        env.states.modality = self.seminar_conclusion
        return env
