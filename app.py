import streamlit as st

# ======== CONFIGURACIÓN =========
st.set_page_config(
    page_title="GenomiX - Agente de Biología",
    page_icon="assets/favicon.png",
    layout="wide"
)

# Paleta de colores GenomiX
GENOMIX_COLORS = {
    "azul": "#1B365D",       # rigor académico
    "cian": "#00C2D1",       # tecnología
    "verde": "#2ECC71",      # naturaleza
    "gris": "#4D4D4D"        # equilibrio
}

# CSS para identidad visual
st.markdown(f"""
    <style>
        body {{
            font-family: 'Roboto', sans-serif;
            color: {GENOMIX_COLORS['gris']};
        }}
        .title-genomix {{
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            color: {GENOMIX_COLORS['azul']};
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        .subtitle-genomix {{
            font-size: 1.2rem;
            color: {GENOMIX_COLORS['cian']};
            text-align: center;
            margin-bottom: 2rem;
        }}
        .chat-box {{
            background-color: #F9F9F9;
            border: 1px solid {GENOMIX_COLORS['cian']};
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
        }}
        .bot-response {{
            color: {GENOMIX_COLORS['azul']};
            font-weight: 500;
        }}
        .user-query {{
            color: {GENOMIX_COLORS['verde']};
            font-style: italic;
        }}
    </style>
""", unsafe_allow_html=True)

# ======== CABECERA =========
st.markdown('<div class="title-genomix">GenomiX 🔬</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-genomix">"Donde la biología se encuentra con la inteligencia"</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("assets/logo.png", width=200)

st.write("---")

# ======== SIMULACIÓN DE CHAT =========
st.subheader("💬 Conversación con GenomiX")

user_input = st.text_input("Escribe tu pregunta biológica:", placeholder="Ejemplo: ¿Cómo funciona la fotosíntesis?")

if user_input:
    st.markdown(f"<div class='chat-box user-query'>👤 Tú: {user_input}</div>", unsafe_allow_html=True)
    respuesta = """
    🔬 <span class='bot-response'>GenomiX:</span>  
    La fotosíntesis es un proceso mediante el cual las plantas convierten la energía de la luz en energía química.  
    Si lo pensamos como una fábrica, la luz es la fuente de energía, el CO₂ es la materia prima  
    y la glucosa es el producto terminado que alimenta al organismo.
    """
    st.markdown(f"<div class='chat-box'>{respuesta}</div>", unsafe_allow_html=True)

# ======== SIDEBAR =========
st.sidebar.image("assets/logo.png", width=100)
st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("**GenomiX - Identidad de Marca**")
st.sidebar.markdown(f"- Azul: {GENOMIX_COLORS['azul']}")
st.sidebar.markdown(f"- Cian: {GENOMIX_COLORS['cian']}")
st.sidebar.markdown(f"- Verde: {GENOMIX_COLORS['verde']}")
st.sidebar.markdown(f"- Gris: {GENOMIX_COLORS['gris']}")
st.sidebar.write("---")
st.sidebar.info("💡 Este es un mockup visual. El modelo LLM se integrará en la versión final con Groq.")
