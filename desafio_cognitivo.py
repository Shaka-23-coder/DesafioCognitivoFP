"""Código principal para el desafio cognitivo"""
import os

# Constantes de configuración
ARCHIVO_DATOS = "expedientes_licitacion.txt"
MAX_REGISTROS = 100

# ==========================================
# MÓDULO 1: VALIDACIONES
# ==========================================


def validar_fecha(fecha_limite_str, fecha_actual_str="20261014"):
    """
    Valida que la fecha límite no sea anterior a la fecha actual.
    Formato esperado: AAAAMMDD
    """
    if len(fecha_limite_str) != 8 or not fecha_limite_str.isdigit():
        return False
    return int(fecha_limite_str) >= int(fecha_actual_str)

# ==========================================
# MÓDULO 2: LÓGICA DE NEGOCIO Y CÓDIGOS
# ==========================================


def generar_codigo_correlativo(numero):
    """
    Genera un identificador único correlativo con formatio SEG-2026-X
    """
    return f"SEG-2026-{numero}"


def ordenar_por_fecha_vencimiento(expedientes):
    """
    Ordena la lista de expedientes de menor a mayor según fecha límite
    Algoritmo de ordenamiento burbuja
    """
    n = len(expedientes)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if (
                int(expedientes[j]['fecha_limite'])
                > int(expedientes[j + 1]['fecha_limite'])
            ):
                expedientes[j], expedientes[j + 1] = (
                    expedientes[j + 1],
                    expedientes[j]
                )
