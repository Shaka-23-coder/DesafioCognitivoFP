"""Código principal para el desafio cognitivo"""
# ==========================================
# MÓDULO: VALIDACIONES
# ==========================================


def validar_fecha(fecha):
    """
    Valida que la fecha tenga el formato AAAA-MM-DD y sea una fecha válida
    """
    if len(fecha) != 10:
        return False
    if fecha[4] != "-" or fecha[7] != "-":
        return False
    numeros = fecha[0:4] + fecha[5:7] + fecha[8:10]
    if not numeros.isdigit():
        return False

    anio = int(fecha[0:4])
    mes = int(fecha[5:7])
    dia = int(fecha[8:10])

    if anio < 2000 or mes < 1 or mes > 12:
        return False

    dias = 31
    if mes == 4 or mes == 6 or mes == 9 or mes == 11:
        dias = 30
    elif mes == 2:
        dias = 28
        if anio % 4 == 0:
            if anio % 100 != 0 or anio % 400 == 0:
                dias = 29

    if dia < 1 or dia > dias:
        return False

    return True


def validar_monto(texto):
    """Valida que el monto sea un número positivo"""
    numero = texto.replace(".", ".", 1)
    if numero.isdigit():
        if float(texto) > 0:
            return True
    return False


def validar_anexos(anexos):
    """Valida que los anexos tengan el formato correcto"""
    if anexos.strip() == "":
        return False

    lista = anexos.split(";")
    for nombre in lista:
        nombre = nombre.strip().lower()
        if len(nombre) <= 4 or not nombre.endswith(".pdf"):
            return False

    return True


# ==========================================
# MÓDULO: NEGOCIO
# ==========================================


def siguiente_codigo(lista):
    """
    Genera el siguiente codigo interno para una nueva licitación
    """
    mayor = 0
    for fila in lista:
        numero = int(fila[0][4:])
        if numero > mayor:
            mayor = numero
    return f"LIC-{mayor + 1:04d}"


def registrar_licitacion(numero, entidad, objeto, fecha_registro,
                         fecha_limite, monto, responsable, anexos):
    """
    Registra una nueva licitacion si no existe ya una con el mismo numero
    y entidad.
    """
    lista = cargar_licitaciones()

    for fila in lista:
        if (
            fila[1].lower() == numero.lower()
            and fila[2].lower() == entidad.lower()
        ):
            print("Ya existe esa licitacion para la misma entidad.")
            return ""

    codigo = siguiente_codigo(lista)
    fila = [codigo, numero, entidad, objeto, fecha_registro, fecha_limite,
            str(monto), responsable, anexos, "Pendiente"]
    guardar_licitacion(fila)
    return codigo


def listar_licitaciones():
    """Lista todas las licitaciones registradas"""
    return cargar_licitaciones()


def buscar_licitaciones(termino):
    """Busca licitaciones por codigo, numero o entidad"""
    lista = cargar_licitaciones()
    encontrados = []
    termino = termino.lower()

    for fila in lista:
        if (
            termino in fila[0].lower()
            or termino in fila[1].lower()
            or termino in fila[2].lower()
        ):
            encontrados.append(fila)

    return encontrados


def listar_por_vencimiento():
    """Lista las licitaciones ordenadas por fecha limite"""
    lista = cargar_licitaciones()

    # Metodo burbuja: ordena fechas de menor a mayor.
    for i in range(len(lista) - 1):
        for j in range(len(lista) - 1 - i):
            if lista[j][5] > lista[j + 1][5]:
                auxiliar = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = auxiliar

    return lista


def generar_ficha_control(codigo):
    """Genera la ficha de control de una licitacion por codigo interno"""
    lista = cargar_licitaciones()
    for fila in lista:
        if fila[0].lower() == codigo.lower():
            return fila
    return []


# ==========================================
# MÓDULO: PERSISTENCIA
# ==========================================


