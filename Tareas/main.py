from fastapi import FastAPI

app = FastAPI(
    title="Tareas",
    description="Paola",
    version="1.0.1"
)

#Endpoint Obtener Tareas
@app.get('/tareas')
def optenerTareas():
    return { }




