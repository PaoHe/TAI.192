from fastapi import FastAPI

app = FastAPI(
    title="Tareas",
    description="Paola",
    version="1.0.1"
)

tareas = [
    {"id": 1 , "Tarea1": "Descripcion", "Estado": "Vencimiento"}
    {"id":2, "Tarea2": "Descripcion",}

]

#Endpoint Obtener Tareas
@app.get('/tareas')
def optenerTareas():
    return tareas





