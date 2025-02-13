from fastapi import FastAPI,HTTPException
from typing import Optional

app = FastAPI(
    title="Mi Primer Parcial 192",
    description="Paola",
    version="1.0.1"
)

usuarios = [
    {"id": 1, "nombre": "Paola", "edad": 21},
    {"id": 2, "nombre": "Moni", "edad": 51},
    {"id": 3, "nombre": "Adriana", "edad": 31},
    {"id": 4, "nombre": "Rodrigo", "edad": 32}
]

# Endpoint home
@app.get("/")
def home():
    return {"hello": "world FastAPI"}

#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios', tags=['Operaciónes CRUD'])
def leerUsuarios():
    return {"Los usuarios registrados son:": usuarios}

#Endpoint AGREGAR NUEVOS
@app.post('/usuario', tags=['Operaciónes CRUD'])
def agregarUsuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(status_code=400, detail="El id ya existe")
        usuarios.append(usuario)
        return usuario

#Endopoint ACTUALIZAR USUARIO
@app.put('/usuario/{id}', tags=['Operaciónes CRUD'])
def actualizarUsuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr["nombre"] = usuario.get("nombre")
            usr["edad"] = usuario.get("edad")
            return usuario
        