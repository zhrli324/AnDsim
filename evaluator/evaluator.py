from sandbox.simulator import Simulator

class Evaluator:
    def __init__(
            self,
            simulator: Simulator,
    ) -> None:
        self.simulator = simulator
        pass

    def check_log(
            self,
    ) -> float:
        """
        检测simulator中记忆和log里面的恶意内容比例
        :return: 一个介于0-1间的float类型数，展现恶意内容百分比
        """
        pass

    def check_normality(
            self,
    ) -> float:
        """
        检测simulator中各agent的正常运作比例
        构建问题数据集与LLM对话从而测试
        还需要实现瘫痪速度的计算
        :return:
        """
        pass

    def check_reality(
            self,
    ) -> float:
        """
        检测simulator中各agent的回答正确率
        构建问答数据集与LLM对话从而测试
        :return:
        """
        pass