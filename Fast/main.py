from fastapi import FastAPI
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

# Endpoint promedio
@app.get("/promedio", tags=["Mi Calificacion Parcial"])
def promedio():
    return {"promedio": 10}

# Endpoint parámetro opcional
@app.get("/usuario/", tags=["Parametro Opcional"])
def consultausuario(id: Optional[int] = None):
    if id is not None:
        for usu in usuarios:
            if usu["id"] == id:
                return {"mensaje": "Usuario encontrado", "usuario": usu}
        
        return {"mensaje": f"No se encontró el usuario con id: {id}"}
    else :
        return {"mensaje": "No se proporcionó un id"}

#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}