from fastapi import FastAPI

app = FastAPI(
    title="Tareas",
    description="Paola",
    version="1.0.1"
)


#Endpoint 
@app.get('/')
def home():
    return {'mensaje': 'Holi'}
