# Prototipo de gestión de licitaciones

Proyecto académico de Fundamentos de Programación. Implementa un prototipo de consola para registrar y consultar expedientes de licitación.

## Requisitos
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

## Límites del prototipo
Este es un prototipo académico. No sube archivos PDF ni comprueba que las rutas existan: guarda las rutas escritas por el usuario. Tampoco se conecta a plataformas oficiales ni presenta ofertas. La fecha límite se valida por formato; el programa no bloquea licitaciones cuya fecha ya pasó. Estas mejoras pueden agregarse si el docente las exige.

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
git remote add origin PEGA_AQUI_LA_URL_DE_TU_REPOSITORIO
git push -u origin main
```

Reemplaza `PEGA_AQUI_LA_URL_DE_TU_REPOSITORIO` por la URL real de tu repositorio. No escribas esa frase literalmente.

## Evidencias para el informe
1. Captura del proyecto abierto en VS Code mostrando los módulos.
2. Captura de la ejecución del menú en la terminal.
3. Captura del registro de una licitación de prueba.
4. Captura de la búsqueda o del listado ordenado por vencimiento.
5. Captura de `licitaciones.json` después de registrar un expediente.
6. Captura de GitHub donde se vean los commits.
7. En el informe, explica que cada commit registra una etapa concreta del desarrollo.

## Ejemplo de prueba
- Número: LP-001-2026
- Entidad: Municipalidad de prueba
- Objeto: Servicio de consultoría
- Fecha límite: 2026-12-31
- Monto: 15000
- Responsable: Ana Torres
- Anexos PDF: (puede dejarse vacío)

Estos datos son ficticios y solo sirven para probar el programa.
