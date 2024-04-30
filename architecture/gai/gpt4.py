import openai
from helper.translator import translate

def gpt4_generate_text(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt
    )
    if response.choices[0].text:
        response = translate("en", "id", response.choices[0].text)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response

def gpt4_chatbot(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt
    )
    if response.choices[0].text:
        response = translate("en", "id", response.choices[0].text)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response