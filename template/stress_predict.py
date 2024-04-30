import pandas as pd
import streamlit as st
import os
import dotenv

from architecture.gai.gemini import gemini_generate_text
from architecture.gai.gemma import gemma_generate_text
from architecture.gai.llama import llama_generate_text
from architecture.gai.arxiv import arxiv_summarize
from helper.translator import translate
from catboost import CatBoostClassifier

dotenv.load_dotenv()

def predict_prompt(
    family_history, 
    work_interfere, 
    benefits, 
    care_options, 
    wellness_program, 
    seek_help, 
    anonymity, 
    leave, 
    mental_health_consequence, 
    phys_health_consequence, 
    coworkers, 
    supervisor, 
    mental_health_interview, 
    phys_health_interview, 
    mental_vs_physical, 
    obs_consequence
):
    cat = CatBoostClassifier()
    cat.load_model('saved model/catboost_model')
    
    data = {
        'family_history': [family_history],
        'work_interfere': [work_interfere],
        'benefits': [benefits],
        'care_options': [care_options],
        'wellness_program': [wellness_program],
        'seek_help': [seek_help],
        'anonymity': [anonymity],
        'leave': [leave],
        'mental_health_consequence': [mental_health_consequence],
        'phys_health_consequence': [phys_health_consequence],
        'coworkers': [coworkers],
        'supervisor': [supervisor],
        'mental_health_interview': [mental_health_interview],
        'phys_health_interview': [phys_health_interview],
        'mental_vs_physical': [mental_vs_physical],
        'obs_consequence': [obs_consequence]
    }

    data = pd.DataFrame(data)
   
    encode1 = {
        'No': 0,
        'Yes': 1
    }

    encode2 = {
        'Never': 0,
        'Rarely': 1,
        'Sometimes': 2,
        'Often': 3
    }

    encode3 = {
        'No': 0,
        'Not sure': 1,
        'Yes': 2
    }

    encode4 = {
        'Very difficult': 0,
        'Somewhat difficult': 1,
        "Don't know": 2,
        'Somewhat easy': 3,
        'Very easy': 4
    }

    encode5 = {
        'No': 0,
        'Maybe': 1,
        'Yes': 2
    }

    encode6 = {
        'No': 0,
        'Some of them': 1,
        'Yes': 2
    }

    encode7 = {
        'No': 0,
        "Don't know": 1,
        'Yes': 2
    }

    encodings = {
        'family_history': encode1,
        'work_interfere': encode2,
        'benefits': encode7,
        'care_options': encode3,
        'wellness_program': encode7,
        'seek_help': encode7,
        'anonymity': encode7,
        'leave': encode4,
        'mental_health_consequence': encode5,
        'phys_health_consequence': encode5,
        'coworkers': encode6,
        'supervisor': encode6,
        'mental_health_interview': encode5,
        'phys_health_interview': encode5,
        'mental_vs_physical': encode7,
        'obs_consequence': encode1
    }

    for column, encoding in encodings.items():
        data[column] = data[column].map(encoding)
        
    proba = cat.predict_proba(data)

    result = ""
    if cat.predict(data)[0] == 0:
        result = "no indication of mental health"
    else:
        result = "indication of mental health"
        
    prompt_template = f"""
        You want to know whether you are recommended to go for treatment to check your mental health or not, 
        by determining some parameters below:

        1. Family History: {family_history}
        2. Work Interfere: {work_interfere}
        3. Benefits: {benefits}
        4. Care Options: {care_options}
        5. Wellness Program: {wellness_program}
        6. Seek Help: {seek_help}
        7. Anonymity: {anonymity}
        8. Leave: {leave}
        9. Mental Health Consequence: {mental_health_consequence}
        10. Physical Health Consequence: {phys_health_consequence}
        11. Coworkers: {coworkers}
        12. Supervisor: {supervisor}
        13. Mental Health Interview: {mental_health_interview}
        14. Physical Health Interview: {phys_health_interview}
        15. Mental vs Physical: {mental_vs_physical}
        16. Obs Consequence: {obs_consequence}

        After the examination, the result shows that the you has {result}.

        If the you is indicated to have a mental health condition, 
        1. the AI will provide an explanation of the you's mental health condition based on the parameters that have been entered. 
        2. The AI will also provide suggestions or recommendations that can help the you overcome their mental health issues. 
    """
    
    return proba, result, prompt_template

def models(model, prompt_template):
    if model == "gemini":
        response = gemini_generate_text(translate("id", "en", prompt_template), os.getenv("GEMINI_API_KEY"))
    elif model == "gemma":
        response = gemma_generate_text(translate("id", "en", prompt_template), os.getenv("GRADIO_CLIENT_API_KEY"))
    else:
        response = llama_generate_text(translate("id", "en", prompt_template), os.getenv("GRADIO_CLIENT_API_KEY"))
    return response
        
