# API REST - Servicios de Agua y Drenaje

API REST modular y profesional desarrollada con **Python** y **FastAPI** para la modernización de la gestión de clientes, lecturas de consumo de agua, tarifas base y reportes de facturación de Servicios de Agua y Drenaje.

Proyecto desarrollado para el **Examen del 2.º Parcial**.

---
## Tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI
* **Validación de Datos:** Pydantic (Modelos DTO y validación de esquemas)
* **Servidor ASGI:** Uvicorn
* **Documentación Interactiva:** Swagger UI y ReDoc
* **Persistencia:** Almacenamiento volátil en memoria RAM (estructuras nativas de Python)  

---
## Estructura del Proyecto
El proyecto sigue una arquitectura limpia basada en separación de responsabilidades (*Separation of Concerns*):

```
api-agua-y-drenaje/

├── venv/                 # Entorno virtual aislado (ignorado en Git)

├── .gitignore            # Exclusión de archivos temporales y entorno

├── requirements.txt      # Lista de dependencias del proyecto

├── schemas.py            # Modelos de datos y validaciones con Pydantic

├── database.py           # Estado y persistencia de datos en memoria RAM

├── main.py               # Configuración de FastAPI y endpoints de la API

└── README.md             # Instrucciones de despliegue y documentación

```

## Instrucciones para Ejecutar el Proyecto

1. **Clonar el repositorio**

```
git clone [https://github.com/05AP/api-agua-y-drenaje.git](https://github.com/05AP/api-agua-y-drenaje.git)

cd api-agua-y-drenaje
```

2. **Crear y activar el entorno virtual**

Windows (PowerShell):
```
python -m venv venv

.\venv\Scripts\Activate.ps1
```

Linux / macOS / Git Bash:
```
python3 -m venv venv

source venv/bin/activate
```

3. **Instalar dependencias**

```
pip install -r requirements.txt
```

4. **Iniciar el servidor de desarrollo**

```
uvicorn main:app --reload
```

El servidor quedará disponible en http://127.0.0.1:8000.

5. **Documentación interactiva (Swagger)**

Accede desde el navegador para realizar pruebas interactivas de las operaciones:
- Swagger UI: http://127.0.0.1:8000/docs

---
## Autor

- **Nombre**: Alan Emiliano Palomo Plata
- **Matricula:** 2048459
- **Materia:** Desarrollo Web: Tecnologías Servidor
- **Fecha:** 10/13/2026