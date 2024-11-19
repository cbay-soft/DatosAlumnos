from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Función para conectar a la base de datos SQLite
def conectar_db():
    conn = sqlite3.connect("estudiantes.db")
    return conn

# Crear la tabla de estudiantes
@app.on_event("startup")
def startup():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            carrera TEXT,
            semestre INTEGER,
            materias TEXT,
            horarios TEXT
        )
    """)
    conn.commit()
    conn.close()

# Modelo para los datos de los estudiantes
class Estudiante(BaseModel):
    nombre: str
    carrera: str
    semestre: int
    materias: str
    horarios: str

# Endpoint para ingresar datos de estudiantes
@app.post("/ingresar/")
def ingresar_datos(estudiante: Estudiante):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO estudiantes (nombre, carrera, semestre, materias, horarios)
        VALUES (?, ?, ?, ?, ?)
    """, (estudiante.nombre, estudiante.carrera, estudiante.semestre, estudiante.materias, estudiante.horarios))
    conn.commit()
    conn.close()
    return {"message": "Datos ingresados correctamente"}

# Contraseña de consulta
ADMIN_PASSWORD = "admin123"

# Endpoint para consultar los datos de los estudiantes
@app.post("/consultar/")
def consultar_datos(password: str = Form(...)):
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="Contraseña incorrecta")
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    estudiantes = cursor.fetchall()
    conn.close()

    datos = []
    for estudiante in estudiantes:
        datos.append({
            "nombre": estudiante[1],
            "carrera": estudiante[2],
            "semestre": estudiante[3],
            "materias": estudiante[4],
            "horarios": estudiante[5]
        })
    return {"estudiantes": datos}
