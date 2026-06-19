import sqlite3

conexion = sqlite3.connect("proveedores.db")
cursor = conexion.cursor()

# Consultamos todos los proveedores guardados
cursor.execute("SELECT * FROM proveedores")
filas = cursor.fetchall()

print("--- REGISTROS EN LA BASE DE DATOS ---")
for fila in filas:
    print(f"ID: {fila[0]} | CUIT: {fila[1]} | Razón Social: {fila[2]} | Email: {fila[3]} | Trámite: {fila[4]} | Estado: {fila[5]}")

conexion.close()