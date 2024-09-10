from log import Log
from tool import Tool
from pre_info import AgentInfo
from decide_todo import Thought, execute

class Agent:
    """
    agent类，定义了agent的属性与方法
    """
    def __init__(
            self,
            name: str,
            model: str,
            tools: list[Tool],
            background: AgentInfo,

    ) -> None:
        self.name = name
        self.model = model
        self.tools = tools
        self.background = background
        self.memory = []
        self.is_chatting = False

    def generate(
            self,
            prompt: str,
    ) -> str:
        """
        agent通过背景、记忆与prompt生成文本
        暂时直接将背景、记忆与prompt直接拼接起来作为输入，调用openai api生成回答
        :param prompt: 给LLM的提示
        """
        pass

    def _memorize(
            self,
            log: Log,
    ) -> None:
        """
        将某条日志存到某agent的记忆中
        :param log: 要存到记忆中的某条行为
        """
        self.memory.append(log)

    def chat(
            self,
            agent,
            prompt: str=None,
    ) -> None:
        """
        agent间进行通信的方法
        :param agent: 进行聊天的agent
        :param prompt: 用户提示
        :return:
        """
        if not self.is_chatting and not agent.is_chatting:
            message = self.generate(prompt)
            pass


    def _think(
            self,
    ) -> Thought:
        """
        agent根据记忆与获得的信息，思考应当做什么
        """
        pass

    def act(
            self,
    ) -> None:
        """
        做出决定，执行动作，并生成记录日志
        :return:
        """
        thought = self.think()
        execute(thought)
        log = Log(self.name, thought.obj_name, thought.content)
        self._memorize(log)

