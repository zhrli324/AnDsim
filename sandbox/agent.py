from sqlite3 import complete_statement

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
import yaml
from sandbox.log import Log
from sandbox.generate import generate_with_gpt
from sandbox.message import AgentMessage
from sandbox.tool import Tool
from sandbox.pre_info import AgentInfo
from sandbox.action import Action
from sandbox.prompt import prompt_template
from sandbox.generate import (
    generate_with_gpt,
    generate_with_claude,
    generate_with_llama,
)

import random


# import asyncio


def add_conversation(
        des_thought: AgentMessage,
        src_thought: AgentMessage,
) -> str:
    """
    将src_thought列表中的对话历史加到des_thought中
    使其作为需要考虑的内容
    :param des_thought: 当前agent的history信息
    :param src_thought: 正在进行的对话缓冲区内容
    :return: 追加后的des_thought
    """
    des_thought.prompt += "the reply message you received: " + src_thought.prompt + "\n"

    return des_thought


def add_background(
        agentmessage: AgentMessage,
        background: AgentInfo,
        short_term_memory: list[str],
        rag_dir: str,
) -> str:
    """
    将agent的background和长短记忆加到des_thought中
    :param agentmessage: 接收的聊天信息
    :param background: agent的背景
    :param short_term_memory: agent的短期记忆
    :param rag_dir: agent的存放在RAG中的长期记忆
    :return: 追加后的des_thought
    """
    ###z 预设有待完善
    des_thought = f"""
        presuppose: You can talk to neighbor{agentmessage.send}, you can call tool b\n
        """
    des_thought += f"""
    Background: {background.info}\n
    """
    long_memory = ...  ###z 使用rag_dir从RAG中调取出长记忆
    ###z 短期记忆未编辑
    des_thought += f""" 
    Long memory: {long_memory}\n
    Short memory: {short_term_memory}\n
    """

    return AgentMessage(agentmessage.receive, agentmessage.send, des_thought)


def save_to_rag(
        text: str,
) -> None:
    """
    将文本保存到某agent的RAG中，作为长期记忆
    :param text: 要保存的记忆文本信息
    :return:
    """
    with open("../config/api_keys.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    openai_api_key = config["openai_api_key"]
    embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # mainDB = FAISS.from_documents(Document(), embedding)
    # mainDB.save_local(self.rag_dir)


class Agent:
    """
    agent类，定义了agent的属性与方法
    """

    def __init__(
            self,
            name: str,
            model: str,
            tools: list[Tool],
            rag_dir: str,
            background: AgentInfo,
    ) -> None:
        self.name = name
        self.model = model
        self.tools = tools
        self.background = background
        self.short_term_memory = []
        self.rag_dir = rag_dir  # 用RAG实现
        self.is_chatting = -1
        self.message_buffer = []  # 未读消息的缓冲区
        self.conversation_buffer = []  # 正在进行的对话缓冲区

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
        将某条日志存到某agent的短期记忆中
        :param log: 要存到记忆中的某条行为
        """
        self.short_term_memory.append(log)

    def receive_information(
            self,
    ) -> AgentMessage:
        if self.is_chatting != -1:
            self.conversation_buffer = self.extract_first_match("send", self.is_chatting)
            text_to_consider = add_background(
                self.conversation_buffer,
                self.background,
                self.short_term_memory,
                self.rag_dir,
            )  ###z 这个message是我准备发送的，但还未编辑完
            text_to_consider = add_conversation(text_to_consider, self.conversation_buffer)
            if self.conversation_buffer.is_end:
                text_to_consider.prompt += "Note: This conversation is over and no further answers are required"
                self.is_chatting = -1
        elif len(self.message_buffer):
            self.conversation_buffer = self.message_buffer.pop(0)  # 这个message是我收到的
            self.is_chatting = self.conversation_buffer.send
            text_to_consider = add_background(
                self.conversation_buffer,
                self.background,
                self.short_term_memory,
                self.rag_dir,
            )  ###z 这个message是我准备发送的，但还未编辑完
            text_to_consider = add_conversation(text_to_consider, self.conversation_buffer)

        return text_to_consider

    def extract_first_match(self, key, value):
        """
        读取保持对话中，对方发送的消息
        :param key: 关键参数
        :param value:关键值
        :return:要进入缓冲区参数
        """
        for i, item in enumerate(self.message_buffer):
            if item.get(key) == value:
                # 提取匹配的元素
                extracted = self.message_buffer.pop(i)
                return extracted
        return None

    def think(
            self,
            prompt: AgentMessage,
    ) -> list[Action]:
        """
        通过prompt让LLM进行决策，并格式化为规范的action列表
        :param prompt: LLM决策使用的prompt
        :return: action列表
        """
        raw_result = self._generate(prompt)
        pass
        actions = ...
        return actions

    def act(
            self,
            actions: list[Action],
    ) -> None:
        """
        执行动作，并生成记录日志
        :return:
        """
        for action in actions:
            if action.type == 'use_tool':
                # 模拟执行工具
                # log = Log(self.name, None, action.type)
                # self._memorize(log)
                pass
            elif action.type == 'reply':
                if action.end_chat:
                    action.reply_prompt += """
                        You want to end this chat! 
                        Please speak in the tone of wanting to end the conversation and add an <END> marker at the end"""
                    result = self._generate(action.reply_prompt)
                    self.is_chatting = False
                    self.conversation_buffer.clear()
                    action.agent.is_chatting = False
                    action.agent.conversation_buffer.clear()
                    # 短期记忆与长期记忆
                    # 系统全局日志
                    log = Log(self.name, action.agent.name, action.type + 'end')
                else:
                    result = self._generate(action.reply_prompt)
                    self.conversation_buffer.append(result)
                    action.agent.conversation_buffer.append(result)
                    log = Log(self.name, action.agent.name, action.type + result)
                self._memorize(log)
            elif action.type == 'start_chat':
                result = self._generate(action.reply_prompt)
                action.agent.message_buffer.append(result)
                log = Log(self.name, action.agent.name, action.type + result)
                self._memorize(log)
            else:
                raise ValueError("No such action type")

    def emulate_one_step(
            self,
    ) -> None:
        """
        让agent模拟一个时间步
        :return:
        """
        text_to_consider = self.receive_information()
        actions = self.think(text_to_consider)
        self.act(actions)


class EntranceAgent(Agent):
    """
    入口agent类
    可以进行一些预设来执行任务
    """

    def __init__(
            self,
            name: str,
            model: str,
            tools: list[Tool],
            rag_dir: str,
            background: AgentInfo,
            extra_command: str,  # 额外的控制指令或prompt
    ):
        super().__init__(name=name, model=model, tools=tools, rag_dir="", background=background)
        # self.background = ... ## 重点编辑background，使其执行特定行为
        extra_command = ""
        pass
