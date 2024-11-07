import os

from made.phase import PhaseRegistry
from made.phase.repository.base_phase_repository_impl import BasePhaseRepositoryImpl
from made.tools.file.repository.file_tool_repository_impl import FileToolRepositoryImpl

from states.phase_states import PhaseStates


PHASE_PROMPT = """
The new user's task, our developed codes and required dependencies are listed:

Task: {task}

Modality: {modality}

Programming Language: {language}

Codes: 
{raw_codes}

Requirements:
{requirements}

As the {assistant_role}, by using Markdown, you should write a manual.md file which is a detailed user manual to use the software, \
including introducing main functions of the software, how to install environment dependencies and how to use/play it. For example:

# LangChain
Building applications with LLMs through composability
Looking for the JS/TS version? Check out LangChain.js.
**Production Support:** As you move your LangChains into production, we'd love to offer more comprehensive support.
Please fill out this form and we'll set up a dedicated support Slack channel.
## Quick Install
`pip install langchain`
or
`conda install langchain -c conda-forge`
## 🤔 What is this?
Large language models (LLMs) are emerging as a transformative technology, enabling developers to build applications \
that they previously could not. However, using these LLMs in isolation is often insufficient \
for creating a truly powerful app - the real power comes when you can combine them with other sources of computation or knowledge.
This library aims to assist in the development of those types of applications. Common examples of these applications include:
**❓ Question Answering over specific documents**
- Documentation
- End-to-end Example: Question Answering over Notion Database
**🤖 Agents**
- Documentation
- End-to-end Example: GPT+WolframAlpha
## 📖 Documentation
Please see [here](https://python.langchain.com) for full documentation on:
- Getting started (installation, setting up the environment, simple examples)
- How-To examples (demos, integrations, helper functions)
- Reference (full API docs)
- Resources (high-level explanation of core concepts)

You SHOULD NOT include any other texts in response except for contents of manual.
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
Here is a new customer's task: {task}
To complete the task, you must write a response that appropriately solves the requested instruction based on your expertise and customer's needs.
"""


@PhaseRegistry.register()
class Manual(BasePhaseRepositoryImpl):
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
        self.states.task = env.config.task_prompt
        self.states.modality = env.states.modality
        self.states.language = env.states.language
        self.states.raw_codes = env.states.raw_codes
        self.states.requirements = "\n".join(env.states.requirements)

    def update_env_states(self, env):
        manual = self.seminar_conclusion
        FileToolRepositoryImpl.write_file(os.path.join(env.config.directory, "README.md"), manual)
        env.states.manual = manual
        env.states.codes["README.md"] = env.states.manual
        return env
