# Trabajo Práctico Integrador: Automatización de Procesos (Alta de Proveedores)
## Cátedra: Organización Empresarial
### Tecnicatura Universitaria en Programación - UTN

Este proyecto consiste en la automatización del proceso de **Alta de Proveedores** para la empresa ficticia **Logística Express S.A.** mediante un asistente virtual (Chatbot) integrado en Telegram y conectado a una base de datos relacional SQLite.

El desarrollo implementa una **Máquina de Estados** para gestionar la conversación con el usuario y mecanismos de robustez para controlar posibles errores en el ingreso de datos (Camino Infeliz).

---

## Información Académica

* **Institución:** Universidad Tecnológica Nacional (UTN)
* **Carrera:** Tecnicatura Universitaria en Programación (A Distancia)
* **Materia:** Organización Empresarial
* **Estudiante(s):** 
  * Luca Joel Ferreira
* **Cuerpo de Docentes:**
  * Prof. Gabriela Martínez (titular)
  * Prof. Carolina Bruno, Prof. Mario Raúl López, Prof. Andrea Ramos (adjuntos)

---

## Estructura del Proyecto

El repositorio está organizado de forma modular para separar las responsabilidades de la base de datos, la lógica del bot y las utilidades administrativas:

| Archivo | Descripción |
| :--- | :--- |
| **`main.py`** | Script principal que inicia el bot y ejecuta la lógica de la máquina de estados y validaciones. |
| **`database.py`** | Módulo de persistencia que gestiona la conexión, creación de tablas e inserciones en SQLite. |
| **`proveedores.db`** | Archivo de base de datos relacional SQLite (se genera automáticamente al iniciar el sistema). |
| **`ver_datos.py`** | Script administrativo auxiliar para consultar y listar por consola los proveedores registrados. |
| **`aprobar_proveedor.py`** | Script administrativo para cambiar el estado de un trámite de PENDIENTE a APROBADO. |

---

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado en tu sistema:

* Python 3.8 o superior.
* Gestor de paquetes `pip`.
* Una cuenta de Telegram para interactuar con el bot.

---

## Instrucciones de Instalación y Configuración

Sigue estos pasos para clonar y ejecutar el bot de forma local en tu computadora:

1. Clonar el repositorio
Clona este repositorio en tu máquina local utilizando la terminal:

git clone [LINK_DE_TU_REPOSITORIO_DE_GITHUB]
cd [NOMBRE_DE_LA_CARPETA_DEL_PROYECTO]

2. Instalar las dependencias

Instala la librería oficial de Telegram para Python ejecutando el siguiente
comando:

pip install pyTelegramBotAPI

3. Configurar el Token de Telegram

1.  Habla con @BotFather en Telegram para crear un nuevo bot mediante el comando
    /newbot.
2.  Copia el Token API proporcionado.
3.  Abre el archivo main.py de tu proyecto y reemplaza la variable de la línea 8
    con tu token de acceso:

TOKEN = "[TU_TOKEN_DE_TELEGRAM_AQUÍ]"

## Ejecución del Sistema

**Iniciar el Chatbot**

Para iniciar el bot y la conexión con la base de datos, ejecuta el script
principal en tu consola:

python main.py

Una vez iniciado, abre el chat de tu bot en Telegram y envía el comando /start
para comenzar el flujo de registro de proveedores.

**Herramientas de Administración (Auditoría de Datos)**

Para simular las tareas administrativas que ocurren fuera del chatbot, puedes
utilizar los siguientes scripts auxiliares:

**Visualizar registros de proveedores**

Para ver los datos que se han guardado de manera persistente en proveedores.db,
ejecuta en otra terminal:

python ver_datos.py

**Aprobar un proveedor pendiente**

Para cambiar el estado de un trámite específico de PENDIENTE a APROBADO tras una
validación administrativa de la empresa, ejecuta:

1.  Abre el archivo aprobar_proveedor.py.
2.  Edita la variable TRAMITE_A_APROBAR con el código de trámite que deseas
    validar (ej. REG-8521).
3.  Corre el script en tu terminal:

python aprobar_proveedor.py

---

## Tecnologías Utilizadas

  - Lenguaje: Python
  - Plataforma: Telegram Bot API (Librería pyTelegramBotAPI)
  - Base de Datos: SQLite (Módulo nativo sqlite3 de Python)
  - Control de Versiones: Git & GitHub
  - Modelado de Negocios: BPMN 2.0

