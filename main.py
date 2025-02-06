from fastapi import FastAPI, HTTPException, Depends, APIRouter
from database import db
from models import User, Product, UserLogin
from bson import ObjectId
from auth import hash_password, verify_password, create_access_token, get_current_user
from product_routes import router as product_router
from services_routes import router as service_router

app = FastAPI()

app.include_router(product_router)
app.include_router(service_router)

@app.get("/")
def home():
    return {"message": "Welcome to the Online Business API"}

# Create User
@app.post("/users/")
async def create_user(user: User):
    user_dict = user.dict()
    result = await db.users.insert_one(user_dict)
    return {"id": str(result.inserted_id), **user_dict}

# Get Users
@app.get("/users/")
async def get_users():
    users = await db.users.find().to_list(100)
    return [{"id": str(user["_id"]), **user} for user in users]

@app.post("/signup/")
async def signup(user: User):
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    
    # Insert user into database
    result = await db.users.insert_one(user_dict)
    return {"id": str(result.inserted_id), "message": "User registered successfully"}

@app.post("/login/")
async def login(user: UserLogin):
    # Find user in database
    user_db = await db.users.find_one({"email": user.email})
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify password
    if not verify_password(user.password, user_db["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Create JWT Token
    token = create_access_token({"user_id": str(user_db["_id"]), "email": user_db["email"]})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected/")
async def protected_route(user=Depends(get_current_user)):
    return {"message": "You have access!", "user": user}

