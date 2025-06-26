# Pruebas de Aceptación con Behave

Este repositorio contiene la implementación de pruebas de aceptación para un proyecto simple, utilizando la herramienta **Behave**.

## Requisitos Previos

- Python instalado (versión utilizada: 3.11)
- pip actualizado

## Instalación

Instala las dependencias necesarias ejecutando:

```bash
pip install -r requirements.txt
```

## Preparación de la Base de Datos

Crear la base de datos ejecutando:

```bash
python crear_db.py
```

## Ejecución del Servidor

Iniciar el servidor con el siguiente comando:

```bash
python main.py
```

## Ejecución de Pruebas de Aceptación

Para ejecutar las pruebas de aceptación, se deben utilizar los siguientes archivos feature:

- `crear_serie.feature`
- `asignar_grupos.feature`
- `subir_solucion.feature`
- `registro_usuario.feature`

Estas pruebas cubren las siguientes Historias de Usuario (HU):

- **Como profesor, quiero crear y definir nuevas series de ejercicios, y poder asignarlas a los grupos que superviso, para organizar actividades para mis estudiantes.**
- **Como profesor, quiero asignar estudiantes a grupos existentes para que puedan resolver series de ejercicios.**
- **Como estudiante, quiero poder subir mi solucion a un ejercicio dado para que el profesor pueda evaluarme**
- **Como usuario nuevo, quiero registrarme en el sistema, para poder acceder a las funcionalidades según mi rol asignado (Estudiante/Supervisor).**


Cada una de estas implementaciones está documentada paso a paso en los commits de las ramas `sam`, `Juan`, `cristobal` y `pablo`:
- En la rama **sam** se encuentra la implementación de crear y asignar series.
- En la rama **Juan** se encuentra la implementación de asignar estudiantes a grupos.
- En la rama **cristobal** se encuentra la implementación de subir_solucion.
- En la rama **pablo** se encuentra la implementación de registro_usuario

Se pueden recorrer los commits de estas ramas para ver el proceso de desarrollo y ejecución de pruebas usando Behave.

Para ejecutar las pruebas, se utiliza el siguiente comando:

```bash
behave features/nombre_archivo.feature
```

Se debe reemplazar *nombre_archivo* por el archivo .feature a testear.

--- No es necesario tener el servidor en ejecución para correr Behave ---
