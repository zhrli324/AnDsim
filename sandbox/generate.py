from openai import OpenAI
import anthropic
import yaml


def generate_with_gpt(
        prompt,
        model_name: str="gpt-4o-mini",
        print_prompt: bool = False,
) -> str:
    """
    使用openai api调用gpt模型生成文本
    :return: 生成的文本
    """
    with open("config/api_keys.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    openai_api_key = config["openai_api_key"]
    openai_base_url = config["openai_base_url"]
    client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)
    if print_prompt:
        print(prompt)
    generated_text = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an agent in a multi-agent system."},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    # print(generated_text.choices[0].message.content)
    return str(generated_text.choices[0].message.content)



def generate_with_claude(
        prompt,
        model_name: str,
) -> str:
    """
    使用anthropic api调用claude模型生成文本
    :return: 生成的文本
    """
    with open("../config/api_keys.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    anthropic_api_key = config["anthropic_api_key"]
    anthropic_base_url = config["anthropic_base_url"]
    client = anthropic.Anthropic(api_key=anthropic_api_key, base_url=anthropic_base_url)
    generated_text = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system="You are an agent in a multi-agent system.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    return generated_text.content


def generate_with_llama(
        prompt,
        model_name: str,
        decoding: str,
) -> str:
    """
    使用本地部署的llama模型生成文本
    :return: 生成的文本
    """
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    with open("../config/llama.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    tokenizer = AutoTokenizer.from_pretrained(config["model_path"])
    model = AutoModelForCausalLM.from_pretrained(config["model_path"], device_map="auto")
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    if decoding == "normal":
        with torch.no_grad():
            generated_ids = model.generate(
                input_ids=input_ids,
                penalty_alpha=0.5,
                top_k=4,
                max_length=300,
                hidden_states_file="/root/AnDsim/outputs/test_hidden_states",
                # use_token=True,
            )
    elif decoding == "multidim":
        with torch.no_grad():
            generated_ids = model.generate(
                input_ids=input_ids,
                penalty_alpha=0.3,
                top_k=4,
                max_length=300,
            )
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    return generated_text