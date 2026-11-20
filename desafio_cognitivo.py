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

# ==========================================
# MÓDULO 3: PERSISTENCIA EN ARCHIVOS
# ==========================================


def guardar_expedientes_en_archivo(expedientes):
    """
    Guarda de forma permanente la información de expedientes en disco.
    """
    try:
        with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
            for exp in expedientes:
                linea = (
                    f"{exp['codigo']}|{exp['num_lic']}|{exp['entidad']}|"
                    f"{exp['objeto']}|{exp['fecha_limite']}|{exp['monto']}|"
                    f"{exp['analista']}|{exp['estado']}\n"
                )
                f.write(linea)
    except OSError as e:
        print(f"Error al guardar datos: {e}")


def cargar_expedientes_desde_archivo():
    """
    Carga los expedientes existentes al iniciar el programa.
    """
    expedientes = []
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split("|")
                    if len(datos) == 8:
                        expedientes.append({
                            "codigo": datos[0],
                            "num_lic": datos[1],
                            "entidad": datos[2],
                            "objeto": datos[3],
                            "fecha_limite": datos[4],
                            "monto": float(datos[5]),
                            "analista": datos[6],
                            "estado": datos[7]
                        })
        except ValueError as e:
            print(f"Error al procesar datos: {e}")
    return expedientes

# ==========================================
# MÓDULO 4: INTERFAZ Y CONTROLADOR
# ==========================================


def registrar_expediente(expedientes):
    """Función que permite registrar un nuevo expediente"""
    print("\n--- REGISTRO DE NUEVO EXPEDIENTE ---")
    if len(expedientes) >= MAX_REGISTROS:
        print("Error: Capacidad máxima de memoria alcanzada.")
        return

    num_lic = input("Ingrese N° de Licitación/Convocatoria: ").strip()
    entidad = input("Ingrese nombre de la entidad convocante: ").strip()
    objeto = input("Ingrese materia/objeto de la licitación: ").strip()

    while True:
        fecha_limite = input("Ingrese fecha límite (AAAAMMDD): ").strip()
        if validar_fecha(fecha_limite):
            break
        print(
            "Error: La fecha debe tener 8 dígitos y ser igual o posterior "
            "a la actual."
        )

    while True:
        try:
            monto = float(input("Ingrese monto de la oferta (S/): "))
            break
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")

    analista = input("Ingrese nombre del analista responsable: ").strip()

    nuevo_codigo = generar_codigo_correlativo(len(expedientes) + 1)
    nuevo_expediente = {
        "codigo": nuevo_codigo,
        "num_lic": num_lic,
        "entidad": entidad,
        "objeto": objeto,
        "fecha_limite": fecha_limite,
        "monto": monto,
        "analista": analista,
        "estado": "EN PROCESO"
    }

    expedientes.append(nuevo_expediente)
    guardar_expedientes_en_archivo(expedientes)
    print(f"¡Expediente registrado con éxito! Código asignado: {nuevo_codigo}")


def buscar_expediente(expedientes):
    """Función para buscar expediente con el código correlativo"""
    print("\n--- BÚSQUEDA DE EXPEDIENTE ---")
    if not expedientes:
        print("No hay expedientes registrados.")
        return

    codigo_buscado = input(
        "Ingrese el código correlativo a buscar (ej. SEG-2026-1): "
    ).strip().upper()
    encontrado = False

    for exp in expedientes:
        if exp["codigo"].upper() == codigo_buscado:
            print("\n=============================")
            print("   EXPEDIENTE ENCONTRADO")
            print("=============================")
            print(f"Código interno:  {exp['codigo']}")
            print(f"N° Licitación:   {exp['num_lic']}")
            print(f"Entidad:         {exp['entidad']}")
            print(f"Objeto/Materia:  {exp['objeto']}")
            print(f"Fecha Límite:    {exp['fecha_limite']}")
            print(f"Monto Oferta:    S/ {exp['monto']:.2f}")
            print(f"Analista:        {exp['analista']}")
            print(f"Estado:          {exp['estado']}")
            print("=============================")
            encontrado = True
            break

    if not encontrado:
        print(
            "Error: No se encontró ningún expediente con el código ingresado."
        )


def listar_expedientes_ordenados(expedientes):
    """Función que ordena los expedientes y lo muestra"""
    print("\n--- LISTADO DE LICITACIONES ORDENADAS POR VENCIMIENTO ---")
    if not expedientes:
        print("No hay expedientes registrados.")
        return

    ordenar_por_fecha_vencimiento(expedientes)
    for exp in expedientes:
        print(
            f"[{exp['fecha_limite']}] {exp['codigo']} - {exp['entidad']} "
            f"(Lic. {exp['num_lic']}) | Estado: {exp['estado']}"
        )


def generar_ficha_control(expedientes):
    """Función que genera una ficha de control"""
    print("\n--- FICHAS DE CONTROL DE EXPEDIENTES ---")
    if not expedientes:
        print("No hay expedientes registrados.")
        return

    for exp in expedientes:
        print(
            f"Ficha {exp['codigo']}: Lic. {exp['num_lic']} | "
            f"Entidad: {exp['entidad']} | Resp: {exp['analista']} | "
            f"Monto: S/ {exp['monto']:.2f}"
        )


def menu_principal():
    """Función que muestra el menú principal con las distintas opciones"""
    expedientes = cargar_expedientes_desde_archivo()

    while True:
        print("\n========================================================")
        print(" SISTEMA DIGITAL DE GESTIÓN DE LICITACIONES - GRUPO SEG ")
        print("========================================================")
        print("1. Registrar nuevo expediente de licitación")
        print("2. Buscar expediente por código correlativo")
        print("3. Listar y ordenar licitaciones por fecha de vencimiento")
        print("4. Generar ficha de control del expediente")
        print("5. Salir del sistema")

        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            registrar_expediente(expedientes)
        elif opcion == "2":
            buscar_expediente(expedientes)
        elif opcion == "3":
            listar_expedientes_ordenados(expedientes)
        elif opcion == "4":
            generar_ficha_control(expedientes)
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    menu_principal()
