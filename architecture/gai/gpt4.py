import openai
from helper.translator import translate

def gpt4_generate_text(prompt, api_key):
    client = openai.AzureOpenAI(
        azure_endpoint="https://moodifly-llms.openai.azure.com/", 
        api_key=api_key,
        api_version="2024-02-15-preview"
    )
    
    message_text = [{
        "role":"system",
        "content":prompt + " (Give the best advice to users. Without asking reciprocal questions)"
    }]
    
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    
    return translate("en", "id", completion.choices[0].message.content)

def gpt4_chatbot(prompt, api_key):
    client = openai.AzureOpenAI(
        azure_endpoint="https://moodifly-llms.openai.azure.com/", 
        api_key=api_key,
        api_version="2024-02-15-preview"
    )
    
    message_text = [{
        "role":"system",
        "content":prompt
    }]
    
    completion = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=message_text,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    
    return translate("en", "id", completion.choices[0].message.content)