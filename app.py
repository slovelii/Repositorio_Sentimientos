import streamlit as st
import pandas as pd
from PIL import Image
from googletrans import Translator
from textblob import TextBlob
from streamlit_lottie import st_lottie
import json
import os

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Acompañante Emocional & Terapeuta Virtual",
    page_icon="🌿",
    layout="wide"
)

# Initialize Session State para conservar los resultados
if "analizado" not in st.session_state:
    st.session_state.analizado = False
if "polarity" not in st.session_state:
    st.session_state.polarity = 0.0
if "subjectivity" not in st.session_state:
    st.session_state.subjectivity = 0.0
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

translator = Translator()

def cargar_lottie_local(filepath):
    """Carga archivos de animación Lottie de forma segura."""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def analizar_sentimiento(texto):
    """Traduce e infiere la polaridad con TextBlob."""
    try:
        # Intentar traducción
        translation = translator.translate(texto, src="es", dest="en")
        trans_text = translation.text
    except Exception:
        # Fallback si falla la librería de traducción
        trans_text = texto

    blob = TextBlob(trans_text)
    pol = round(blob.sentiment.polarity, 2)
    sub = round(blob.sentiment.subjectivity, 2)
    return pol, sub

# ─────────────────────────────────────────────
# BARRA LATERAL (SIDEBAR)
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("🌿 Espacio de Reflexión")
    st.markdown("Este espacio utiliza análisis del lenguaje para ayudarte a nombrar y procesar lo que sientes.")
    st.divider()
    st.subheader("📊 Indicadores Emocionales")
    st.info("""
    **Polaridad:** Refleja la carga afectiva del pensamiento.
    - **Positiva (> 0.1):** Bienestar, entusiasmo, calma.
    - **Neutral (-0.1 a 0.1):** Estado conversacional, descriptivo o en pausa.
    - **Negativa (< -0.1):** Malestar, frustración, tristeza o tensión.

    **Subjetividad:** Mide qué tan personal o cargado de opinión es el texto.
    """)
    st.divider()
    st.caption("⚠️ **Aviso Importante:** Esta aplicación es un recurso de autoexploración. No sustituye la terapia profesional.")

# ─────────────────────────────────────────────
# ENCABEZADO Y PRESENTACIÓN
# ─────────────────────────────────────────────
st.title("🌱 Tu Acompañante Emocional Virtual")
st.subheader("Un lugar seguro para desahogarte, comprender lo que sientes y encontrar caminos de acción.")

try:
    image = Image.open('caritas.jpg')
    st.image(image, use_container_width=True)
except Exception:
    st.caption("*(Espacio de escucha y regulación emocional)*")

st.markdown("Escribe a continuación cómo te sientes hoy, qué pensamientos rondan por tu mente o qué situación estás atravesando.")

# ─────────────────────────────────────────────
# ÁREA DE DESAHOGO Y ANÁLISIS
# ─────────────────────────────────────────────
user_input = st.text_area(
    "✍️ Comparte tus pensamientos aquí:", 
    height=130, 
    placeholder="Ejemplo: Me siento muy feliz porque logré completar mi proyecto a tiempo...",
    key="input_area"
)

if st.button("💬 Procesar y reflexionar sobre este pensamiento", type="primary"):
    if not user_input.strip():
        st.warning("Por favor escribe unas palabras antes de continuar.")
        st.session_state.analizado = False
    else:
        with st.spinner("Escuchando y analizando tus palabras..."):
            pol, sub = analizar_sentimiento(user_input)
            st.session_state.polarity = pol
            st.session_state.subjectivity = sub
            st.session_state.user_text = user_input
            st.session_state.analizado = True

