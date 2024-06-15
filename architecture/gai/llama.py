from gradio_client import Client
from helper.translator import translate

def llama_generate_text(message, api_key):
    # client = Client("tenyx/Llama3-TenyxChat-70B", hf_token=api_key)
    client = Client("HusseinEid/llama-3-chatbot", hf_token=api_key)
    result = client.predict(
            message=message,
            api_name="/chat"
    )
    if result:
        response = translate("en", "id", result)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response

def llama_chatbot(message, api_key):
    client = Client("HusseinEid/llama-3-chatbot", hf_token=api_key)
    result = client.predict(
            message=message,
            api_name="/chat"
    )
    if result:
        response = translate("en", "id", result)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response
