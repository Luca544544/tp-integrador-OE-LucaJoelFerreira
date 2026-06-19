import sqlite3

TRAMITE_A_APROBAR = input("Ingrese el trámite a aprobar. Todo en mayuscula, con guion entre letras y numero. \nEjemplo de entrada válida: REG-2806: ")

try    :
    # Validamos que el trámite no esté vacío
    if not TRAMITE_A_APROBAR.strip():
        raise ValueError("El trámite no puede estar vacío. Por favor, ingrese un trámite válido.")
    if len(TRAMITE_A_APROBAR) < 5:
        raise ValueError("El trámite ingresado es demasiado corto. Ingrese un trámite válido.")
except ValueError as ve:
    print(f"Error: {ve}")
    exit(1)  # Salimos del programa con un código de error

# Reemplaza con el trámite que quieres aprobar

conexion = sqlite3.connect("proveedores.db")
cursor = conexion.cursor()

# Ejecutamos la actualización (UPDATE) en SQL
cursor.execute(
    "UPDATE proveedores SET estado_registro = 'APROBADO' WHERE id_tramite = ?", 
    (TRAMITE_A_APROBAR,)
)

conexion.commit()
print(f"Trámite {TRAMITE_A_APROBAR} actualizado a APROBADO con éxito.")

conexion.close()