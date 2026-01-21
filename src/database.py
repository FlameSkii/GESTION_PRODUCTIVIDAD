import sqlite3
from .modelos import Tarea, Proyecto
import os

DATABASE_NAME = "tareas.db"

def get_connection():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn

def crear_tablas():
    """Crea las tablas necesarias en la base de datos si no existen."""
    conn = get_connection()
    cursor = conn.cursor()

# Tabla de proyectos

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            fecha_inicio TEXT,
            estado TEXT
        )
    ''')

# Tabla de tareas

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_creacion TEX,
            fecha_limite TEXT,
            prioridad TEXT,
            estado TEXT,
            proyecto_id INTEGER,
            FOREIGN KEY (proyecto_id) REFERENCES proyectos (id)
        )
    ''')

try:
    cursor.execute(
        "INSERT INTO proyectos (id, nombre, descripcion, estado) VALUES (0, 'Tareas Generales', 'Tareas sin clasificar', 'Activo')")
except sqlite3.IntegrityError:
    pass  # El proyecto ya existe, no hacer nada

conn.commit()
conn.close()

class DBManager:

    def __init__(self):
        crear_tablas()

    def crear_tarea(self, tarea: Tarea) -> Tarea:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, fecha_creacion, fecha_limite, prioridad, estado, proyecto_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tarea._titulo, tarea._descripcion, tarea._fecha_creacion,
              tarea._fecha_limite, tarea._prioridad, tarea._estado, tarea._proyecto_id))

        tarea.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return tarea

def obtener_proyectos(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM proyectos')
        filas = cursor.fetchall()
        conn.close()

        proyectos = [
            Proyecto(nombre=fila['nombre'], descripcion=fila['descripcion'], id=fila['id'], estado=fila['estado'])
            for fila in filas
        ]
        return proyectos

def obtener_tareas(self, estado = None):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = 'SELECT * FROM tareas'
    params = []

    if estado:
        sql += ' WHERE estado = ?'
        params.append(estado)

    sql += ' ORDER BY fecha_limite ASC'

    cursor.execute(sql, params)
    filas = cursor.fetchall()
    conn.close()

    tareas = []

    for fila in filas:
        t = Tarea(
            titulo=fila['titulo'],
            fecha_limite=fila['fecha_limite'],
            prioridad=fila['prioridad'],
            proyecto_id=fila['proyecto_id'],
            descripcion=fila['descripcion'],
            id=fila['id'],
            estado=fila['estado'],
        )
        tareas.append(t)
    return tareas

if __name__ == "__main__":
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
        print(f"Base de datos {DATABASE_NAME} eliminada.")

    crear_tablas()
    print(
        f"Base de datos {DATABASE_NAME} y tablas inicializadas correctamente."
    )

# Prueba del CRUD

manager = DBManager()
tarea_prueba = Tarea(
    titulo="Completar ejercicio de CRUD", 
    fecha_limite="2025-10-30",
    prioridad="Alta",
    proyecto_id=0,
    descripcion="Implementar el módulo database.py."
)
tarea_creada = manager.crear_tarea(tarea_prueba)
print(f"Tarea creada y ID asignado: {tarea_creada.id}")