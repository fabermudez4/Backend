from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1
SECRET = "e4f9a38207293dd0345910ecf793bf7155518ef22e2aa4d62dc590df82e1dabc"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username:str
    full_name:str
    email:str
    disabled:bool

class UserDB(User):
    password: str

users_db = {
    "mauredev": {
        "username": "mauredev",
        "full_name": "Brais Moure",
        "email": "braismoure@moure.com",
        "disabled": False,
        "password": "$2a$12$8CJITUbCamIxPkXkFx8k0u7jmGGtxaQ.XPdOSBFlHxUdcA.l6jSRy"
    },
    "fabian": {
        "username": "fabermudez",
        "full_name": "Fabian Bermudez",
        "email": "fabermudez@gmail.com",
        "disabled": True,
        "password": "$2a$12$Ki6lEMHsOaLrfZXp0z3qOOZjazRW7KQYf0W1FhScgIr0rDZadlT3G"
    }
}

    
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str= Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = "Credenciales de autentificacion invalidas",
            headers={"WWW-Authenticate": "Barer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub") 
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)

async def  current_user( user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail ="Usuario inactivo")
    
    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "La contraseña no es correcta")

    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow()+ timedelta(minutes=ACCES_TOKEN_DURATION) }

    return {"acces_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user