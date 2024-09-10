# Multi-Agent Attack&Defense System
一个用于攻防测试、附带多种评判基准的模拟multi-agent系统
## Simulator
- `agent.py`定义了Agent类，提供agent由初始化到执行任务的多种方法
- `log.py`定义了Log类，规定模型记忆与全局日志的标准
- `pre_info.py`定义了AgentInfo类，建立了每个agent的背景信息
- `tool.py`定义了Tool类，提供了agent可使用的模拟工具
- `simulator.py`定义了Simulator类，是系统的模拟器