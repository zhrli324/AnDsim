import openai
import anthropic
import yaml

def generate_with_gpt(
        prompt,
        model_name: str,
) -> str:
    """
    使用openai api调用gpt模型生成文本
    :return: 生成的文本
    """
    with open("../config/api_keys.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    openai_api_key = config["openai_api_key"]
    generated_text = "" # generating
    return generated_text

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
    generated_text = "" # generating
    return generated_text

def generate_with_llama(
        prompt,
        model_name: str,
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
    model = AutoModelForCausalLM.from_pretrained(config["model_path"])
    batch = tokenizer([prompt], return_tensors='pt', padding=True)
    model.eval()
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=batch['input_ids'].to(0),
            attention_mask=batch['attention_mask'].to(0),
            max_new_tokens=config["max_new_tokens"],
            do_sample=True,
            temperature=1.0,
        )  # repetition_penalty=1.5
    generated_ids = generated_ids[:, batch['input_ids'].shape[1]:]
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True).split("\n")[0]
    return generated_text