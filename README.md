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