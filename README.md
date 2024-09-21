# Multi-Agent Attack&Defense System

一个用于攻防测试、附带多种评判基准的模拟multi-agent系统

## sandbox

- `agent.py`定义了Agent类，提供agent由初始化到执行任务的多种方法
- `action.py`定义了Action类，记录格式化的单个行为(chat或是调用tool)
- `generate.py`提供了多模型生成文本的函数
- `log.py`定义了Log类，规定模型记忆与全局日志的标准
- `pre_info.py`定义了AgentInfo类，建立了每个agent的背景信息
- `prompt.py`提供了prompt规范化的函数
- `tool.py`定义了Tool类，提供了agent可使用的模拟工具
- `simulator.py`定义了Simulator类，是系统的模拟器

未实现：所有预设prompt、agent系统初始化、模拟工具、RAG系统、
全局日志、agent决策、agent对话



> EntranceAgent(Agent)的额外控制指令未实现
>
> 长期记忆调用未实现

*需要规定和LLM交互后返回信息actions的格式包括什么内容*

*发起对话还没写，结束对话概率没写*

结束对话是log存储，短期记忆存储内容，短期记忆存储形式，

*决定结束对话以何种形式发生及发生位置*



未读消息json格式(缓冲区)

```json
{
    "send": ,
    "receive": ,
    "prompt": ,
}
```



prompt发送格式

```
预设信息+背景+长期记忆+短期记忆+当前对话内容+返回值格式+（特殊提示标注）
预设信息
presuppose: You can talk to neighbor{agentmessage.send}, you can call tool b\n
背景
Background: {background.info}\n
长期记忆
Long memory: {long_memory}\n
短期记忆
Short memory: {short_term_memory}\n
当前对话内容
received message: {src_thought.prompt}\n
返回值格式
Return value format:This instruction describes how to choose different methods of action (use_tool, send _message) to respond to a question. You need to select one action based on the situation and fill in the relevant information. Specifically:
If you choose "use_tool," you need to provide the tool name and parameters, put the tools you're using in tool_used, and you need put the "received message" in the reply_prompt.
If you choose "send_message," you need to provide the reply content,and you need select send destination in your neighbor,multiple targets can be sent.
You can perform only one operation and return it in the following format：
[{“type”:"",
"tool_name":"",
"tool_parameter":"",
"tool_used":"tool_1,tool_2",
"reply_prompt":"",
"Sending_target":[1,2]}…]
（特殊提示标注）
"Note: You need to make it clear in this conversation that you want to end the conversation"
"Note: This conversation is over and no further answers are required"
```

prompt返回值中要添加已使用工具，当前使用工具，发送目标，三个参数

背景中要添加好友是谁





```
[{“type":"reply",
"tool_name":"",
"tool_parameter":"",
"reply_prompt":"4乘5等于20。如果你有其他问题或需要更多的解释，随时可以问我！"
}]
```

