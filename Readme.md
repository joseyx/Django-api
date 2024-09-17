Aquí tienes el `README.md` actualizado con instrucciones sobre cómo acceder al shell de PostgreSQL para crear la base de datos:


# Proyecto Django con PostgreSQL

Este proyecto es una aplicación web construida con Django y PostgreSQL. A continuación, se detallan los pasos para instalar y configurar el proyecto en un entorno local.

## Requisitos

- Python 3.8 o superior
- PostgreSQL
- Virtualenv (opcional pero recomendado)

## Instalación

### 1. Clonar el repositorio

```bash
git clone [Enlace del repositorio]
```

### 2. Crear y activar un entorno virtual

Es recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
python -m venv env
env\Scripts\activate
```

### 3. Instalar las dependencias

Instala las dependencias del proyecto usando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Asegúrate de tener PostgreSQL instalado y en funcionamiento. Luego, accede al shell de PostgreSQL y crea una base de datos para el proyecto.

```bash
psql -U postgres
```

Dentro del shell de PostgreSQL, ejecuta el siguiente comando:

```sql
CREATE DATABASE nombre_de_tu_base_de_datos;
```

### 5. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables de entorno:

```env
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario_de_postgres
DB_PASSWORD=tu_contraseña_de_postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Aplicar las migraciones

Ejecuta las migraciones para configurar la base de datos:

```bash
python manage.py migrate
```

### 7. Crear un superusuario

Crea un superusuario para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

### 8. Ejecutar el servidor de desarrollo

Inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
```

Ahora puedes acceder a la aplicación en `http://localhost:8000`.
