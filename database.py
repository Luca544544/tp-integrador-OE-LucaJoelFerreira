import sqlite3

DATABASE_NAME = "proveedores.db"

def inicializar_bd():
    """Crea la base de datos y la tabla de proveedores si no existen."""
    conexion = sqlite3.connect(DATABASE_NAME)
    cursor = conexion.cursor()
    
    # Creamos la tabla exactamente con las variables de nuestro Diccionario de Datos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            cuit TEXT UNIQUE NOT NULL,
            razon_social TEXT NOT NULL,
            email TEXT NOT NULL,
            id_tramite TEXT UNIQUE NOT NULL,
            estado_registro TEXT DEFAULT 'PENDIENTE'
        )
    """)
    
    conexion.commit()
    conexion.close()
    print("Base de datos inicializada correctamente.")

def existe_cuit(cuit):
    """Verifica si un CUIT ya está registrado en la base de datos."""
    conexion = sqlite3.connect(DATABASE_NAME)
    cursor = conexion.cursor()
    
    cursor.execute("SELECT 1 FROM proveedores WHERE cuit = ?", (cuit,))
    resultado = cursor.fetchone()
    
    conexion.close()
    return resultado is not None  # Retorna True si existe, False si no

def registrar_proveedor(cuit, razon_social, email, id_tramite):
    """Guarda un nuevo proveedor en la base de datos."""
    try:
        conexion = sqlite3.connect(DATABASE_NAME)
        cursor = conexion.cursor()
        
        cursor.execute("""
            INSERT INTO proveedores (cuit, razon_social, email, id_tramite)
            VALUES (?, ?, ?, ?)
        """, (cuit, razon_social, email, id_tramite))
        
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al registrar en la base de datos: {e}")
        return False