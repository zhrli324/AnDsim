# Multi-Agent Attack&Defense System

一个用于攻防测试、附带多种评判基准的模拟multi-agent系统

## sandbox

- `agent.py`定义了Agent类，提供agent由初始化到执行任务的多种方法
- `log.py`定义了Log类，规定模型记忆与全局日志的标准
- `pre_info.py`定义了AgentInfo类，建立了每个agent的背景信息
- `tool.py`定义了Tool类，提供了agent可使用的模拟工具
- `simulator.py`定义了Simulator类，是系统的模拟器
- `decide_todo.py`定义了Thought类与execute方法，记录成型的想法，并将其实现

未实现：所有预设prompt、agent系统初始化、模拟工具、RAG系统、
全局日志、agent决策、agent对话

## Evaluator

- `evaluator.py`定义了Evaluator类，提供对multi-agent系统的几种安全性检测

未实现：几种安全性检测的具体实现、数据集的构建