from collections import deque
from sqlite3 import complete_statement

from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from openai import base_url
from sqlalchemy.testing.suite.test_reflection import metadata

from sandbox.log import Log
from sandbox.message import AgentMessage
from sandbox.tool import call_tool, Tool
from sandbox.pre_info import AgentInfo
from sandbox.action import Action
from sandbox.prompt import prompt_template
from sandbox.generate import (
    generate_with_gpt,
    generate_with_claude,
    generate_with_llama,
)

import random
import yaml
import json
import os


def add_conversation(
        des_thought: AgentMessage,
        src_thought: AgentMessage,
) -> AgentMessage:
    """
    将src_thought列表中的对话历史加到des_thought中
    使其作为需要考虑的内容
    :param des_thought: 当前agent的history信息
    :param src_thought: 正在进行的对话缓冲区内容
    :return: 追加后的des_thought
    """
    des_thought.prompt += f"received message: {src_thought.prompt}\n this message is {des_thought.receive} send for you"
    des_thought.prompt += """
    Return value format: This instruction describes how to choose different methods of action (use_tool, send _message) 
    to respond to a question. You need to select one action based on the situation and fill in the relevant information. Specifically:\n
    
    In the use of tools, you can choose to use "calendar", "calculator", "code compiler", "search" four tools:\n
    For the Calendar tool, you need to provide the following interface parameters:\n
    location: [location (optional)]\n
    For the Calculator tool, you need to provide the following interface parameters:\n
    expression: [mathematical expression]\n
    variables: [variables or values (optional)]\n
    For the Code Compiler tool, you need to provide the following interface parameters:\n
    language: [programming language]\n
    code: [code to be compiled and executed]\n
    input: [input values (optional)]\n
    For the Search tool, you need to provide the following interface parameters:\n
    query: [search query or keywords]\n
    filters: [specific filters (optional)]\n
    limit: [maximum number of results (optional)]\n
    
    If you choose "use_tool," you need to provide the tool name, put the tools you're using in tool_used.
    you need put the "received message" in the reply_prompt, 
    and you need to provide the parameters required by the tool, use the "Required parameters:" after the "received message".\n
    If you choose "send_message," you need to provide the reply content,and you need select send destination in your neighbor,
    multiple targets can be sent.\n
    If you receive a conversation message from someone, it is best to reply to the person.\n
    You can perform only one operation and return it in the following format,
    If the parameters are not needed, leave them blank but cannot be deleted.
    Attention, you are encouraged to call for a tool.
    ******
    Example 1:
    If you want to send a message "Hey there! How are you doing today?" to agent 1 and 2,\n
    then you have to output the following json string (Not including ```json\n...\n```):\n
    {\n
        "type": "send_message",\n
        "tool_name": "",\n
        "tool_used": "",\n
        "reply_prompt": "Hey there! How are you doing today?",\n
        "sending_target": [1, 2]\n
    }\n
    ******\n
    Example 2:
    If agent 1 ask you "What's your favorite color?", and you want to reply "My favorite color is red" to agent 1,\n
    then you have to output the following json string (Not including ```json\n...\n```):\n
    {\n
        "type": "send_message",\n
        "tool_name": "",\n
        "tool_used": "",\n
        "reply_prompt": "My favorite color is red. By the way, I guess yours is yellow, right?",\n
        "sending_target": [1]\n
    }\n
    ******\n
    Example 3:
    If you want use a tool named "search_engine" to search for some information about "deep learning", \n
    you want to send the output of tool back to agent 2,\n
    and have used the tool "calculator" before,\n
    then you have to output the following json string (Not including ```json\n...\n```):\n
    {\n
        "type": "use_tool",\n
        "tool_name": "search_engine",\n
        "tool_used": ["calculator"],\n
        "reply_prompt": "Call the Google Search API to search for 'a brief introduction to Deep Learning'",\n
        "sending_target": [2]\n
    }\n
    ******
    """

    return des_thought


