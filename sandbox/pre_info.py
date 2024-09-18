class AgentInfo:
    """
    单个agent的背景信息
    """
    def __init__(
            self,
            actively_chat_probability: float,
            end_chat_probability: float,
    ) -> None:
        self.info = ...
        self.neighbors = []
        self.actively_chat_probability = actively_chat_probability
        self.end_chat_prob = end_chat_probability
        pass