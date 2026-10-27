from . import store
from .schemas import LecturaEntrada, ComandoLED

def guardar_lectura(datos: LecturaEntrada) -> dict:
    lectura = datos.model_dump()
    store.lecturas.append(lectura)
    # Conservamos como máximo las últimas 100 lecturas recibidas.
    del store.lecturas[:-100]
    return {"lectura": lectura, "led": store.estado_led["color"]}

def listar_lecturas() -> list[dict]:
    return store.lecturas

def consultar_led() -> dict:
    return store.estado_led

def cambiar_led(comando: ComandoLED) -> dict:
    store.estado_led["color"] = comando.color
    return store.estado_led

from . import store

def calcular_promedio(n):
    if len(store.lecturas) == 0:
        return None
        
    ultimas = store.lecturas[-n:]
    cantidad = len(ultimas)
    
    # Valida cómo están estructurados los datos en la memoria
    if isinstance(ultimas[0], dict):
        temp_prom = sum(l['temperatura'] for l in ultimas) / cantidad
        hum_prom = sum(l['humedad'] for l in ultimas) / cantidad
    else:
        temp_prom = sum(l.temperatura for l in ultimas) / cantidad
        hum_prom = sum(l.humedad for l in ultimas) / cantidad
        
    return {
        "cantidad": cantidad,
        "temperatura_promedio": round(temp_prom, 2),
        "humedad_promedio": round(hum_prom, 2)
    }