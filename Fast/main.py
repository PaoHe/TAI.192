from fastapi import FastAPI,HTTPException  
from fastapi.responses import JSONResponse
from BD.conexion import Session,engine,Base
from models.modelsDB import User
from routers.usuario import routerUsuario
from routers.auth import routerAuth

app = FastAPI(
    title='Mi Primer API 192',
    description='Paola',
    version='1.0.1'
)

app.include_router(routerUsuario)
app.include_router(routerAuth)


Base.metadata.create_all(bind=engine)

# Endpoint home
@app.get('/', tags=['Hola Mundo'])
def home():
    return {'hello': 'world FastAPI'}



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