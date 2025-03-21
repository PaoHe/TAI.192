from fastapi import FastAPI,HTTPException, Depends  
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from middlewares import BearerJWT
from BD.conexion import Session,engine,Base
from models.modelsDB import User

app = FastAPI(
    title="Mi Primer Parcial 192",
    description="Paola",
    version="1.0.1"
)

Base.metadata.create_all(bind = engine)

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

# Endpoint Autenticación
@app.post('/auth', tags= ['Autentificacion'])
def login(autirizacion:modeloAuth):
    if autirizacion.email == 'pao@example.com' and autirizacion.passw == '123456789':
        token:str = createToken(autirizacion.model_dump())
        print(token)
        return JSONResponse(content = token)
    else:
        return{"Aviso": "Usuario sin autorizacion"}

#Endpoint CONSULTA TODOS
@app.get('/todosUsuarios',dependencies= [Depends(BearerJWT())], response_model=List[modeloUsuario], tags=['Operaciónes CRUD'])
def leerUsuarios():
    return usuarios

#Endpoint AGREGAR NUEVOS
@app.post('/usuario', response_model= modeloUsuario, tags=['Operaciónes CRUD'])
def agregarUsuario(usuario:modeloUsuario):
    db= Session()
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code = 201,
                            content={"message":"Usuario Guardado",
                            "usuario":usuario.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code = 500,
                            content={"message":"Error al Gueardar Usuario",
                                     "Exception":str(e)})
    finally:
        db.close()


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

