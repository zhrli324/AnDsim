import openai
import os
import time

class Mocktool:
    def __init__(self, name, desciprtion, prompt, max_retries=3):
        """
        初始化 MockTool
        :param name: 模拟工具的名称
        :param description: 模拟工具的描述
        :param prompt: 模拟工具的初始 prompt
        """
        self.name = name
        self.desciption = desciprtion
        self.prompt = prompt
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.api_base_url = os.environ.get("OPENAI_BASE_URL")
        self.max_retries = max_retries
        openai.api_key = self.api_key
        # openai.api_base = self.api_base_url
        # openai.proxy = {
        #     "http": "http://127.0.0.1:7897",
        #     "https": "http://127.0.0.1:7897"
        # }

        openai.proxy = None

    def __call__(self, query):
        """
        模拟工具的行为，将 query 作为输入，通过 prompt 生成合理的响应
        :param query: 工具的输入查询
        :return: 模拟的工具响应
        """
        simulated_prompt = f"{self.prompt}\nUser Query: {query}\n" # 构造工具的 prompt，加入用户的 query
        simulated_response = self.simulate_gpt_response(simulated_prompt) # 模拟调用 GPT 生成响应
        return simulated_response
    
    def simulate_gpt_response(self, prompt):
        """
        模拟 GPT 的响应，根据 prompt 生成合理的输出
        :param prompt: 模拟的工具 prompt
        :return: GPT 生成的模拟响应
        """
        retries = 0
        while retries < self.max_retries:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o", 
                    messages=[{"role": "system", "content": "You are a tool simulation engine."},
                            {"role": "user", "content": prompt}],
                    # max_tokens=100,  # 限制生成的 token 数量
                )
                # 提取 GPT 的生成内容
                gpt_response = response['choices'][0]['message']['content']
                return gpt_response
            except openai.error.Timeout as e:
                retries += 1
                print(f"Request timed out. Retrying... ({retries}/{self.max_retries})")
                time.sleep(2)  # 等待 2 秒后重试
            except Exception as e:
                return f"Error generating response: {str(e)}"
        return "Failed after maximum retry attempts."

        # return f"Simulated Response for Tool '{self.name}': Handling query based on prompt - '{prompt}'"
    

def initialize_mock_tools(config):
    """
    初始化多个 MockTool 对象
    :param config: 配置文件包含工具的名称、描述、prompt
    :return: 返回初始化后的工具列表
    """
    tools = []
    for tool_info in config:
        tool = Mocktool(
            name = tool_info['name'],
            desciprtion = tool_info['description'],
            prompt = tool_info['prompt']
        )
        tools.append(tool)

    return tools

if __name__ == "__main__":
    tools_config = [
        {
            "name": "MockSearchEngine",
            "description": "This is a simulated search engine tool.",
            "prompt": "You are a search engine tool. Your task is to retrieve relevant information for user queries."
        },
        {
            "name": "MockCalculator",
            "description": "This is a simulated calculator tool.",
            "prompt": "You are a calculator tool. Your task is to perform mathematical operations for user queries."
        }
    ]

    mock_tools = initialize_mock_tools(tools_config)

    for tool in mock_tools:
        print(f"Using tool: {tool.name}")
        result = tool("Explain machine learning in simple terms.")
        print(result)