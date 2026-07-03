# codigo de diseño del agente 
import sys
sys.path.append(r"C:\Users\germa\Desktop\Ejercicios\Agente-ML-IA-FugaClientes-")


from langchain_core.prompts import MessagesPlaceholder,ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents import create_tool_calling_agent

from llm.tools_agente import tool_descuentos_clientes
from llm.prompts import SYSTEM_PROMPT,HUMAN_PROMPT_CHURN

@tool
def busqueda_descuento_cliente(contexto_ml: dict) -> str:
    """Calcula el descuento que se dará al cliente dependiendo del riesgo.
        Args:
            contexto_ml: Un diccionario que contiene obligatoriamente la clave 'risk_level'"""
    return tool_descuentos_clientes(contexto_ml)
tools = [busqueda_descuento_cliente]

prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human",HUMAN_PROMPT_CHURN),
    MessagesPlaceholder(variable_name="agent_scratchpad") 
])

def creacion_agente_ia():
    llm = ChatOllama(model="llama3.1", temperature=0)
    agent = create_tool_calling_agent(llm, tools, prompt_template)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)

def proceso_agente(contexto_ml,agente_AI):
    agente = agente_AI
    resultado = agente.invoke({
        "customer_id": contexto_ml["customer_id"],
        "churn_probability": contexto_ml["prediction"]["churn_probability"],
        "risk_level": contexto_ml["prediction"]["risk_level"],
        "important_factors": contexto_ml["important_factors"]
    })
    return resultado["output"]                           