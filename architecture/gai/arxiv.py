from gradio_client import Client
from helper.translator import translate

def arxiv_summarize(text):
    client = Client("bishmoy/Arxiv-CS-RAG")
    result = client.predict(
		text,	# str  in 'Search' Textbox component
		4,	# float (numeric value between 4 and 10) in 'Top n results as context' Slider component
		"Semantic Search - up to 22 Apr 2024",	# Literal['Semantic Search - up to 22 Apr 2024', 'Arxiv Search - Latest - (EXPERIMENTAL)']  in 'Search Source' Dropdown component
		"mistralai/Mixtral-8x7B-Instruct-v0.1",	# Literal['mistralai/Mixtral-8x7B-Instruct-v0.1', 'mistralai/Mistral-7B-Instruct-v0.2', 'google/gemma-7b-it', 'None']  in 'LLM Model' Dropdown component
		api_name="/update_with_rag_md"
    )
    
    if "###" in result[0]:
        result = result[0].replace("###", "####")
        
    if "# 🔍 Search Results" in result:
        result = result.replace("# 🔍 Search Results", "")	

    return result