from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

app = APIRouter(prefix="/users",
                tags=["users"],
                responses= {404: {"message": "No encontrado"}})

# Inicia el server: uvicorn users:app --reload

# Entidad User
class User(BaseModel):
    id:int
    name:str
    surname:str
    url:str
    age:int

users_list = [User(id=1, name="Bris", surname="Moure", url="https://mouredev.dev", age=30),
         User(id=2, name="Moure", surname="Dev", url="https://mouredev.com", age=32),
         User(id=3, name="Fabian", surname="Bermudez", url="https://fabermudez.com", age=23)]

@app.get("/")
async def usersjson():
    return [{"name":"Bris", "surname": "Moure", "url": "https://mouredev.dev", "age": 30},
            {"name":"Moure", "surname": "Dev", "url": "https://mouredev.com", "age": 32},
            {"name":"Fabian", "surname": "Bermudez", "url": "https://fabermudez.com", "age": 23}]

@app.get("/")
async def users():
    return users_list

#Path
@app.get("/{id}")
async def user(id: int):
    return search_user(id)
    
#query
@app.get("/")
async def user(id: int):
        return search_user(id)


@app.post("/")
async def user(user: User):
    if type(search_user(user.id))== User:
        return {"error": "Usuario ya existe"}
    
    users_list.append(user)
    return user 

@app.put("/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index]= user
            found = True
    
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    return user

@app.delete("/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True 
    if not found:
        return {"error": "No se ha eliminado el usuario"}
    

def search_user (id: int):
    #filter operaciones de orden superior
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado un usuario"}
    
