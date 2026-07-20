# "herramientas del agente"

def tool_descuentos_clientes(entrada_ml):
    descuento = 0
    if entrada_ml["risk_level"] == "alto":
        descuento = 30
    elif entrada_ml["risk_level"] == "medio":
        descuento = 15
        
    return f"descuento a aplicar : {descuento}%"