def cargar_licitaciones():
    """Carga las licitaciones desde el archivo de texto"""
    lista = []

    # Crea el archivo si todavia no existe.
    with open("licitaciones.txt", "a", encoding="utf-8") as archivo:
        archivo.write("")

    with open("licitaciones.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            fila = linea.strip().split(",")
            if len(fila) == 10:
                lista.append(fila)

    return lista


def guardar_licitacion(fila):
    """Guarda una licitacion en el archivo de texto"""
    linea = ",".join(str(valor) for valor in fila[:10])
    with open("licitaciones.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{linea}\n")


# ==========================================
# MÓDULO 4: INTERFAZ Y MENÚ
# ==========================================


def pedir_texto(mensaje):
    """Pide un texto al usuario y valida que no este vacio ni contenga comas"""
    texto = input(mensaje).strip()
    while texto == "" or "," in texto:
        print("Ingresa un dato valido y sin comas.")
        texto = input(mensaje).strip()
    return texto


def pedir_fecha(mensaje):
    """Pide una fecha al usuario y valida que tenga el formato AAAA-MM-DD"""
    fecha = input(mensaje).strip()
    while not validar_fecha(fecha):
        print("Fecha incorrecta. Ejemplo: 2026-12-31")
        fecha = input(mensaje).strip()
    return fecha


def pedir_monto():
    """Pide un monto al usuario y valida que sea un numero positivo"""
    monto = input("Monto de la oferta (S/): ").strip()
    while not validar_monto(monto):
        print("Ingresa un monto numerico mayor que cero. Ejemplo: 1500.50")
        monto = input("Monto de la oferta (S/): ").strip()
    return float(monto)


def pedir_anexos():
    """
    Pide los nombres de los anexos PDF al usuario y valida que
    tengan el formato correcto.
    """
    anexos = input("Nombres de anexos PDF (separados por ;): ").strip()
    while not validar_anexos(anexos):
        print("Ingresa al menos un nombre terminado en .pdf")
        anexos = input("Nombres de anexos PDF (separados por ;): ").strip()
    return anexos


def registrar():
    """Registra una nueva licitacion solicitando los datos al usuario"""
    print("\n--- REGISTRAR LICITACION ---")
    numero = pedir_texto("Numero de licitacion: ")
    entidad = pedir_texto("Entidad convocante: ")
    objeto = pedir_texto("Objeto de contratacion: ")
    fecha_registro = pedir_fecha("Fecha de registro (AAAA-MM-DD): ")
    fecha_limite = pedir_fecha("Fecha limite (AAAA-MM-DD): ")

    if fecha_limite < fecha_registro:
        print("Error: la fecha limite es anterior a la fecha de registro.")
        return

    monto = pedir_monto()
    responsable = pedir_texto("Analista responsable: ")
    anexos = pedir_anexos()
    codigo = registrar_licitacion(
        numero, entidad, objeto, fecha_registro,
        fecha_limite, monto, responsable, anexos
    )

    if codigo != "":
        print(f"Registro exitoso. Codigo interno: {codigo}")


def mostrar_registros(lista):
    """Muestra una lista de licitaciones en formato tabular"""
    if len(lista) == 0:
        print("No se encontraron licitaciones.")
    else:
        print(
            "\nCodigo     Numero          Entidad                   "
            "Fecha limite  Monto       Estado"
        )
        print("-" * 94)
        for fila in lista:
            print(
                f"{fila[0]:<11}{fila[1]:<16}{fila[2]:<26}"
                f"{fila[5]:<14}{float(fila[6]):<12.2f}{fila[9]}"
            )


def buscar():
    """Busca licitaciones por codigo, numero o entidad y las muestra"""
    termino = pedir_texto("Buscar por codigo, numero o entidad: ")
    lista = buscar_licitaciones(termino)
    mostrar_registros(lista)


def ficha():
    """Genera la ficha de control de una licitacion por codigo interno"""
    codigo = pedir_texto("Codigo interno (ejemplo LIC-0001): ")
    fila = generar_ficha_control(codigo)
    if len(fila) == 0:
        print("No se encontro ese expediente.")
    else:
        print("\n--- FICHA DE CONTROL ---")
        print(f"Codigo interno: {fila[0]}")
        print(f"Numero de licitacion: {fila[1]}")
        print(f"Entidad: {fila[2]}")
        print(f"Objeto: {fila[3]}")
        print(f"Fecha de registro: {fila[4]}")
        print(f"Fecha limite: {fila[5]}")
        print(f"Monto: S/ {float(fila[6]):.2f}")
        print(f"Responsable: {fila[7]}")
        print(f"Anexos PDF: {fila[8]}")
        print(f"Estado: {fila[9]}")


def menu():
    """Muestra el menu principal y permite al usuario seleccionar opciones"""
    opcion = ""
    while opcion != "0":
        print("\nSISTEMA DE GESTION DE LICITACIONES - GRUPO SEG")
        print("1. Registrar licitacion")
        print("2. Listar licitaciones")
        print("3. Buscar licitacion")
        print("4. Ordenar por fecha limite")
        print("5. Generar ficha de control")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ")
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
            print("Programa finalizado.")
        else:
            print("Opcion incorrecta.")


if __name__ == "__main__":
    menu()
