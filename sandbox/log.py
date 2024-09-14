from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Log:
    """
    Log是日志类，包含主体、客体、内容、时间戳四个属性
    """
    subjective: str
    objective: str
    context: str
    timestamp: float = field(init=False)

    def __post_init__(self):
        self.timestamp = datetime.now().timestamp()