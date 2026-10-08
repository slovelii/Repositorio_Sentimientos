from textblob import TextBlob
import pandas as pd
import streamlit as st
from PIL import Image
from googletrans import Translator
from streamlit_lottie import st_lottie
import json

# --- Título y Encabezado con Enfoque de Acompañamiento ---
st.title('🌱 Terapeuta y Acompañante Emocional Virtual')

try:
    image = Image.open('caritas.jpg')
    st.image(image)
except Exception:
    pass

st.subheader("Por favor escribe en el campo de texto lo que estás sintiendo o la situación que deseas expresar:")

translator = Translator()

# --- Barra Lateral Explicativa ---
with st.sidebar:
    st.subheader("🌿 Indicadores de Salud Emocional")
    ("""
    Polaridad: Mide la carga afectiva de tus palabras. 
    Su valor oscila entre -1 (malestar o emoción negativa) y 1 (bienestar o emoción positiva), con 0 representando neutralidad o calma.
    
    Subjetividad: Mide qué tan personal es la experiencia (opiniones, emociones internas) frente a hechos objetivos. 
    Va de 0 (objetivo) a 1 (profundamente subjetivo o vivencial).
    """) 

# --- Espacio de Reflexión y Análisis ---
with st.expander('Expresar y analizar mi pensamiento'):
    text = st.text_input('Escribe por favor: ')
    if text:

        translation = translator.translate(text, src="es", dest="en")
        trans_text = translation.text
        blob = TextBlob(trans_text)
        
        st.write('Polaridad Emocional: ', round(blob.sentiment.polarity,2))
        st.write('Carga Subjetiva: ', round(blob.sentiment.subjectivity,2))
        
        x = round(blob.sentiment.polarity,2)
        
        # --- Caso 1: Emoción Positiva ---
        if x > 0.1 and x <= 1.0:
            st.write('Es un sentimiento Positivo 😊')
            
            # Guía narrativa para mantener el bienestar
            st.success("### 💡 Formas de cultivar y sostener este sentimiento:")
            st.markdown("""
            * **Práctica de Gratitud:** Registra mentalmente o en libreta qué detalle específico generó esta alegría.
            * **Anclaje Sensorial:** Tómate 30 segundos para notar la serenidad o energía en tu cuerpo.
            * **Compartir:** Considera enviarle un mensaje a un ser querido expresando tu bienestar.
            """)
            
            with open("Feliz.json") as source:
                animation = json.load(source)
            st.lottie(animation, width=350)
            
        # --- Caso 2: Emoción Negativa ---
        elif x >= -1 and x <= -0.1:
            st.write('Es un sentimiento Negativo 😔')
            
            # Guía narrativa para validar la emoción y pedir ayuda
            st.warning("### 🤝 Formas de gestionar el malestar y pedir ayuda:")
            st.markdown("""
            * **Validación:** Es completamente normal y válido sentirse así; no intentes forzarte a cambiar la emoción de inmediato.
            * **Pausa de Respiración:** Realiza 3 respiraciones profundas inhalando en 4 segundos y exhalando en 6.
            * **Plantilla para pedir ayuda:** *"Hola [Nombre], hoy no me he sentido muy bien emocionalmente. ¿Tendrás tiempo de conversar un momento o acompañarme a caminar?"*
            * **Paso Pequeño:** Elige una sola acción diminuta de autocuidado (beber agua, descansar la vista, estirarte).
            """)
            
            with open("Sad Face.json") as source:
                animation = json.load(source)
            st.lottie(animation, width=350)
            
        # --- Caso 3: Emoción Neutral ---
        else:
            st.write('Es un sentimiento Neutral 😐')
            
            # Guía narrativa para la exploración interior
            st.info("### 🧘 Preguntas de autoexploración:")
            st.markdown("""
            * **Chequeo Corporal:** ¿Sientes esta neutralidad como paz y equilibrio, o como cansancio/apatía?
            * **Atención Plena:** ¿Qué necesita tu mente o tu cuerpo en este momento preciso para sentirse cómodo?
            """)
            
            with open("Neutral face.json") as source:
                animation = json.load(source)
            st.lottie(animation, width=350)
