from fastapi import FastAPI

#Instalar FastApi: pip install "fastapi[all]"

app = FastAPI()

# Url local: http://127.0.0.1:8000/url

@app.get("/")
async def root():
    return "Hola FastApi"

# get realiza solicitudes al servidor o leer datos

@app.get("/url")
async def root():
    return {"url":"https://mouredev.com/python"}

# Inicia el server: uvicorn main:app --reload
# Documentacion con Swagger: http://127.0.0.1:8000/docs
# Documentacion con Redocly: http://127.0.0.1:8000/redoc
