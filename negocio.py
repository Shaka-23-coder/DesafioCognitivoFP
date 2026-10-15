from datetime import date
from persistencia import cargar_licitaciones, guardar_licitaciones
from validaciones import validar_licitacion


def siguiente_id(registros):
    mayor = 0
    for registro in registros:
        codigo = registro.get("id", "")
        if codigo.startswith("LIC-"):
            try:
                mayor = max(mayor, int(codigo[4:]))
            except ValueError:
                pass
    return f"LIC-{mayor + 1:04d}"


def registrar_licitacion(datos):
    validar_licitacion(datos)
    registros = cargar_licitaciones()

    numero = datos["numero_licitacion"].strip().casefold()
    entidad = datos["entidad"].strip().casefold()
    for registro in registros:
        if (registro["numero_licitacion"].strip().casefold() == numero
                and registro["entidad"].strip().casefold() == entidad):
            raise ValueError("Ya existe esa licitación para la misma entidad.")

    nuevo = {
        "id": siguiente_id(registros),
        "numero_licitacion": datos["numero_licitacion"].strip(),
        "entidad": datos["entidad"].strip(),
        "objeto": datos["objeto"].strip(),
        "fecha_limite": datos["fecha_limite"],
        "monto": float(datos["monto"]),
        "responsable": datos["responsable"].strip(),
        "anexos_pdf": datos.get("anexos_pdf", "").strip(),
        "estado": datos.get("estado", "Pendiente"),
    }
    registros.append(nuevo)
    guardar_licitaciones(registros)
    return nuevo


def listar_licitaciones():
    return cargar_licitaciones()


def buscar_licitaciones(termino):
    texto = termino.strip().casefold()
    registros = cargar_licitaciones()
    return [
        r for r in registros
        if texto in r["id"].casefold()
        or texto in r["numero_licitacion"].casefold()
        or texto in r["entidad"].casefold()
    ]


def listar_por_vencimiento():
    registros = cargar_licitaciones()
    return sorted(registros, key=lambda r: date.fromisoformat(r["fecha_limite"]))


def generar_ficha_control(codigo):
    for registro in cargar_licitaciones():
        if registro["id"].casefold() == codigo.strip().casefold():
            return registro
    return None
