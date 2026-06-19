import telebot
from telebot import types
import random
import re
import database  # Importamos nuestro módulo de base de datos

# Reemplaza con tu Token real que te dio BotFather
TOKEN = "8993166335:AAF8VobYWD2hVfWb4ZnDtGvkcKbNZNyJKJM"
bot = telebot.TeleBot(TOKEN)

# Inicializamos la base de datos al encender el bot (crea la tabla si no existe)
database.inicializar_bd()

# Diccionario para controlar los estados y datos temporales de cada usuario
# Estructura: { chat_id: { "estado": "PASO", "cuit": "...", "razon_social": "...", "email": "..." } }
user_states = {}

# Expresión regular sencilla para validar el formato de correo electrónico
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# ==================== FUNCIONES DE CONTROL DE ESTADOS ====================

def obtener_datos_usuario(chat_id):
    """Inicializa la sesión temporal si el usuario escribe por primera vez."""
    if chat_id not in user_states:
        user_states[chat_id] = {
            "estado": "INICIO",
            "cuit": None,
            "razon_social": None,
            "email": None
        }
    return user_states[chat_id]

def reiniciar_usuario(chat_id):
    """Limpia los datos temporales al finalizar o cancelar el proceso."""
    if chat_id in user_states:
        del user_states[chat_id]

# ==================== COMANDO DE INICIO (/START) ====================

@bot.message_handler(commands=['start'])
def comando_start(message):
    chat_id = message.chat.id
    reiniciar_usuario(chat_id)  # Aseguramos un inicio limpio
    
    # Ponemos al usuario en estado de espera de CUIT
    datos = obtener_datos_usuario(chat_id)
    datos["estado"] = "ESPERANDO_CUIT"
    
    bot.send_message(
        chat_id, 
        "Bienvenido al sistema de registro de Logística Express S.A.\n\n"
        "Para iniciar el trámite, por favor ingrese su número de CUIT (solo números, sin guiones ni espacios):"
    )

# ==================== MANEJADOR PRINCIPAL DE MENSAJES ====================

@bot.message_handler(func=lambda m: True)
def procesar_conversacion(message):
    chat_id = message.chat.id
    texto_usuario = message.text.strip()
    datos = obtener_datos_usuario(chat_id)
    estado_actual = datos["estado"]

    # --- PASO 1: Procesar CUIT ---
    if estado_actual == "ESPERANDO_CUIT":
        # Robustez (Camino infeliz): Validamos que sean exactamente 11 números
        if not texto_usuario.isdigit() or len(texto_usuario) != 11:
            bot.send_message(chat_id, "El CUIT debe contener exactamente 11 dígitos numéricos. Intente nuevamente:")
            return
        
        # Validamos contra la Base de Datos real
        if database.existe_cuit(texto_usuario):
            bot.send_message(chat_id, "El CUIT ingresado ya se encuentra registrado en nuestro sistema. El proceso ha finalizado.")
            reiniciar_usuario(chat_id)
            return
        
        # CUIT válido y libre: Guardamos temporalmente y avanzamos
        datos["cuit"] = texto_usuario
        datos["estado"] = "ESPERANDO_RAZON_SOCIAL"
        bot.send_message(chat_id, "CUIT disponible.\n\nPor favor, ingrese la Razón Social de su empresa:")

    # --- PASO 2: Procesar Razón Social ---
    elif estado_actual == "ESPERANDO_RAZON_SOCIAL":
        if len(texto_usuario) < 3:
            bot.send_message(chat_id, "La Razón Social ingresada es muy corta. Ingrese una válida:")
            return
        
        datos["razon_social"] = texto_usuario
        datos["estado"] = "ESPERANDO_EMAIL"
        bot.send_message(chat_id, "Razón Social registrada.\n\nIngrese la dirección de correo electrónico de contacto:")

    # --- PASO 3: Procesar Email ---
    elif estado_actual == "ESPERANDO_EMAIL":
        # Robustez (Camino infeliz): Validación de regex de correo
        if not re.match(EMAIL_REGEX, texto_usuario):
            bot.send_message(chat_id, "El correo ingresado no es válido (ejemplo: contacto@empresa.com). Reintente:")
            return
        
        datos["email"] = texto_usuario
        datos["estado"] = "ESPERANDO_CONFIRMACION"
        
        # Armamos botones rápidos (SI / NO) para facilitar la respuesta del usuario
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('SÍ', 'NO')
        
        # Mostramos resumen (tarea "Mostrar resumen datos" del BPMN)
        resumen = (
            "Resumen de datos ingresados:\n\n"
            f"• CUIT: {datos['cuit']}\n"
            f"• Razón Social: {datos['razon_social']}\n"
            f"• Email: {datos['email']}\n\n"
            "¿Confirma que los datos son correctos?"
        )
        bot.send_message(chat_id, resumen, parse_mode="Markdown", reply_markup=markup)

    # --- PASO 4: Procesar Confirmación ---
    elif estado_actual == "ESPERANDO_CONFIRMACION":
        opcion = texto_usuario.upper()
        
        if opcion == 'SÍ':
            # Generamos un ID de trámite único (ej: REG-1234)
            id_tramite = f"REG-{random.randint(1000, 9999)}"
            
            # Guardamos definitivamente en la base de datos sqlite
            exito = database.registrar_proveedor(
                cuit=datos["cuit"],
                razon_social=datos["razon_social"],
                email=datos["email"],
                id_tramite=id_tramite
            )
            
            if exito:
                bot.send_message(
                    chat_id, 
                    f"¡Alta completada exitosamente!\n\n"
                    f"Su número de trámite de seguimiento es: **{id_tramite}**\n"
                    "Su estado actual es PENDIENTE de verificación administrativa.",
                    parse_mode="Markdown",
                    reply_markup=types.ReplyKeyboardRemove()  # Quitamos los botones
                )
            else:
                bot.send_message(chat_id, "Ocurrió un problema al guardar los datos. Intente de nuevo más tarde.", reply_markup=types.ReplyKeyboardRemove())
                
            reiniciar_usuario(chat_id)
            
        elif opcion == 'NO':
            # Según tu diagrama BPMN, si no confirma, vuelve al inicio
            bot.send_message(
                chat_id, 
                "El registro ha sido cancelado. Volviendo al inicio del formulario...",
                reply_markup=types.ReplyKeyboardRemove()
            )
            # Re-enviamos el paso inicial de forma automática
            reiniciar_usuario(chat_id)
            comando_start(message)
            
        else:
            bot.send_message(chat_id, "Por favor, seleccione SÍ o NO usando los botones disponibles.")

# ==================== INICIO DEL POLLING ====================
if __name__ == "__main__":
    print("El bot de Logística Express se está ejecutando...")
    bot.infinity_polling()