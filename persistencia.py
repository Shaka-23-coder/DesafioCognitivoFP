import json
import os

ARCHIVO_DATOS = os.path.join(os.path.dirname(__file__), "licitaciones.json")


def cargar_licitaciones():
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
    except (json.JSONDecodeError, OSError):
        raise RuntimeError("No se pudo leer licitaciones.json. Verifica el archivo.")


def guardar_licitaciones(licitaciones):
    temporal = ARCHIVO_DATOS + ".tmp"
    with open(temporal, "w", encoding="utf-8") as archivo:
        json.dump(licitaciones, archivo, ensure_ascii=False, indent=4)
    os.replace(temporal, ARCHIVO_DATOS)
