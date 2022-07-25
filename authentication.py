from numpy import deprecate
from passlib.context import CryptContext
import jwt
from models import User
from dotenv import dotenv_values

config_credentials = dotenv_values(".env")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(password):
    return pwd_context.hash(password)

async def verify_password(plain_password, hashed_password):
    verified = pwd_context.verify(plain_password, hashed_password)
    return verified


async def authenticate_user(username:str, password:str):
    user = await User.get(username=username)
    verified = await verify_password(password, user.password)
    if user and verified:
        return user
    return False

async def token_generator(username:str, password:str):
    user = await authenticate_user(username,password)
    if not user:
        return False
    
    token_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "contact": user.contact_number,
        "is_admin": user.is_admin
    }

    token = jwt.encode(token_data, config_credentials["SECRET"])

    return token