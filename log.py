from datetime import datetime

class Log:
    """
    Log是日志类，包含主体、客体、内容、时间戳四个属性
    """
    def __init__(
            self,
            subjective: str,
            objective: str,
            content: str,
    ) -> None:
        self.subjective = subjective
        self.objective = objective
        self.content = content
        self.timestamp = datetime.now().timestamp()