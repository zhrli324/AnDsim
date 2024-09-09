

class Tool:
    def __init__(
            self,
            name,
            description,
            prompt,
            model="gpt-4o-mini"
    ):
        """
        初始化tool
        tool的初始化配置应当从tools_config.json中读取
        :param name: tool的名称
        :param model: tool所使用的模型代号
        :param description: tool的描述
        :param prompt: tool的初始prompt
        """
        self.name = name
        self.model = model
        self.description = description
        self.prompt = prompt

    def __call__(
            self,
            *args,
            **kwargs
    ):
        """
        调用模拟tool
        套用不同工具的输入输出格式，进行执行与反馈
        :param args:
        :param kwargs:
        :return:
        """
        pass