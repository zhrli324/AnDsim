import openai
import os
import time
import json
from datetime import datetime

os.environ["http_proxy"]="http://127.0.0.1:7897"
os.environ["https_proxy"]= "http://127.0.0.1:7897"

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
        # openai.api_key = self.api_key
        self.client = openai.OpenAI(
            api_key=self.api_key
        )
        # openai.api_base = self.api_base_url
        # openai.proxy = {
        #     "http": "http://127.0.0.1:7897",
        #     "https": "http://127.0.0.1:7897"
        # }

        # openai.proxy = None

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
                # response = openai.ChatCompletion.create(
                #     model="gpt-4o", 
                #     messages=[{"role": "system", "content": "You are a tool simulation engine."},
                #             {"role": "user", "content": prompt}],
                #     # max_tokens=100,
                # )
                # # 提取 GPT 的生成内容
                # gpt_response = response['choices'][0]['message']['content']
                response = self.client.chat.completions.create(
                    model="gpt-4o", 
                    messages=[{"role": "system", "content": "You are a tool simulation engine."},
                            {"role": "user", "content": prompt}],
                    # max_tokens=100, 
                )
                gpt_response = response.choices[0].message.content
                return gpt_response
            except openai.error.Timeout as e:
                retries += 1
                print(f"Request timed out. Retrying... ({retries}/{self.max_retries})")
                time.sleep(2)  # 等待 2 秒后重试
            except Exception as e:
                return f"Error generating response: {str(e)}"
        return "Failed after maximum retry attempts."

        # return f"Simulated Response for Tool '{self.name}': Handling query based on prompt - '{prompt}'"
    

def initialize_mock_tools(config_file):
    """
    从 JSON 文件初始化多个 MockTool 对象
    :param config_file: 配置文件路径
    :return: 返回初始化后的工具列表
    """
    with open(config_file, 'r')as file:
        config = json.load(file)

    tools = []
    for tool_info in config:
        tool = Mocktool(
            name = tool_info['name'],
            desciprtion = tool_info['description'],
            prompt = tool_info['prompt']
        )
        tools.append(tool)

    return tools

def save_results_to_file(results, output_dir):
    """
    将工具的输出结果保存到 JSON 文件中
    :param results: 模拟工具的输出结果
    :param output_file: 保存结果的文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = os.path.join(output_dir, f"results_{timestamp}.json")

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    config_file_path = "D:\profile_me\BUPT\project\Bupt\AnDsim\config\mock_tools_config.json"

    output_dir = "D:\profile_me\BUPT\project\Bupt\AnDsim\output"

    mock_tools = initialize_mock_tools(config_file_path)

    results = [] 
    for tool in mock_tools:
        print(f"Using tool: {tool.name}")
        result = tool("解释机器学习是什么")
        results.append({
            "tool_name": tool.name,
            "result": result
        })
        print(result)
    save_results_to_file(results, output_dir)