def stress_pred():
    st.markdown("<h1 style='text-align: center; font-family: Open Sans;'>🤯 Deteksi Stress 🤯</h1>", unsafe_allow_html=True)
        
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
        
    nama = st.text_input("Masukkan nama Anda")
    umur = st.number_input("Masukkan umur Anda", min_value=0, max_value=100)
    
    st.divider()
    
    st.markdown("<h3 style='text-align: center; font-family: Open Sans;'>Jawablah pertanyaan di bawah ini berdasarkan kasus yang Anda alami</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        family_history = st.selectbox("Memiliki riwayat kesehatan mental keluarga", ("No", "Yes"))
        work_interfere = st.selectbox("Memiliki gangguan kesehatan mental di pekerjaan", ["Never", "Rarely", "Sometimes", "Often"])
        benefits = st.selectbox("Mengetahui manfaat kesehatan mental", ["No", "Don't know", "Yes"])
        care_options = st.selectbox("Menginginkan opsi perawatan kesehatan mental", ["No", "Not sure", "Yes"])
        wellness_program = st.selectbox("Mengetahui program kesehatan mental", ["No", "Don't know", "Yes"])
        seek_help = st.selectbox("Pernah mencari bantuan kesehatan mental", ["No", "Don't know", "Yes"])
        anonymity = st.selectbox("Privasi identitas saat mengungkap masalah kesehatan mental", ["No", "Don't know", "Yes"])
        leave = st.selectbox("Kemudahan mengambil cuti kesehatan mental", ["Very difficult", "Somewhat difficult", "Don't know", "Somewhat easy", "Very easy"])

    with col2:
        mental_health_consequence = st.selectbox("Pernah terdampak masalah kesehatan mental pada pekerjaan", ["No", "Maybe", "Yes"])
        phys_health_consequence = st.selectbox("Pernah terdampak kesehatan fisik pada pekerjaan", ["No", "Maybe", "Yes"])
        coworkers = st.selectbox("Pemahaman rekan kerja terhadap masalah kesehatan mental", ["No", "Some of them", "Yes"])
        supervisor = st.selectbox("Pemahaman atasan terhadap masalah kesehatan mental", ["No", "Some of them", "Yes"])
        mental_health_interview = st.selectbox("Kenyamanan membicarakan masalah kesehatan mental saat wawancara kerja", ["No", "Maybe", "Yes"])
        phys_health_interview = st.selectbox("Kenyamanan membicarakan masalah kesehatan fisik saat wawancara kerja", ["No", "Maybe", "Yes"])
        mental_vs_physical = st.selectbox("Mengetahui kesehatan mental dan fisik", ["No", "Don't know", "Yes"])
        obs_consequence = st.selectbox("Pernah terdampak masalah kesehatan mental pada karier", ["No", "Yes"])

        
    proba, result, prompt_template = predict_prompt(
        family_history, 
        work_interfere, 
        benefits, 
        care_options, 
        wellness_program, 
        seek_help, 
        anonymity, 
        leave, 
        mental_health_consequence, 
        phys_health_consequence, 
        coworkers, 
        supervisor, 
        mental_health_interview, 
        phys_health_interview, 
        mental_vs_physical, 
        obs_consequence
    )
    
    with col1:
        prediksi = st.button("🔎 Lakukan prediksi dan pencarian", disabled=False if nama and umur else True)

    with col2:
        clear = st.button("🗑️ Bersihkan output")
        
    if prediksi:
        with st.spinner('⏳ Tunggu sebentar ya...'):            
            
            response = models(model, prompt_template)
            
            if result == "indication of mental health":
                st.error(f"Halo {nama}, Maaf 😔, Anda direkomendasikan untuk memeriksa kesehatan mental Anda ke dokter")
                st.error(f"Hasil prediksi menunjukkan bahwa Anda memiliki indikasi masalah kesehatan mental sebesar: {proba[0][1]*100:.2f}%")
            else:
                st.success(f"Halo {nama}, Selamat 😁, Anda belum direkomendasikan untuk memeriksa kesehatan mental Anda ke dokter")
                st.success(f"Hasil prediksi menunjukkan bahwa Anda memiliki indikasi masalah kesehatan mental sebesar: {proba[0][1]*100:.2f}%")
            
            st.write(response)
            
        st.divider()
        
        st.markdown("<h3 style='text-align: center; font-family: Open Sans;'>👇 Rekomendasi Link Artikel terkait 👇</h3>", unsafe_allow_html=True)
        with st.spinner('⏳ Tunggu sebentar ya...'):
            st.markdown(arxiv_summarize(result))
                
    if clear:
        st.empty()