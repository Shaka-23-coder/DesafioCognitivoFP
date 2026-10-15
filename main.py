from datetime import datetime
from negocio import (
    registrar_licitacion, listar_licitaciones, buscar_licitaciones,
    generar_ficha_control, listar_por_vencimiento
)
from persistencia import cargar_licitaciones

FECHA_FORMATO = "%Y-%m-%d"


def pedir_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El campo no puede estar vacío.")


def pedir_fecha(mensaje):
    while True:
        valor = input(mensaje).strip()
        try:
            fecha = datetime.strptime(valor, FECHA_FORMATO).date()
            return fecha.isoformat()
        except ValueError:
            print("Fecha inválida. Usa el formato AAAA-MM-DD, por ejemplo 2026-12-31.")


def pedir_monto():
    while True:
        try:
            monto = float(input("Monto de la oferta (S/): ").strip().replace(",", "."))
            if monto < 0:
                print("El monto no puede ser negativo.")
                continue
            return monto
        except ValueError:
            print("Ingresa un monto numérico válido.")


def registrar():
    print("\n--- Registrar licitación ---")
    licitacion = {
        "numero_licitacion": pedir_texto("Número/código de licitación: "),
        "entidad": pedir_texto("Entidad convocante: "),
        "objeto": pedir_texto("Objeto de contratación: "),
        "fecha_limite": pedir_fecha("Fecha límite (AAAA-MM-DD): "),
        "monto": pedir_monto(),
        "responsable": pedir_texto("Analista responsable: "),
        "anexos_pdf": input("Rutas de archivos PDF (separadas por ;, opcional): ").strip(),
        "estado": "Pendiente",
    }
    try:
        creado = registrar_licitacion(licitacion)
        print(f"\nRegistro guardado. Código interno: {creado['id']}")
    except ValueError as error:
        print(f"\nNo se pudo registrar: {error}")


def mostrar_registros(registros):
    if not registros:
        print("No se encontraron licitaciones.")
        return
    print("\nID | N.º licitación | Entidad | Fecha límite | Monto | Estado")
    print("-" * 88)
    for r in registros:
        print(f"{r['id']} | {r['numero_licitacion']} | {r['entidad']} | "
              f"{r['fecha_limite']} | S/ {r['monto']:.2f} | {r['estado']}")


def buscar():
    termino = pedir_texto("Buscar por código interno, número o entidad: ")
    mostrar_registros(buscar_licitaciones(termino))


def ficha():
    codigo = pedir_texto("Código interno del expediente (ej. LIC-0001): ")
    registro = generar_ficha_control(codigo)
    if not registro:
        print("No existe un expediente con ese código.")
        return
    print("\n--- FICHA DE CONTROL DEL EXPEDIENTE ---")
    for clave, valor in registro.items():
        etiqueta = clave.replace("_", " ").capitalize()
        print(f"{etiqueta}: {valor}")


def menu():
    while True:
        print("""
===== SISTEMA DE GESTIÓN DE LICITACIONES =====
1. Registrar licitación
2. Listar todas las licitaciones
3. Buscar licitación
4. Ver licitaciones ordenadas por vencimiento
5. Generar ficha de control en pantalla
0. Salir
""")
        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            registrar()
        elif opcion == "2":
            mostrar_registros(listar_licitaciones())
        elif opcion == "3":
            buscar()
        elif opcion == "4":
            mostrar_registros(listar_por_vencimiento())
        elif opcion == "5":
            ficha()
        elif opcion == "0":
            print("Datos guardados. Hasta luego.")
            break
        else:
            print("Opción inválida. Elige una opción del menú.")


if __name__ == "__main__":
    # Carga inicial para comprobar que el archivo de datos se puede leer.
    cargar_licitaciones()
    menu()
