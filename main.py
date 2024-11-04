from made.chat_chain.service.chat_chain_service_impl import ChatChainServiceImpl
from made.phase import import_all_modules

from states.env_states import EnvStates


import_all_modules("phases")


if __name__ == "__main__":
    chain = ChatChainServiceImpl(
        task_prompt="Develop tetris game using pygame",
        directory="project_zoo/tetris",
        base_url="https://si-follow.loca.lt/v1/",
        model="llama3.1",
        phases=[
            "DemandAnalysis",
            "ProductBacklogUpdate",
            "SprintCompletion",
            "CodeAndFormat",
            "CodeReview",
            "Test",
            "SprintReview",
            "NextSprintCompletion",
            "IncrementalCodeAndFormat",
            "CodeReview",
            "Test",
            "SprintReview",
            "EnvironmentDoc",
            "Manual",
        ],
        env_states=EnvStates(),
        save_chain=True,
        git_management=True,
    )
    chain.run()
