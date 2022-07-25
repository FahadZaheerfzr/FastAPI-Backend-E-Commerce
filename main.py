import json
import fastapi
from fastapi import FastAPI, Depends, Request
from tortoise.contrib.fastapi import register_tortoise
from authentication import *
from models import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise import Tortoise


app = FastAPI()

app.add_middleware(
   CORSMiddleware,
    allow_origins = ["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials =True,
    allow_methods = ["*"],
    allow_headers= ["*"],   
)

SECERT_KEY = "YOUR_FAST_API_SECRET_KEY"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config_credentials["SECRET"], algorithms=[ALGORITHM])
        user = await User.get(id = payload.get("id"))
    except:
        raise fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return await user


@app.post('/token')
async def generate_token(request_form: OAuth2PasswordRequestForm = Depends()):
    token = await token_generator(request_form.username, request_form.password)
    if token:
        return {"access_token": token, "token_type": "bearer"}
    else:
        return {"message":"login failed"}


@app.post('/register')
async def user_registration(user: user_pydanticIn):
    user_info = user.dict(exclude_unset=True)
    user_info["password"] = get_hashed_password(user_info['password'])
    user_obj = await User.create(**user_info)
    #new_user = await user_pydantic.from_tortoise_orm(user_obj)
    return{
        "status" : "Ok",
        "data" : "Registration Succesfull"
    }


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/get_cart/user')
async def get_cart(user:user_pydanticIn = Depends(get_current_user)):
    pass

@app.post('/add_to_cart/user')
async def add_to_cart(cart_info, user: user_pydanticIn = Depends(get_current_user)):
    pass


@app.post('/add_category')
async def addCategory(request: Request, user:user_pydanticIn = Depends(get_current_user)):
    conn = Tortoise.get_connection("default")
    data = await request.body()
    json_data = json.loads(str(data, encoding='utf-8'))
    if json_data["parent"] == "None":
        query = f'INSERT INTO category (name, slug, description, parent_cat_id) VALUES ("{json_data["name"]}", "{json_data["slug"]}", "{json_data["description"]}", null);'
    else:
        parent_cat = json_data["parent"]
        print(parent_cat)
        get_query = f'Select id from category where name = "{parent_cat}"'
        parent = await conn.execute_query(get_query)
        create_query = query = f'INSERT INTO category (name, slug, description, parent_cat_id) VALUES ("{json_data["name"]}", "{json_data["slug"]}", "{json_data["description"]}", "{parent[0]}");'
            

@app.get('/get_categories')
async def getCategories(user:user_pydanticIn = Depends(get_current_user)):
    conn = Tortoise.get_connection("default")
    val = await conn.execute_query_dict("SELECT * FROM category")
    return {
        "status":"ok",
        "value": json.dumps(val),
    }



database_url = "mysql://root:root@localhost:8889/e-commerce"

register_tortoise(
    app,
    db_url=database_url,
    modules={"models":["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)