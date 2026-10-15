from datetime import date


def texto_obligatorio(valor, nombre):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{nombre}' es obligatorio.")
    return valor.strip()


def validar_fecha_limite(fecha_texto):
    try:
        fecha = date.fromisoformat(fecha_texto)
    except (TypeError, ValueError):
        raise ValueError("La fecha límite debe tener el formato AAAA-MM-DD.")
    return fecha


def validar_monto(monto):
    try:
        valor = float(monto)
    except (TypeError, ValueError):
        raise ValueError("El monto debe ser numérico.")
    if valor < 0:
        raise ValueError("El monto no puede ser negativo.")
    return valor


def validar_licitacion(datos):
    campos = ["numero_licitacion", "entidad", "objeto", "responsable"]
    for campo in campos:
        texto_obligatorio(datos.get(campo), campo)
    validar_fecha_limite(datos.get("fecha_limite"))
    validar_monto(datos.get("monto"))
    anexos = datos.get("anexos_pdf", "").strip()
    if anexos:
        rutas = [ruta.strip() for ruta in anexos.split(";") if ruta.strip()]
        no_pdf = [ruta for ruta in rutas if not ruta.lower().endswith(".pdf")]
        if no_pdf:
            raise ValueError("Los anexos deben ser archivos con extensión .pdf.")
    return True
