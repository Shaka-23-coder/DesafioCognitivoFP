# Prototipo de gestión de licitaciones

Proyecto académico de Fundamentos de Programación. Implementa un prototipo de consola para registrar y consultar expedientes de licitación.

## Herramientas usadas
- Python 3.10 o superior (no requiere instalar librerías externas).
- Visual Studio Code.
- Git para el control de versiones.
- Cuenta de GitHub para publicar el repositorio.

## Archivos
- `main.py`: menú e interacción con el usuario.
- `validaciones.py`: validación de campos, fechas, montos y extensión PDF.
- `negocio.py`: registro, código correlativo, búsqueda, ficha y ordenamiento.
- `persistencia.py`: lectura y guardado permanente en JSON.
- `licitaciones.json`: se crea automáticamente al registrar la primera licitación.

## Cómo ejecutar
1. Abre esta carpeta en Visual Studio Code.
2. Abre Terminal > New Terminal.
3. Ejecuta `python --version` para comprobar que Python está instalado.
4. Ejecuta `python main.py` (en algunos equipos de Windows funciona `py main.py`).
5. Usa las opciones del menú. Las fechas se ingresan como `AAAA-MM-DD`, por ejemplo `2026-12-31`.
6. Para salir, elige `0`. Los datos quedan guardados en `licitaciones.json`.

## Funciones implementadas
- Registro de licitaciones con código interno correlativo `LIC-0001`, `LIC-0002`, etc.
- Validación de campos obligatorios, fecha y monto.
- Verificación de que las rutas de anexos ingresadas terminen en `.pdf`.
- Prevención de registros duplicados por número de licitación y entidad.
- Persistencia en archivo JSON.
- Búsqueda por código interno, número o entidad.
- Listado ordenado por fecha límite más próxima.
- Ficha de control en pantalla.

## Historial de versiones con Git
Ejecuta estos comandos en la terminal, dentro de esta carpeta:

```bash
git init
git add README.md validaciones.py
git commit -m "Commit 1: crear estructura y validaciones"
git add persistencia.py
git commit -m "Commit 2: implementar persistencia de datos"
git add negocio.py
git commit -m "Commit 3: implementar lógica de licitaciones"
git add main.py
git commit -m "Commit 4: implementar menú y consultas"
```

Luego crea un repositorio vacío en GitHub (sin README ni licencia), copia la URL HTTPS del repositorio y ejecuta:

```bash
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

