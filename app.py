import os
import streamlit as st
from src.utils import get_llm
from src.agents.biology_agent import build_biology_agent

# ======== CONFIGURACIÓN =========
st.set_page_config(
    page_title="GenomiX - Donde la biología se encuentra con la inteligencia.",
    page_icon="🧬",  # fallback si no encuentra favicon
    layout="centered",
)

# ======== IDENTIDAD VISUAL =========
GENOMIX_COLORS = {
    "azul": "#1B365D",       # rigor académico
    "cian": "#00C2D1",       # tecnología
    "verde": "#2ECC71",      # naturaleza
    "gris": "#4D4D4D"        # equilibrio
}

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
    </style>
""", unsafe_allow_html=True)

# ======== CABECERA =========
st.markdown('<div class="title-genomix">GenomiX 🔬</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-genomix">"Donde la biología se encuentra con la inteligencia"</div>', unsafe_allow_html=True)

# Logo centrado (si existe en /assets)
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, width=200)

st.write("---")

# ======== SIDEBAR =========
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=100)

st.sidebar.title("⚙️ Configuración")
st.sidebar.markdown("**GenomiX - Identidad de Marca**")
st.sidebar.markdown(f"- Azul: {GENOMIX_COLORS['azul']}")
st.sidebar.markdown(f"- Cian: {GENOMIX_COLORS['cian']}")
st.sidebar.markdown(f"- Verde: {GENOMIX_COLORS['verde']}")
st.sidebar.markdown(f"- Gris: {GENOMIX_COLORS['gris']}")
st.sidebar.write("---")

with st.sidebar:
    st.header("🔑 Conexión con Groq")

    # Ingreso manual de API Key
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    user_api_key = st.text_input("Tu GROQ_API_KEY", type="password", value=st.session_state.api_key)
    if user_api_key:
        st.session_state.api_key = user_api_key
        st.success("✅ Clave ingresada")

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

# ======== VALIDACIÓN API KEY =========
api_key = st.session_state.api_key or st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
if not api_key:
    st.warning("⚠️ Ingresa tu GROQ_API_KEY en la barra lateral o en `.streamlit/secrets.toml`.")
    st.stop()

# ======== INICIALIZA AGENTE =========
llm = get_llm(model, api_key)
agent = build_biology_agent(llm, verbose=show_thoughts)

# ======== CHAT =========
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
