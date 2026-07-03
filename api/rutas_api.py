import sys
sys.path.append(r"C:\Users\germa\Desktop\Ejercicios\Agente-ML-IA-FugaClientes-")

from fastapi import FastAPI
import uvicorn
import os
from servicios.orquestador_proceso import ejecutar_analisis
from llm.agente_ia import creacion_agente_ia

app = FastAPI()
AGENTE_GLOBAL = creacion_agente_ia()

print(os.getcwd())
@app.get("/customers/{customer_id}")
def inicio_proceso(customer_id: int) :
    resultado = ejecutar_analisis(customer_id, AGENTE_GLOBAL)
    return resultado

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)