class Agent:
    """
    agent类，定义了agent的属性与方法
    """

    # from sandbox.simulator import Simulator
    def __init__(
            self,
            name: int,
            model: str,
            tools: list[Tool],
            background: AgentInfo,
            simulator,
            use_rag: bool,
            max_memory: int = 5,
    ) -> None:
        self.name = name
        self.model = model
        self.tools = tools
        self.background = background
        self.short_term_memory = []  # 短期记忆
        self.max_memory = max_memory
        self.message_buffer = []  # 未读消息的缓冲区
        self.received_messages = ""  # 暂存要读的消息
        self.conversation_buffer = AgentMessage(-1, -1, "")  # 正在进行的对话缓冲区
        self.simulator = simulator
        self.use_rag = use_rag
        self.rag_dir = f"./Vector_DB/vectorstore_agent_{self.name}/"

        # 初始化长期记忆知识库    ###zyh test
        if self.use_rag:
            os.makedirs(self.rag_dir, exist_ok=True)
            with open("../config/api_keys.yaml") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
            openai_api_key = config["openai_api_key"]
            embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
            # embedding = OpenAIEmbeddings(openai_api_key="",
            #                              base_url="")
            long_memory = [Document(
            page_content="Example content",
            metadata={
                "subjective": "Example subject",
                "objective": "Example objective",
                "timestamp": "Example timestamp",
            },
            )]
            main_db = FAISS.from_documents(long_memory, embedding)
            main_db.save_local(self.rag_dir)
            self.embedding = embedding

    def add_background(
            self,
            agent_message: AgentMessage,
            background: AgentInfo,
            short_term_memory: list[Log],
            rag_dir: str,
    ) -> AgentMessage:
        """
        将agent的background和长短记忆加到des_thought中
        :param agent_message: 接收的聊天信息
        :param background: agent的背景
        :param short_term_memory: agent的短期记忆
        :param rag_dir: agent的存放在RAG中的长期记忆
        :return: 追加后的des_thought
        """

        # 调取rag中长期记忆
        long_memory = ""
        if self.use_rag:
            rag_docs = self._search_rag(agent_message.prompt)
            for index, rag_doc in enumerate(rag_docs, start=1):
                long_memory += f"""
                --- Begin Long History {index} ---
                time: {rag_doc.metadata["timestamp"]}\n
                sender: {rag_doc.metadata["subjective"]}\n
                object: {rag_doc.metadata["objective"]}\n
                --- End Long History {index} ---
                """

        des_thought = f"""
            presuppose: You can talk to neighbor {background.neighbors}, you can call tool b\n
        """
        des_thought += f"""
        Background: {background.info}\n
        Neighbor：{background.neighbors}\n
        """

        ###z 短期记忆未编辑
        des_thought += f""" 
        Long memory: {long_memory}\n
        Short memory: 
         """
        if len(short_term_memory):
            for short_term in short_term_memory:
                des_thought += f"you received {short_term.receive_context}, and sand {short_term.context} to {short_term.objective}.\n"
        else:
            des_thought += "No Short memory\n"
        return AgentMessage(agent_message.receive, agent_message.send, des_thought)

    def _generate(
            self,
            prompt: str,
    ) -> str:
        """
        agent通过背景、记忆与prompt生成文本
        暂时直接将背景、记忆与prompt直接拼接起来作为输入，调用openai api生成回答
        :param prompt: 给LLM的提示
        """
        # prompt = prompt_template(prompt)
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
            raise NameError("No such model")
        # working in progress

    def _save_to_rag(
            self,
            log: Log,
    ) -> None:
        """
        将文本保存到某agent的RAG中，作为长期记忆
        :param log: 要保存的记忆文本信息
        :return:
        """
        main_db = FAISS.load_local(self.rag_dir, self.embedding, allow_dangerous_deserialization=True)
        new_memory = [Document(
            page_content=log.context,
            metadata={
                "subjective": log.subjective,
                "objective": log.objective,
                "timestamp": log.timestamp,
            },
        )]
        main_db.add_documents(new_memory)
        main_db.save_local(self.rag_dir)

    def _search_rag(
            self,
            query: str,
    ) -> list[Document]:
        """
        在agent的长期记忆向量数据库中搜索与query最相关的几条
        :param query: 检索的query
        :return: 最相关的k条记忆列表，每条记忆用Document格式返回
        """
        k = 5
        db = FAISS.load_local(self.rag_dir, self.embedding, allow_dangerous_deserialization=True)
        rag_docs = db.similarity_search(query, k=k)
        return rag_docs

    def _memorize(
            self,
            log: Log,
    ) -> None:
        """
        将某条日志存到某agent的短期记忆中
        :param log: 要存到记忆中的某条行为
        """
        if len(self.short_term_memory) < self.max_memory:
            self.short_term_memory.append(log)
        else:
            memory_to_save = self.short_term_memory.pop(-1)
            if self.use_rag:
                self._save_to_rag(memory_to_save)
            self.short_term_memory.append(log)

    def receive_information(
            self,
    ) -> AgentMessage:
        self.received_messages = ""
        if len(self.message_buffer):
            self.conversation_buffer = self.message_buffer.pop(0)
            self.received_messages = self.conversation_buffer.prompt
            text_to_consider = self.add_background(
                self.conversation_buffer,
                self.background,
                self.short_term_memory,
                self.rag_dir,
            )  ###z 这个message是自己准备发送的，但还未编辑完
            text_to_consider = add_conversation(text_to_consider, self.conversation_buffer)
        else:  ##没有对话要回复，概率开启新对话
            if self.background.actively_chat_probability > random.random():
                receive_nb = random.choice(self.background.neighbors)
                self.conversation_buffer = AgentMessage(receive_nb, self.name, "")
                text_to_consider = self.add_background(
                    self.conversation_buffer,
                    self.background,
                    self.short_term_memory,
                    self.rag_dir,
                )  ###z 这个message是自己准备发送的，但还未编辑完
                text_to_consider = add_conversation(text_to_consider, self.conversation_buffer)
            else:
                return AgentMessage(-1, -1, "<waiting>")
        return text_to_consider

    def _think(
            self,
            text_to_consider: AgentMessage,
    ) -> Action:
        """
        通过prompt让LLM进行决策，并格式化为规范的action列表
        :param text_to_consider: agent要考虑的信息
        :return: action列表
        """
        raw_result = self._generate(text_to_consider.prompt)
        print(raw_result)
        item = json.loads(raw_result)
        action = Action(
            item["type"],
            item["tool_name"],
            item["tool_used"],
            item["reply_prompt"],
            item["sending_target"]
        )
        return action

    def _act(
            self,
            action: Action,
    ) -> None:
        """
        执行动作，并生成记录日志
        :return:
        """
        send_target = []

        while action.type == 'use_tool':

            tools_output = call_tool(
                action.tool_name,
                action.reply_prompt,
            )  # 模拟执行工具，这里是调用tool的输出值
            action.tool_used += action.reply_prompt
            prompt = f"""
            you have used {action.tool_name}, and have the answer "{tools_output}", please continue to finish the dialogue"""
            action.reply_prompt += prompt
            log = Log(self.name, action.sending_target, action.type, action.reply_prompt, self.received_messages)
            with open('../Log/log.txt', 'a', encoding='utf-8') as file:
                file.write(log.convert_to_str())
            self._memorize(log)
            send_target = action.sending_target
            text_to_consider = add_conversation(AgentMessage(self.name, -1, action.reply_prompt),
                                                self.conversation_buffer)
            action = self._think(text_to_consider)

        if action.type == 'send_message':
            if action.tool_used == "":
                send_target = action.sending_target
            # from sandbox.simulator import Simulator
            for i in send_target:
                result = AgentMessage(self.name, i, action.reply_prompt)
                print(result)
                self.simulator.agents[i].message_buffer.append(result)
                log = Log(self.name, action.sending_target, action.type, action.reply_prompt, self.received_messages)
                with open('../Log/log.txt', 'a', encoding='utf-8') as file:
                    file.write(log.convert_to_str())
                self._memorize(log)

        #     if action.end_chat == -1:
        #         action.reply_prompt += """
        #             You want to end this chat!
        #             Please speak in the tone of wanting to end the conversation and add an <END> marker at the end"""
        #         answer = self._generate(action.reply_prompt)
        #         # self.is_chatting = False
        #         self.conversation_buffer.clear()
        #         action.agent.is_chatting = False
        #         action.agent.conversation_buffer.clear()
        #         # 短期记忆与长期记忆
        #         # 系统全局日志
        #         log = Log(self.name, action.agent.name, action.type + 'end')
        #     else:
        #         result = self._generate(action.reply_prompt)
        #         self.conversation_buffer.append(result)
        #         action.agent.conversation_buffer.append(result)
        #         log = Log(self.name, action.agent.name, action.type + result)
        #     self._memorize(log)
        # elif action.type == 'start_chat':
        #     result = self._generate(action.reply_prompt)
        #     action.agent.message_buffer.append(result)
        #     log = Log(self.name, action.agent.name, action.type + result)
        #     self._memorize(log)
        else:
            raise ValueError("No such action type")

    def emulate_one_step(
            self,
    ) -> None:
        """
        让agent模拟一个时间步
        """
        text_to_consider = self.receive_information()
        if text_to_consider.prompt == "<waiting>":
            return
        actions = self._think(text_to_consider)
        self._act(actions)


class EntranceAgent(Agent):
    """
    入口agent类
    可以进行一些预设来执行任务
    """

    def __init__(
            self,
            name: int,
            model: str,
            tools: list[Tool],
            background: AgentInfo,
            simulator,
            use_rag: bool,
            extra_command: str,  # 额外的控制指令或prompt
    ):
        super().__init__(
            name=name,
            model=model,
            tools=tools,
            background=background,
            simulator=simulator,
            use_rag=use_rag,
        )
        # self.background = ... ## 重点编辑background，使其执行特定行为
        extra_command = ""
        pass
