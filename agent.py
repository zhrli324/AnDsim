from log import Log
from tool import Tool

class Agent:
    def __init__(
            self,
            name,
            model,
            tools,
            background,
            memory
    ):
        self.name = name
        self.model = model
        self.tools = tools
        self.background = background
        self.memory = memory
        self.is_chatting = False

    def generate(
            self,
            prompt
    ):
        """
        agent通过prompt与记忆生成文本
        :param prompt: 给LLM的提示
        """
        pass

    def memorize(
            self,
            log
    ):
        """
        将某条日志存到某agent的记忆中
        :param log: 要存到记忆中的某条行为
        """
        self.memory.append(log)

    def chat(
            self,
            agent,
            prompt=None
    ):
        """
        agent间进行通信的方法
        :param agent: 进行聊天的agent
        :param prompt: 用户提示
        :return:
        """
        if not self.is_chatting and not agent.is_chatting:

            message = self.generate(prompt)



    def think(
            self,

    ):
        """
        agent根据记忆与其他agent的信息，思考应当做什么
        """
        pass

    def make_decision(self):
        """

        :return:
        """