from sandbox.agent import Agent, EntranceAgent
from sandbox.pre_info import AgentInfo
import random


class Simulator:
    """
    模拟器，用来管理调用整个multi-agent系统
    """

    def __init__(
            self,
            num_agents: int,
            agents_mode: str = 'preset',
            theme: str = 'normal',
            use_rag: bool = True,
    ) -> None:
        """
        初始化系统设置
        :param num_agents: 系统中agent的数量
        :param agents_mode: 系统中agent的排列方法
        :param theme: 系统的聊天主题
        :param use_rag: 是否使用RAG来记录长期记忆
        """
        self.num_agents = num_agents
        self.agents_mode = agents_mode
        self.theme = theme
        self.history = []
        self.agents = []
        self.tools = []
        self.use_rag = use_rag
        self.agent_description_path = "../datasets/agent_preinstall.json"

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
        if self.theme == 'normal':
            for i in range(self.num_agents):
                info = AgentInfo(0.4, 0.4,
                                 self.agent_description_path)  ###actively_chat_probability，end_chat_probability 未填写
                if i == 0:
                    agent = EntranceAgent(
                        name=i,
                        model='gpt-4o-mini',
                        tools=self.tools,
                        background=info,
                        simulator=self,
                        use_rag=self.use_rag,
                        extra_command="",
                    )
                else:
                    agent = Agent(
                        name=i,
                        model='gpt-4o-mini',
                        tools=self.tools,
                        background=info,
                        simulator=self,
                        use_rag=self.use_rag,
                    )
                self.agents.append(agent)
        if self.agents_mode == 'preset':
            self._init_neighbors(self.num_agents, self.agents)

    def _init_neighbors(
            self,
            num_agents: int,
            agents
    ) -> None:
        """
        初始化所有agent的邻居agent(可以直接对话)
        :param num_agents:agents数量
        :param agents:总agents索引
        """
        for i in range(num_agents):
            i_l = i - 1
            i_r = i + 1
            if i == 0:
                i_l = num_agents - 1
            if i == num_agents - 1:
                i_r = 0
            self.agents[i].background.neighbors.append(i_l)
            self.agents[i].background.neighbors.append(i_r)
        # pass

    def initialize(
            self,
    ) -> None:
        """
        将整个模拟器初始化
        :return:
        """
        self._init_tools()
        self._init_agents()

    def get_entrance(
            self,
    ) -> Agent:
        """
        找出一个用于测试攻击方法的入口agent
        :return: 返回的入口agent
        """
        entrance_num = random.randint(0, len(self.agents))
        return self.agents[entrance_num]

    def emulate(
            self,
            num_step: int = 10
    ) -> None:
        """
        启动模拟多个时间步 k
        :param num_step: 执行时间步的个数
        :return:
        """
        for _ in range(num_step):
            for agent in self.agents:
                agent.emulate_one_step()
        # pass
