
class AgentMessage:
    """
    agent交流传递的信息
    """

    def __init__(
            self,
            send: list,
            receive: list,
            prompt: str,
    ) -> None:
        """
        通讯信息初始化
        :param send:发送端
        :param receive:接收端
        :param prompt:信息内容
        """
        self.send: list = send
        self.receive: list = receive
        self.prompt: str = prompt
