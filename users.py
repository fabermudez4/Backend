from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#Inicia el server : uvicorn users:app --reload

#Emtidad user

class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int

#users = [User("Brais","moure","https://moure.dev", 35)]

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Brais", "surname": "moure", "url":"https://moure.dev", "age":35}] 

@app.get("/userclass")
async def userclass():
    return User(name="Brais", surname= "moure", url= "https://moure.dev", age= 35)