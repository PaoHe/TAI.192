from fastapi import HTTPException  
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modeloUsuario
from genToken import createToken
from middlewares import BearerJWT
from BD.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter

routerUsuario = APIRouter()


# Endpoint CONSULTA TODOS
@routerUsuario.get("/todoUsuarios", tags=["Operaciones CRUD"])
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
@routerUsuario.get('/usuario/{id}', tags=["Operaciones CRUD"])
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
@routerUsuario.post('/usuario/', response_model= modeloUsuario, tags=['Operaciones CRUD'])
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
@routerUsuario.put('/usuario/{id}', response_model= modeloUsuario, tags=['Operaciones CRUD'])
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
@routerUsuario.delete('/usuario/{id}', tags=['Operaciones CRUD'])
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