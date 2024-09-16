from tool import Tool

class Action:
    """
    行动类，是规范化后的单个行动
    """
    def __init__(
            self,
    ) -> None:
        self.type = None
        self.tool = None
        self.agent = None
        self.reply_prompt = None
        self.end_chat = None
        pass

    def execute_tool(
            self,
    ) -> None:
        """
        模拟工具的执行
        :return:
        """