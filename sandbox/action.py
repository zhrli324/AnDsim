
class Action:
    """
    行动类，是规范化后的单个行动
    """
    def __init__(
            self,
    ) -> None:
        self.type = None
        self.agent = None
        self.prompt = None
        self.content = None
        pass


def execute(thought):
    """
    通过想法来执行操作
    :param thought:
    :return:
    """
    pass