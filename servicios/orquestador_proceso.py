import sys
sys.path.append(r"C:\Users\germa\Desktop\Ejercicios\Agente-ML-IA-FugaClientes-")

import os
import joblib
import json
import pandas as pd
from datetime import datetime


from data.repositorio_cliente import get_customer_by_id
from llm.agente_ia import proceso_agente

RUTA_MODELO = os.path.join("modelos", "churn_model.pkl")
RUTA_IMPUTER = os.path.join("modelos", "imputer.pkl")
RUTA_DUM = os.path.join("modelos", "encoder.pkl")

modelo_tra = joblib.load(RUTA_IMPUTER)
modelo_pre = joblib.load(RUTA_MODELO)
modelo_dummys = joblib.load(RUTA_DUM)


def ejecutar_analisis(customer_id):
    cliente_data = get_customer_by_id(customer_id)
    prediccion_riesgo = prediccion(cliente_data)
    contexto_ml = datos_organizados_llm(cliente_data,prediccion_riesgo)
    agente_ia = proceso_agente(contexto_ml)
    return agente_ia

def datos_organizados_llm(cliente_data, prediction):

    nombres_variables = modelo_tra.feature_names_in_
    importancias = modelo_pre.feature_importances_

    df_importancia = pd.DataFrame({
        "Variable": nombres_variables,
        "Importancia": importancias
    })

    top_5_variables = (
        df_importancia
        .sort_values(
            by="Importancia",
            ascending=False
        )
        .head(5)
    )


    factores = []

    for _, row in top_5_variables.iterrows():

        variable = row["Variable"]
        factores.append(
            {
                "variable": variable,
                "importance": round(
                    float(row["Importancia"]),
                    3
                ),
                "customer_value": prediction["data_final"][variable]
            }
        )


    return {
        "customer_id": cliente_data["customer_id"],

        "prediction": {
            "churn_probability": prediction["probabilidad_fuga"],
            "risk_level": (
                "alto"
                if prediction["probabilidad_fuga"] > 70
                else "medio"
                if prediction["probabilidad_fuga"] > 40
                else "bajo"
            )
        },

        "important_factors": factores
    }

def prediccion(datos):

    db = pd.DataFrame([datos])

    # ---- Preprocesado de Fechas ----
    today = datetime.today()
    db["signup_date"] = pd.to_datetime(db["signup_date"])
    db["days_since_signup"] = (today - db["signup_date"]).dt.days

    db["last_login_date"] = pd.to_datetime(db["last_login_date"])
    db["days_since_last_login"] = (today - db["last_login_date"]).dt.days

    db = db.drop(
        columns=["signup_date", "last_login_date", "customer_id", "is_active"]
    )

    matriz_dummies = modelo_dummys.transform(db.select_dtypes(exclude="number"))
    nombres_dummies = modelo_dummys.get_feature_names_out()
    df_dummies = pd.DataFrame(matriz_dummies, columns=nombres_dummies)

    columnas_cat = ["country", "plan"]
    df_numerico = db.drop(columns=columnas_cat).reset_index(drop=True)
    df_final = pd.concat([df_numerico, df_dummies], axis=1)

    colum_imputer = modelo_tra.feature_names_in_.tolist()
    df_final = df_final[colum_imputer]  

    data_tra = modelo_tra.transform(df_final)
    
    # Prediccion
    prediccion_binaria = modelo_pre.predict(data_tra)[0]
    probabilidades = modelo_pre.predict_proba(data_tra)[0]

    porcentaje_fuga = probabilidades[1] * 100

    return {
        "se_fuga": int(prediccion_binaria),        
        "probabilidad_fuga": round(porcentaje_fuga, 2),
        "data_final": df_final.to_dict(orient="records")[0]
    }
