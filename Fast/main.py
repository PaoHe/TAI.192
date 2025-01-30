from fastapi import  FastAPI

app= FastAPI(
    title='Mi Primer Parcial 192',
    description='Paola ',
    version='1.0.1'
)
    

#Endpoint home

@app.get('/')
def home():
    return {'hello':'world FastAPI'}

#Endpoint promedio
@app.get('/promedio')
def promedio():
    return 6.1
