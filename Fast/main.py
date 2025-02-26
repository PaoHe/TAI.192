from fastapi import FastAPI,HTTPException
from typing import Optional, List
from models import modeloUsuario

app = FastAPI(
    title="Mi Primer Parcial 192",
    description="Paola",
    version="1.0.1"
)

#BD ficticia
usuarios = [
    {"id": 1, "nombre": "Paola", "edad": 21,"correo":"example@example.com"},
    {"id": 2, "nombre": "Moni", "edad": 51,"correo":"example2@example.com"},
    {"id": 3, "nombre": "Adriana", "edad": 31,"correo":"example3@example.com"},
    {"id": 4, "nombre": "Rodrigo", "edad": 32,"correo":"example4@example.com"}
]

# Endpoint home
@app.get("/")
def home():
    return {"hello": "world FastAPI"}

#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios', response_model=List[modeloUsuario], tags=['Operaciónes CRUD'])
def leerUsuarios():
    return usuarios

#Endpoint AGREGAR NUEVOS
@app.post('/usuario', response_model= modeloUsuario, tags=['Operaciónes CRUD'])
def agregarUsuario(usuario:modeloUsuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
        usuarios.append(usuario)
        return usuario

#Endopoint ACTUALIZAR USUARIO
@app.put('/usuario/{id}',response_model= modeloUsuario, tags=['Operaciónes CRUD'])
def actualizarUsuario(id: int, usuarioActualizado: modeloUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios [index] = usuarioActualizado.model_dump()
            return usuarios[index]
        raise HTTPException(status_code=400, detail="El usuario no existre")

#Endopoint ELIMINAR USUARIO
@app.delete('/usuario/{id}', tags=['Operaciónes CRUD'])
def eliminarUsuario(id: int):   
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"Mensaje": "El usuario ha sido eliminado"}
    return{"Mensaje":"No valido"}

