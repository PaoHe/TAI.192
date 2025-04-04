from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from genToken import validateToken

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super ().__call__(request)

        data = validateToken(auth.credentials)

        if not isinstance(data, dict): #Verificar si es un diccionario valido
            raise HTTPException(status_code=401, detail="token invalido")
        
        if data.get('email') != 'pao@example.com': #Usar .get() para evitar KeyError
            raise HTTPException (status_code=403, detail="Credenciales no validas")
        