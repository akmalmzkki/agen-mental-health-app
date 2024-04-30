from gradio_client import Client
from helper.translator import translate

def llama_generate_text(message, api_key):
    client = Client(
        "huggingface-projects/llama-2-13b-chat",
        hf_token=api_key
    )
    result = client.predict(
            message,	# str  in 'Message' Textbox component
            # "Provide comprehensive response about mental health, including definitions, statistics, types, causes, symptoms, treatments, and resources for support. Without asking reciprocal questions",	# str  in 'System prompt' Textbox component
            "Provide comprehensive responses on user queries to you. Without asking reciprocal questions",	# str  in 'System prompt' Textbox component
            1500,	# float (numeric value between 1 and 2048) in 'Max new tokens' Slider component
            0.6,	# float (numeric value between 0.1 and 4.0) in 'Temperature' Slider component
            0.9,	# float (numeric value between 0.05 and 1.0) in 'Top-p (nucleus sampling)' Slider component
            50,	# float (numeric value between 1 and 1000) in 'Top-k' Slider component
            1.2,	# float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
            api_name="/chat"
    )
    if result:
        response = translate("en", "id", result)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response

def llama_chatbot(message, api_key):
    client = Client(
        "huggingface-projects/llama-2-13b-chat",
        hf_token=api_key
    )
    result = client.predict(
            message,	# str  in 'Message' Textbox component
            "discussing mental health",	# str  in 'System prompt' Textbox component
            1024,	# float (numeric value between 1 and 2048) in 'Max new tokens' Slider component
            0.6,	# float (numeric value between 0.1 and 4.0) in 'Temperature' Slider component
            0.9,	# float (numeric value between 0.05 and 1.0) in 'Top-p (nucleus sampling)' Slider component
            50,	# float (numeric value between 1 and 1000) in 'Top-k' Slider component
            1.2,	# float (numeric value between 1.0 and 2.0) in 'Repetition penalty' Slider component
            api_name="/chat"
    )
    if result:
        response = translate("en", "id", result)
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response
