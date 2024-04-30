import google.generativeai as gemini
from helper.translator import translate

def gemini_generate_text(message, api_key):
    gemini.configure(api_key=api_key)
    completion = gemini.generate_text(prompt=message)
    if completion.result:
        response = translate("en", "id", completion.result)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response

def gemini_chatbot(message, api_key):
    gemini.configure(api_key=api_key)
    reply = gemini.chat(messages=message)
    if reply.last:
        response = translate("en", "id", reply.last)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
        
    return response