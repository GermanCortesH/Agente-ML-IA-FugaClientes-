import sys
sys.path.append(r"C:\Users\germa\Desktop\Ejercicios\Agente-ML-IA-FugaClientes-")

import streamlit as st
import pandas as pd
import numpy 
import requests

from llm.agente_ia import creacion_agente_ia
from servicios.orquestador_proceso import ejecutar_analisis

API_BASE_URL = "http://127.0.0.1:8000/customers"
st.set_page_config(page_title="Agente IA - churn", layout="wide")


if "input_cliente" not in st.session_state:
    st.session_state.input_cliente = None  
if "resultado_analisis" not in st.session_state:
    st.session_state["resultado_analisis"] = None

col_sidebar, col_espacio_izq, col_contenido, col_espacio_der = st.columns(
    [0.1,0.05,0.3,0.05])

with col_sidebar:
    messages = st.container(height=200)
    if id_cliente := st.chat_input("ID cliente"):
        messages.chat_message("user").write(f"el ID del cliente es :{id_cliente}")
        messages.chat_message("assistant").write(f"Agente: analizando al cliente {id_cliente}")
        st.session_state['input_cliente'] = id_cliente

with col_contenido:
    st.title("Agente inteligente para fuga de usuarios")
    st.markdown("Informacion del cliente")

    if st.session_state["input_cliente"]:
        with st.spinner("pensando"):
            try:
                url_final = f"{API_BASE_URL}/{st.session_state['input_cliente']}"
                response = requests.get(url_final)
                if response.status_code == 200:
                    st.session_state["resultado_analisis"] = response.json()
                    st.session_state["ultimo_cliente"] = id_cliente

            except:
                st.error("problemas con el agente")

        if st.session_state["resultado_analisis"]:
            resultado = st.session_state["resultado_analisis"]
            st.success(
                f" Mostrando resultados para el cliente ID: {st.session_state['ultimo_cliente']}"
            )
            st.write(resultado)

    else:
        st.warning("Por favor, introduce un ID de cliente en el chat.")

