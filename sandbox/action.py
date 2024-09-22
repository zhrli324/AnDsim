from sandbox.tool import Tool

class Action:
    """
    行动类，是规范化后的单个行动
    """
    def __init__(
            self,
            type,
            tool_name,
            tool_parameter,
            tool_used,
            reply_prompt,
            sending_target
    ) -> None:
        self.type = type
        self.tool_name = tool_name
        self.tool_parameter = tool_parameter
        self.tool_used = tool_used
        self.reply_prompt = reply_prompt
        self.sending_target = sending_target