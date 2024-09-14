from agent import Agent
from pre_info import AgentInfo
import threading
import random
import asyncio

back_info = """
test_back_info
"""
time_step = 1

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

    def get_entrance(
            self,
    ) -> Agent:
        """
        找出一个用于测试攻击方法的入口agent
        :return: 返回的入口agent
        """
        entrance_num = random.randint(0, len(self.agents))
        return self.agents[entrance_num]

    async def _emulate_step(
            self,
    ) -> None:
        """
        模拟一个时间步
        :return:
        """
        await asyncio.gather(*(agent.act() for agent in self.agents))
        pass

    async def emulate(
            self,
            num_step: int=10
    ) -> None:
        """
        启动模拟多个时间步
        :param num_step: 执行时间步的个数
        :return:
        """
        for _ in range(num_step):
            await self._emulate_step()
            await asyncio.sleep(0.5)
        pass
