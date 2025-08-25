import os
import streamlit as st
from src.utils import get_llm
from src.agents.biology_agent import build_biology_agent
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# ======== CONFIGURACIÓN =========
st.set_page_config(
    page_title="GenomiX - Donde la biología se encuentra con la inteligencia.",
    page_icon="assets/favicon.png",
    layout="centered",
)

# Logo y título
st.image("assets/logo.png", width=200)
st.title("🧬 GenomiX - Agente Experto en Biología")
st.markdown("Agente experto en biología, capaz de explicar procesos complejos, identificar especies y responder preguntas científicas con precisión.")

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

with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Ingreso manual de API Key
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    user_api_key = st.text_input("🔑 Tu GROQ_API_KEY", type="password", value=st.session_state.api_key)
    if user_api_key:
        st.session_state.api_key = user_api_key

    default_model = st.session_state.get("model", "llama-3.1-8b-instant")
    model = st.selectbox(
        "Modelo Groq",
        [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
        ],
        index=["llama-3.1-8b-instant","llama-3.1-70b-versatile","mixtral-8x7b-32768","gemma2-9b-it"].index(default_model)
    )
    st.session_state["model"] = model

    detail = st.radio("Nivel de detalle", ["breve", "intermedio", "profundo"], index=1)
    show_thoughts = st.checkbox("Mostrar trazas del agente (pasos y herramientas)", value=True)

# Determinar si hay clave válida
api_key = st.session_state.api_key or st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Por favor ingresa tu GROQ_API_KEY en la barra lateral o en secrets para continuar.")
    st.stop()

# Inicializa LLM y agente
llm = get_llm(model, api_key)
agent = build_biology_agent(llm, verbose=show_thoughts)

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Escribe tu pregunta o describe la especie/proceso biológico…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando como biólogo…"):
            try:
                resp = agent.invoke({
                    "input": prompt,
                    "detail": detail
                })
                output = resp.get("output", "(Sin respuesta)")
                if show_thoughts and resp.get("intermediate_steps"):
                    with st.expander("🔍 Pasos del agente"):
                        for i, (action, observation) in enumerate(resp["intermediate_steps"], 1):
                            st.markdown(f"**Paso {i} – Acción:** {action}")
                            st.markdown(f"**Observación:** {observation}")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error ejecutando el agente: {e}")
                output = f"Ocurrió un error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": output})
