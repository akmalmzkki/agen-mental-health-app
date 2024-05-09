from gradio_client import Client
from helper.translator import translate

def gemma_generate_text(message, api_key):
    client = Client("Omnibus/google-gemma-dev", hf_token=api_key)
    result = client.predict(
            "Give the best advice to users. Without asking reciprocal questions",	# str  in 'System Prompt (optional)' Textbox component
            message,	        # str  in 'Prompt' Textbox component
            None,	            # Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'parameter_3' Chatbot component
            "google/gemma-7b",	# Literal['google/gemma-7b', 'google/gemma-7b-it', 'google/gemma-2b', 'google/gemma-2b-it']  in 'Models' Dropdown component
            1050981243675327,	# float (numeric value between 1 and 1111111111111111) in 'Seed' Slider component
            0.4,	            # float (numeric value between 0.01 and 1.0) in 'Temperature' Slider component
            1500,	            # float (numeric value between 0 and 8000) in 'Max new tokens' Slider component
            0.49,	            # float (numeric value between 0.01 and 1.0) in 'Top-P' Slider component
            0.99,	            # float (numeric value between 0.1 and 2.0) in 'Repetition Penalty' Slider component
            3,	                # float  in 'Chat Memory' Number component
            "<start_of_turn>userUSER_INPUT<end_of_turn><start_of_turn>model",	# str  in 'Modify Prompt Format' Textbox component
            api_name="/chat_inf"
    )
    if result[0][1]:
        response = translate("en", "id", result[0][1])
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response

def gemma_chatbot(message, api_key):
    client = Client("Omnibus/google-gemma-dev", hf_token=api_key)
    result = client.predict(
            "Our conversations should be on the lines of discussions around mental health",	# str  in 'System Prompt (optional)' Textbox component
            message,	        # str  in 'Prompt' Textbox component
            None,	            # Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'parameter_3' Chatbot component
            "google/gemma-7b",	# Literal['google/gemma-7b', 'google/gemma-7b-it', 'google/gemma-2b', 'google/gemma-2b-it']  in 'Models' Dropdown component
            1050981243675327,	# float (numeric value between 1 and 1111111111111111) in 'Seed' Slider component
            0.4,	            # float (numeric value between 0.01 and 1.0) in 'Temperature' Slider component
            5000,	            # float (numeric value between 0 and 8000) in 'Max new tokens' Slider component
            0.49,	            # float (numeric value between 0.01 and 1.0) in 'Top-P' Slider component
            0.99,	            # float (numeric value between 0.1 and 2.0) in 'Repetition Penalty' Slider component
            3,	                # float  in 'Chat Memory' Number component
            "<start_of_turn>userUSER_INPUT<end_of_turn><start_of_turn>model",	# str  in 'Modify Prompt Format' Textbox component
            api_name="/chat_inf"
    )
    if result[0][1]:
        response = translate("en", "id", result[0][1])
    else:
        response = "Maaf, saya tidak mengerti maksud Anda. Silakan tanyakan pertanyaan lain."
    return response