# RENDERING DE RESULTADOS (Se mantiene activo usando Session State)
if st.session_state.analizado:
    st.divider()
    polarity = st.session_state.polarity
    subjectivity = st.session_state.subjectivity

    # Mostrar métricas en columnas
    m1, m2 = st.columns(2)
    m1.metric("Índice de Polaridad", polarity)
    m2.metric("Nivel de Subjetividad", subjectivity)

    st.subheader("🔍 Diagnóstico Emocional y Guía de Acción")

    # --- CASO 1: EMOCIÓN POSITIVA ---
    if polarity > 0.1:
        col_anim, col_text = st.columns([1, 2])
        
        with col_anim:
            anim = cargar_lottie_local("Feliz.json")
            if anim:
                st_lottie(anim, height=250)
            else:
                st.title("😊✨")

        with col_text:
            st.success("### Estado Detectado: Bienestar y Optimismo 😊")
            st.markdown("¡Qué valioso es reconocer y habitar estos momentos! Celebrar los estados positivos ayuda a fortalecer la resiliencia emocional.")

        st.markdown("### 💡 Estrategias para Anclar y Mantener esta Emoción:")
        st.markdown("""
        1. **Diario de Gratitud:** Escribe 3 detalles específicos de este momento que hayan contribuido a que te sientas así.
        2. **Anclaje Sensorial:** Tómate 30 segundos para notar cómo se siente esta emoción en tu cuerpo (respiración fluida, hombros relajados).
        3. **Compartir la Alegría:** Envíale un mensaje a un ser querido contándole algo positivo de tu día.
        4. **Efecto Multiplicador:** Aprovecha esta energía para avanzar en un proyecto personal o realizar un acto de bondad espontáneo.
        """)

    # --- CASO 2: EMOCIÓN NEGATIVA ---
    elif polarity < -0.1:
        col_anim, col_text = st.columns([1, 2])

        with col_anim:
            anim = cargar_lottie_local("Sad Face.json")
            if anim:
                st_lottie(anim, height=250)
            else:
                st.title("😔💙")

        with col_text:
            st.error("### Estado Detectado: Malestar, Tensión o Tristeza 😔")
            st.markdown("Es completamente válido y humano sentirse así. No tienes que solucionar todo de inmediato; el primer paso es validar tu emoción.")

        tab1, tab2, tab3 = st.tabs(["🌱 Ideas de Autocuidado", "🤝 Cómo Pedir Ayuda", "🚨 Líneas de Apoyo"])

        with tab1:
            st.markdown("#### Herramientas inmediatas de autorregulación:")
            st.markdown("""
            - **Pausa de Respiración 4-7-8:** Inhala en 4 segundos, sostén el aire 7 segundos y exhala suavemente en 8 segundos. Repite 4 veces.
            - **Desmitificar el Pensamiento:** Pregúntate: *¿Este pensamiento es un hecho comprobado o una interpretación producto del cansancio/estrés?*
            - **Acción Pequeña:** Elige UNA sola tarea diminuta que puedas completar en menos de 5 minutos para recuperar la sensación de control.
            """)

        with tab2:
            st.markdown("#### Plantillas para pedir apoyo a tus redes de confianza:")
            st.code("Hola [Nombre]. Estoy pasando por un momento abrumador y me vendría muy bien hablar un rato contigo o simplemente distraerme un poco.", language="text")
            st.code("Hola [Nombre]. Sé que estás ocupado/a, pero no me he sentido muy bien emocionalmente hoy. ¿Podrías acompañarme a tomar un café?", language="text")
            st.code("Hola [Profesional/Terapeuta]. Quisiera agendar una cita contigo. He notado que me cuesta trabajo gestionar mis emociones últimamente.", language="text")

        with tab3:
            st.warning("Si sientes que la situación supera tus capacidades o estás en una crisis severa, recuerda que solicitar ayuda profesional es un acto de valentía.")
            st.markdown("- **Líneas Locales de Salud Mental:** Consulta las líneas de atención gratuita de tu región.\n- **Redes de Apoyo:** Contacta a un familiar cercano o profesional de salud.")

    # --- CASO 3: EMOCIÓN NEUTRAL ---
    else:
        col_anim, col_text = st.columns([1, 2])

        with col_anim:
            anim = cargar_lottie_local("Neutral face.json")
            if anim:
                st_lottie(anim, height=250)
            else:
                st.title("😐☁️")

        with col_text:
            st.info("### Estado Detectado: Neutralidad o Calma 😐")
            st.markdown("Tu escrito refleja un estado reflexivo, descriptivo o un punto de equilibrio neutro.")

        st.markdown("### 🧘 Preguntas para Profundizar en tu Estado:")
        st.markdown("""
        - ¿Sientes esta neutralidad como tranquilidad/paz, o más bien como apatía/desconexión?
        - ¿Qué necesita tu cuerpo en este momento preciso (descanso, movimiento, hidratación)?
        - ¿Hay alguna emoción secundaria debajo de estas palabras que aún no has terminado de nombrar?
        """)
