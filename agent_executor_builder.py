from langchain.base_language import BaseLanguageModel

from sandbox.agent import (
    AgentExecutorWithToolkit,
    ZeroShotAgentWithToolkit,
)

from sandbox.tool import get_toolkits_by_names

def built_multi_agent_executor(
        toolkits: List[str],
        agent_llm: BaseLanguageModel,
        simulator_llm: BaseLanguageModel,
) -> Type[AgentExecutorWithToolkit]:
    toolkits = get_toolkits_by_names(toolkits)
    agent = ZeroShotAgentWithToolkit.from_llm_and_toolkits(
        toolkits=toolkits,
        llm=agent_llm,
    )