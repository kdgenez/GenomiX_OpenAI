from langchain_groq import ChatGroq  # ✅ correcto

# Crea el LLM Groq con LangChain

def get_llm(model_name: str, api_key: str):
    if not api_key:
        raise RuntimeError("GROQ_API_KEY no proporcionada")

    llm = ChatGroq(
        temperature=0.2,
        model_name=model_name,
        groq_api_key=api_key,
        max_tokens=None,
    )
    return llm
