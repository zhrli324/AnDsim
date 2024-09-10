from agent import Agent
from tool import Tool
from pre_info import AgentInfo

back_info = """
test_back_info
"""

class Simulator:
    """
    模拟器，用来管理调用整个multi-agent系统
    """
    def __init__(
            self,
            num_agents: int,
            agents_mode: str='preset',
            subject: str='normal',
    ) -> None:
        """
        初始化系统设置
        :param num_agents: 系统中agent的数量
        :param agents_mode: 系统中agent的排列方法
        :param subject: 系统的聊天主题
        """
        self.num_agents = num_agents
        self.agents_mode = agents_mode
        self.subject = subject
        self.agents = []
        self.tools = []

    def _init_tools(
            self,
    ) -> None:
        """
        初始化agent能使用的工具列表
        :return:
        """
        pass

    def _init_agents(
            self,
    ) -> None:
        """
        初始化所有agent
        :return:
        """
        if self.agents_mode == 'preset' and self.subject == 'normal':
            for i in range(self.num_agents):
                info = AgentInfo()
                agent = Agent(name=f"Agent_{i}", model='got-4o-mini', tools=self.tools, background=info)
                self.agents.append(agent)

    def _init_neighbors(
            self,
    ) -> None:
        """
        初始化所有agent的邻居agent(可以直接对话)
        """
        pass

    def initialize(
            self,
    ) -> None:
        """
        将整个模拟器初始化
        :return:
        """
        self._init_tools()
        self._init_agents()
        self._init_neighbors()

    def emulate(
            self,
    ) -> None:
        """
        启动模拟
        :return:
        """
        pass
