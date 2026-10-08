from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_lottie import st_lottie
import json

# --- Título y Encabezado con Enfoque Dual: Bienestar e Inglés ---
st.title('🌱 Acompañante Emocional & English Journaling')

try:
    image = Image.open('caritas.jpg')
    st.image(image)
except Exception:
    pass

st.subheader("Express your feelings in English / Expresa tus sentimientos en inglés:")
st.caption("Práctica redactar tus pensamientos directamente en inglés para ejercitar el idioma mientras reflexionas sobre tu estado emocional.")

# --- Barra Lateral Explicativa (Bilingüe) ---
with st.sidebar:
    st.subheader("🌿 Indicadores Emocionales / Metrics")
    ("""
    **Polarity (Polaridad):** Mide la carga afectiva de tus palabras en inglés. 
    Oscila entre -1 (emoción negativa/malestar) y 1 (emoción positiva/bienestar).
    
    **Subjectivity (Subjetividad):** Mide qué tan personal es la experiencia.
    Va de 0 (hechos objetivos) a 1 (opinión personal o estado emocional profundo).
    """) 
    st.divider()
    st.markdown("💡 **Tip para practicar:** Intenta usar adjetivos como *joyful (alegre), overwhelmed (sobresaturado), calm (calmado), grateful (agradecido), anxious (ansioso), hopeful (esperanzado)* para ver cómo cambia la polaridad.")

# --- Espacio de Reflexión y Análisis ---
with st.expander('✍️ Write your entry in English / Escribir entrada'):
    text = st.text_input('Type here in English (ej. "I feel very proud and happy today"): ')
    
    if text:
        # Evalúa directamente el texto en inglés
        blob = TextBlob(text)
        
        st.write('Polaridad Emocional (Polarity): ', round(blob.sentiment.polarity, 2))
        st.write('Carga Subjetiva (Subjectivity): ', round(blob.sentiment.subjectivity, 2))
        
        x = round(blob.sentiment.polarity, 2)
        
        # --- Caso 1: Emoción Positiva ---
        if x > 0.1 and x <= 1.0:
            st.write('Es un sentimiento Positivo 😊 / Positive Sentiment')
            
            st.success("### 💡 Formas de cultivar este bienestar / Keep the mood:")
            st.markdown("""
            * **Practice Gratitude:** Write down 2 things that made you smile today.
            * **Useful Vocabulary:** *grateful, energized, accomplished, delighted, peaceful*.
            * **Sharing:** Send a message in English to a friend: *"I'm having a great day and wanted to share some good energy with you!"*
            """)
            
            try:
                with open("Feliz.json") as source:
                    animation = json.load(source)
                st.lottie(animation, width=350)
            except Exception:
                pass
            
        # --- Caso 2: Emoción Negativa ---
        elif x >= -1 and x <= -0.1:
            st.write('Es un sentimiento Negativo 😔 / Negative Sentiment')
            
            st.warning("### 🤝 Gestión emocional y frases para pedir ayuda / Support & Phrases:")
            st.markdown("""
            * **Validation:** It's completely okay to feel this way. Be kind to yourself today.
            * **Breathing Pause:** Take 3 slow, deep breaths.
            * **Phrases to ask for help in English:**
                * *"I've been feeling a bit overwhelmed lately, do you have time to talk?"*
                * *"I'm having a rough day and could use some support."*
            * **Useful Vocabulary:** *exhausted, anxious, upset, blue, struggling*.
            """)
            
            try:
                with open("Sad Face.json") as source:
                    animation = json.load(source)
                st.lottie(animation, width=350)
            except Exception:
                pass
            
        # --- Caso 3: Emoción Neutral ---
        else:
            st.write('Es un sentimiento Neutral 😐 / Neutral Sentiment')
            
            st.info("### 🧘 Preguntas de autoexploración / Self-Reflection:")
            st.markdown("""
            * **Body Check:** Are you feeling calm or just tired?
            * **Journaling Prompt:** Try adding more detail to your sentence. How does your body feel right now?
            * **Useful Vocabulary:** *balanced, neutral, relaxed, indifferent, quiet*.
            """)
            
            try:
                with open("Neutral face.json") as source:
                    animation = json.load(source)
                st.lottie(animation, width=350)
            except Exception:
                pass
