from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Log:
    """
    Log是记忆或日志类，包含主体、客体、内容、时间戳四个属性
    """
    subjective: str
    objective: str
    context: str
    timestamp: float = field(init=False)

    def __post_init__(self):
        self.timestamp = datetime.now().timestamp()

    def convert_to_str(self) -> str:
        """
        将log转化为字符串
        """
        return f"""
            subjective: {self.subjective}
            objective: {self.objective}
            context: {self.context}
            timestamp: {self.timestamp}
        """