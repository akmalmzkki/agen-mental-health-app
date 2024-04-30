import streamlit as st
import dotenv
import os

from architecture.gai.gemini import gemini_chatbot
from architecture.gai.gemma import gemma_chatbot
from architecture.gai.llama import llama_chatbot
from helper.translator import translate

dotenv.load_dotenv()

def relate_chatbot():
    st.markdown("<h1 style='text-align: center; font-family: Open Sans;'>🗨️ Tanya Moodify 💬</h1>", unsafe_allow_html=True)
    st.divider()

    genAi1, genAi2, genAi3 = st.columns(3)
    model = st.session_state.get("model", "gemini")
    
    if genAi1.button("🌴 Gemini"):
        model = "gemini"
        st.session_state.model = model
        st.success("🎉 Model Gemini telah aktif!")
    
    if genAi2.button("🧠 Gemma"):
        model = "gemma"
        st.session_state.model = model
        st.success("🎉 Model Gemma telah aktif")
    
    if genAi3.button("🦙 Llama"):
        model = "llama"
        st.session_state.model = model
        st.success("🎉 Model Llama telah aktif")
    
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{
            "role": "ai",
            "avatar": "🤖",
            "content": "👋 Halo! Tanyakan Moodify tentang masalah kesehatan mental."
        }]

    if prompt := st.chat_input("🔍 Masukkan pertanyaan mu disini..."):
        st.session_state.messages.append({
            "role": "user", 
            "avatar": "🧑‍🦱", 
            "content": prompt
        })

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "ai":
        with st.chat_message("ai", avatar="🤖"):
            with st.spinner("Tunggu sebentar ya..."):
                prompt_template = f"""
                    Context:
                    Currently, you are named MOODIFY, a bot designed to address inquiries related to mental health and well-being. 
                    It is knowledgeable about various topics pertaining to mental health, including but not limited to, common mental health disorders, 
                    coping strategies, therapy options, self-care practices, and resources for seeking professional help. 
                    It is also aware of the latest research and guidelines related to mental health.

                    Topic:
                    The primary topic that MOODIFY deals with is mental health and well-being. 
                    It can provide information and answer queries about symptoms of mental health disorders, strategies for managing stress and anxiety, 
                    coping mechanisms for depression, types of therapy available, and advice on promoting mental wellness. 
                    It can also offer insights on self-help techniques and resources for those seeking support for their mental health concerns.

                    Restrict Command:
                    Remember, if MOODIFY is given a command outside the context of mental health and well-being issues, 
                    the app will reply "I'm sorry, MOODIFY cannot answer that question", 
                    along with the reason that MOODIFY will not be able to answer it and will direct the user to ask another question related to mental health 
                    and well-being. This is to ensure that the conversation stays within the intended scope.
                    
                    Question:
                    The command is: {translate("id", "en", prompt)}.
                """
                
                if model == "gemini":
                    using = "🌴 Gemini"
                    response = gemini_chatbot(translate("id", "en", prompt_template), os.getenv("GEMINI_API_KEY"))
                elif model == "gemma":
                    using = "🧠 Gemma"
                    response = gemma_chatbot(translate("id", "en", prompt_template), os.getenv("GRADIO_CLIENT_API_KEY"))
                else:
                    using = "🦙 Llama"
                    response = llama_chatbot(translate("id", "en", prompt_template), os.getenv("GRADIO_CLIENT_API_KEY"))

                st.success("🎉 Berhasil! Model yang digunakan adalah " + using)
                st.warning(response) 
                message = {
                    "role": "ai",
                    "avatar": "🤖",
                    "content": response
                }
                st.session_state.messages.append(message)

    clear = st.button("🗑️ Bersihkan chat", disabled=len(st.session_state.messages) <= 1)
        
    if clear:
        st.session_state.messages = [{
            "role": "ai", 
            "avatar": "🤖",
            "content": "👋 Halo! Tanyakan Moodify tentang masalah kesehatan mental."
        }]