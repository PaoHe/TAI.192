from fastapi import FastAPI

app = FastAPI(
    title="Tareas",
    description="Paola",
    version="1.0.1"
)

tareas = [
    {"id": 1, "Tarea": "Tarea 1", "Estado": "Completo", "Vencimiento": "00-00-00"},
    {"id": 2, "Tarea": "Tarea 2", "Estado": "Incompleto", "Vencimiento": "00-00-00"},
    {"id": 3, "Tarea": "Tarea 3", "Estado": "Completo", "Vencimiento": "00-00-00"},
    {"id": 4, "Tarea": "Tarea 4", "Estado": "Incompleto", "Vencimiento": "00-00-00"}

]

#Endpoint Obtener Tareas
@app.get('/tareas')
def optenerTareas():
    return {"Las tareas son las siguientes:" : tareas }

#Endpoint Obtener Tarea por ID
@app.get('/tareas/{tareas_id}')
def optenerTareas (tareas_id: int):
    tarea = next ((t for t in tareas if t ["id"] == tareas_id), None)
    if tarea is None:
        return {"Error": "Tarea no encontrado"}
    return tarea

#Endpoint Crear una nueva tarea
@app.post('/tareas')
def crearTareas (tarea: str, estado: str, vencimiento: str ):
    nuevaTarea = {
        "id": len(tareas) + 1,
        "Tarea": tarea,
        "Estado": estado,
        "Vencimiento": vencimiento
    }
    tareas.append(nuevaTarea)
    return nuevaTarea

#Endpoint Actualizar tarea existente
@app.put('/tareas/{tarea_id}')
def actualizarTarea(tarea_id: int, tarea: str = None, estado: str = None, vencimiento: str = None):
    tareaExistente = next((t for t in tareas if t ["id"] ==  tarea_id), None)
    if tareaExistente is None:
        return {"Error": "La tarea no se encontro"}
    
    if tarea is not None:
        tareaExistente ["Tarea"] = tarea
    if estado is not None:
        tareaExistente ["Estado"] = estado
    if vencimiento is not None:
        tareaExistente ["Vencimiento"] = vencimiento
    
    return tareaExistente

#Endpoint Eliminar tarea existente
@app.delete('/tareas/{tarea_id}')
def eliminarTarea (tarea_id : int):
    global tareas
    tareas = [ t for t in tareas if t["id"] != tarea_id]
    return {"Mensaje": "La tarea eliminada"}



