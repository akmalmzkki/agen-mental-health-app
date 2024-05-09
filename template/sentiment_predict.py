import streamlit as st
import string
import os
import re
import tensorflow as tf
import dotenv
import nltk

from architecture.gai.gemini import gemini_generate_text
from architecture.gai.gemma import gemma_generate_text
from architecture.gai.llama import llama_generate_text
from architecture.gai.gpt4 import gpt4_generate_text
from architecture.gai.arxiv import arxiv_summarize
from helper.translator import translate

from nltk.corpus import stopwords
from keras_preprocessing.text import tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences
from nltk.stem import WordNetLemmatizer

dotenv.load_dotenv()
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download()

def remove_stopwords(text):
    stop = set(stopwords.words('english'))
    punctuation = list(string.punctuation)
    stop.update(punctuation)
    
    final_text = []
    for i in text.split():
        if i.strip().lower() not in stop:
            final_text.append(i.strip())
    return " ".join(final_text)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))|rt|wa|co|bit|ly', '', text)
    return text

def wnl_lemmatize(text):
    wnl = WordNetLemmatizer()
    text = [wnl.lemmatize(word) for word in text.split()]
    return " ".join(text)

def predict_stress(text):
    model = tf.keras.models.load_model('saved model/bi_lstm_model.h5')
    
    text = preprocess_text(text)
    text = remove_stopwords(text)
    text = wnl_lemmatize(text)
    
    with open('saved model/tokenizer.json') as f:
        data = f.read()
        tokenizer = tokenizer_from_json(data)
    
    tokenized = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(tokenized, maxlen=400)
    text = tf.convert_to_tensor(padded)
    
    prediction = model.predict(text)
    return prediction[0][0]

def models(model, prompt_template):
    if model == "gemini":
        response = gemini_generate_text(translate("id", "en", prompt_template), os.getenv("GEMINI_API_KEY"))
    elif model == "gemma":
        response = gemma_generate_text(translate("id", "en", prompt_template), os.getenv("GRADIO_CLIENT_API_KEY"))
    elif model == "llama":
        response = llama_generate_text(translate("id", "en", prompt_template), os.getenv("GRADIO_CLIENT_API_KEY"))
    else:
        response = gpt4_generate_text(translate("id", "en", prompt_template), os.getenv("AZURE_OPENAI_API_KEY"))
    return response

def sentiment_predict():
    st.markdown("<h1 style='text-align: center; font-family: Open Sans;'>🧠 Konsultasi 💭</h1>", unsafe_allow_html=True)
    st.divider()
    
    genAi1, genAi2, genAi3, genAi4 = st.columns(4)
    model = st.session_state.get("model", "gemini")
    
    if genAi1.button("🌴 Gemini"):
        model = "gemini"
        st.session_state.model = model
        st.success("🎉 Model Gemini telah aktif!")
    
    if genAi2.button("🧠 Gemma"):
        # model = "gemma"
        # st.session_state.model = model
        # st.success("🎉 Model Gemma telah aktif")
        st.error("🚧 Maaf, model Gemma sedang dalam perbaikan. Silakan gunakan model lain.")
    
    if genAi3.button("🦙 Llama"):
        model = "llama"
        st.session_state.model = model
        st.success("🎉 Model Llama telah aktif")
    
    if genAi4.button("🧠 GPT-4"):
        model = "gpt4"
        st.session_state.model = model
        st.success("🎉 Model GPT-4 telah aktif")
        
    message = st.text_area("", height=200, max_chars=500, placeholder="📝 Bagaimana perasaan Anda dalam beberapa minggu terakhir, apakah Anda merasa cemas, sedih, atau tertekan secara berlebihan?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prediksi = st.button("🚀 Prediksi")
        
    with col2:
        reset = st.button("🔄 Reset")
        
    response = translate("id", "en", message) + ", Please give me feedback on what I experienced."
    
    if prediksi:
        with st.spinner("Sedang memproses..."):
            if message:
                prediction = predict_stress(translate("id", "en", message))
                if prediction <= 0.2:
                    st.success(f"😁 Terdeteksi, nampaknya, Anda memiliki tingkat emosi yang rendah sebesar: {prediction*100:.2f}%")
                    st.success(models(model, response))
                elif prediction <= 0.4:
                    st.info(f"😊, Terdeteksi, nampaknya, Anda memiliki tingkat emosi yang sedang-rendah sebesar: {prediction*100:.2f}%")
                    st.info(models(model, response))
                elif prediction <= 0.6:
                    st.info(f"😐, Terdeteksi, nampaknya, Anda memiliki tingkat emosi yang sedang sebesar: {prediction*100:.2f}%")
                    st.info(models(model, response))
                elif prediction <= 0.8:
                    st.warning(f"😕, Terdeteksi, nampaknya, Anda memiliki tingkat emosi yang tinggi-sekali sebesar: {prediction*100:.2f}%")
                    st.warning(models(model, response))
                else:
                    st.error(f"😔, Terdeteksi, nampaknya, Anda memiliki tingkat emosi yang tinggi sebesar: {prediction*100:.2f}%")
                    st.error(models(model, response))
            else:
                st.error("⚠️ Mohon masukkan teks terlebih dahulu.")
        
        st.divider()
        
        st.markdown("<h3 style='text-align: center; font-family: Open Sans;'>👇 Rekomendasi Link Artikel terkait 👇</h3>", unsafe_allow_html=True)
        with st.spinner('⏳ Tunggu sebentar ya...'):
            st.markdown(arxiv_summarize(translate("id", "en", message)))


    if reset:
        st.empty()
        
    st.markdown("---")