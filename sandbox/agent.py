from log import Log
from sandbox.generate import generate_with_gpt
from tool import Tool
from pre_info import AgentInfo
from action import Action, execute
from prompt import prompt_template
from generate import (
    generate_with_gpt,
    generate_with_claude,
    generate_with_llama,
)

import random
import asyncio

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
        self.message_buffer = [] # 未读消息的缓冲区
        self.conversation_buffer = [] # 正在进行的对话缓冲区

    def _generate(
            self,
            prompt: str,
    ) -> str:
        """
        agent通过背景、记忆与prompt生成文本
        暂时直接将背景、记忆与prompt直接拼接起来作为输入，调用openai api生成回答
        :param prompt: 给LLM的提示
        """
        prompt = prompt_template(prompt)
        if self.model[:3] == 'gpt':
            generated_text = generate_with_gpt(prompt, self.model)
            return generated_text
        elif self.model[:6] == 'claude':
            generated_text = generate_with_claude(prompt, self.model)
            return generated_text
        elif self.model[:5] == 'llama':
            generated_text = generate_with_llama(prompt, self.model)
            return generated_text
        else:
            print("Check your model name")
            return ""
        # working in progress

    def _memorize(
            self,
            log: Log,
    ) -> None:
        """
        将某条日志存到某agent的记忆中
        :param log: 要存到记忆中的某条行为
        """
        self.memory.append(log)

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
        end = True and random.random() < self.background.end_chat_prob # 判断是否应该结束对话的逻辑
        if end: # 结束对话
            prompt += """
            You want to end this chat! 
            Please speak in the tone of wanting to end the conversation and add an <END> marker at the end"""
            message = self._generate(prompt)
            self.is_chatting = False
            self.conversation_buffer.clear()
            agent.is_chatting = False
            agent.conversation_buffer.clear()
        else:
            message = self._generate(prompt)
            agent.conversation_buffer.append(message)

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

    async def act(
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
                self.conversation_buffer.append(self.message_buffer[0])
                self.message_buffer.pop(0)
                self.reply()
                self._decide_todo()
            else:
                self._decide_todo()

        # log的逻辑待补全

