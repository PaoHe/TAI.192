from fastapi import FastAPI,HTTPException, Depends  
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from modelsPydantic import modeloUsuario, modeloAuth
from genToken import createToken
from middlewares import BearerJWT
from BD.conexion import Session,engine,Base
from models.modelsDB import User

app = FastAPI(
    title='Mi Primer API 192',
    description='Paola',
    version='1.0.1'
)

Base.metadata.create_all(bind=engine)



usuarios = [
    {"id": 1, "nombre": "Mario", "edad": 21, "correo":"example@gmail.com"},
    {"id": 2, "nombre": "Gelipe", "edad": 20, "correo":"example2@gmail.com"},
    {"id": 3, "nombre": "Alonso", "edad": 22, "correo":"example3@gmail.com"},
    {"id": 4, "nombre": "Mariano", "edad": 23, "correo":"example4@gmail.com"}
]


# Endpoint home
@app.get('/', tags=['Hola Mundo'])
def home():
    return {'hello': 'world FastAPI'}

# Endpoint autenticación
@app.post('/auth',  tags=['Autentificación'])
def login(autorizacion: modeloAuth):
    if autorizacion.email == "mario@gmail.com" and autorizacion.passw == "123456789":
        token:str = createToken(autorizacion.model_dump())
        print(token)
        return JSONResponse(content=token)
    else:
        return {"Aviso": "Credenciales incorrectas"}


# Endpoint CONSULTA TODOS
@app.get("/todoUsuarios", tags=["Operaciones CRUD"])
def leer_usuarios():
    db = Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content=jsonable_encoder(consulta))
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={"message": "Error al Consultar",
                            "Exception":str(e)})
    finally:
        db.close()


#Endpoint buscar por id
@app.get('/usuario/{id}', tags=["Operaciones CRUD"])
def buscarUno(id: int):
    db = Session()
    try:
        consultauno = db.query(User).filter(User.id == id).first()

        if not consultauno:
            return JSONResponse(status_code=404, content={"mensaje": "Usuario no encontrado"})

        return JSONResponse(content=jsonable_encoder(consultauno))

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "mensaje": "Error al consultar",
                "excepcion": str(e)
            }
        )

    finally:
        db.close()

#endpoint Agregar nuevos
@app.post('/usuario/', response_model= modeloUsuario, tags=['Operaciones CRUD'])
def agregarUsuario(usuario: modeloUsuario):
    db = Session()
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code=201,
                            content={"message": "Usuario Guardado",
                            "usuario": usuario.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500,
                            content={"message": "Error al Guardar al Usuario",
                            "Exception":str(e)})
    finally:
        db.close()

# Endpoint Actualizar Usuarios
@app.put('/usuario/{id}', response_model= modeloUsuario, tags=['Operaciones CRUD'])
def actualizarUsuario(id:int, usuarioActualizado:modeloUsuario):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        for key, value in usuarioActualizado.model_dump().items():
            setattr(usuario, key, value)
        
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Usuario actualizado correctamente", "usuario": jsonable_encoder(usuario)})
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al actualizar el usuario", "Exception": str(e)})
    
    finally:
        db.close()
        
#endpoint Eliminar Usuarios
@app.delete('/usuario/{id}', tags=['Operaciones CRUD'])
def eliminarUsuario(id:int):
    db = Session()
    try:
        usuario = db.query(User).filter(User.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        db.delete(usuario)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Usuario eliminado correctamente"})
    
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"message": "Error al eliminar el usuario", "Exception": str(e)})
    
    finally:
        db.close()