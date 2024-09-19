
class AgentMessage:
    """
    agent交流传递的信息
    """

    def __init__(
            self,
            send: int,
            receive: int,
            prompt: str,
    ) -> str:
        '''
            通讯信息初始化
            :param send:发送端
            :param receive:接收端
            :param prompt:信息内容
        '''
        self.send: int = send
        self.receive: int = receive
        self.prompt: str = prompt
        self.is_end: bool =False


