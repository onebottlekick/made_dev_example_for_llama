from made.phase import PhaseRegistry
from made.phase.repository.base_composed_phase_repository_impl import (
    BaseComposedPhaseRepositoryImpl,
)

from states.phase_states import PhaseStates


@PhaseRegistry.register()
class Test(BaseComposedPhaseRepositoryImpl):
    def __init__(
        self,
        model_config,
        phases=[
            "TestCommands",
            "TestErrorSummary",
            "TestModification",
            "CodeFormatting",
            "TestErrorSummary",
            "TestModification",
        ],
        states=PhaseStates(),
        num_cycle=2,
    ):
        super().__init__(
            model_config=model_config, phases=phases, states=states, num_cycle=num_cycle
        )

    def update_phase_states(self, env):
        pass

    def update_env_states(self, env):
        pass

    def break_cycle(self, phase_states):
        return False
