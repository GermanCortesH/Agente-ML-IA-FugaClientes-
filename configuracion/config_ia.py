import sys
sys.path.append(r"C:\Users\germa\Desktop\Ejercicios\Agente-ML-IA-FugaClientes-")

from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

from configuracion.config import settings

def get_llm():

    print("Provider:", settings.LLM_PROVIDER)
    print("Modelo:", settings.OPENAI_MODEL)
    print("API:", bool(settings.OPENAI_API_KEY))

    if settings.LLM_PROVIDER == "ollama":
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            # base_url=settings.OLLAMA_BASE_URL,
            temperature=0
        )

    elif settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            # temperature=0,
            # max_tokens=500
        )


    raise ValueError(f"Proveedor no soportado: {settings.LLM_PROVIDER}")

def get_embeddings():

    if settings.EMBEDDING_PROVIDER == "ollama":
        return OllamaEmbeddings(
            model=settings.OLLAMA_EMBEDDING_MODEL,
            base_url=settings.OLLAMA_BASE_URL
        )

    elif settings.EMBEDDING_PROVIDER == "openai":
        return OpenAIEmbeddings(
            model=settings.OPENAI_EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY
        )

    raise ValueError(f"Proveedor no soportado: {settings.EMBEDDING_PROVIDER}")