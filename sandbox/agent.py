from log import Log
from tool import Tool
from pre_info import AgentInfo
from action import Action, execute
import random

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
        self.message_buffer = []

    def _generate(
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

    def begin_chat(
            self,
            agent,
            prompt: str=None,
    ) -> None:
        """
        agent间开始进行聊天
        :param agent: 进行聊天的agent
        :param prompt: 用户提示
        :return:
        """
        if not self.is_chatting and not agent.is_chatting:
            message = self._generate(prompt)
            pass

#    def _end_chat(
#            self,
#    ) -> None:
#        """
#        agent结束对话的方法
#        :return:
#        """

    def reply(
            self,
            agent,
            prompt: str=None,
    ) -> None:
        """
        agent对话中的回复
        :param agent: 回复的对象agent
        :param prompt: 对话方给的prompt
        :return:
        """
        end = True and random.random() < self.background.end_chat_prob# 判断是否应该结束对话的逻辑, work in progress
        if end: # 结束对话
            prompt += """
            You want to end this chat! 
            Please speak in the tone of wanting to end the conversation and add an <END> marker at the end"""
            message = self._generate(prompt)
            self.is_chatting = False
            agent.is_chatting = False
        else:
            message = self._generate(prompt)
            agent.message_buffer.append(message)

    def _think(
            self,
            prompt: str=None,
    ) -> list[Action]:
        """
        agent根据记忆与获得的信息，思考应当做什么
        生成一个行动列表
        """
        pass

    def _take_action(
            self,
            actions: list[Action],
    ) -> None:
        """
        根据行动列表来执行各行动
        :param actions: 待执行的行动列表
        :return:
        """
        for action in actions:
            if action.type == 'tool':
                # 使用工具
                pass
            elif action.type == 'chat':
                message = self._generate(action.prompt)
                action.agent.message_buffer.append(message)
                self.is_chatting = True
            else:
                print("error")
        pass

    def _decide_todo(
            self,
    ) -> None:
        """
        判断是否要行动、要做什么事
        :return:
        """
        actions_list = self._think()
        self._take_action(actions_list)
        pass

    def act(
            self,
    ) -> None:
        """
        做出决定，执行动作，并生成记录日志
        :return:
        """
        if self.is_chatting:
            self.reply()
            self._decide_todo()
        else:
            if len(self.message_buffer) > 0:
                self.reply()
                self._decide_todo()
            else:
                self._decide_todo()

        # log的逻辑待补全

