import requests
import json

proxy = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897"
}

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer OPENAI_API_KEY", 
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4o", 
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain machine learning in simple terms."}
    ],
    "max_tokens": 50 
}

response = requests.post(url, headers=headers, json=data, proxies=proxy)

print(response.status_code)
print(response.json())
