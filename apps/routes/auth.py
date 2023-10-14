from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import pyrebase
import firebase_admin
from pathlib import Path

import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from firebase_admin import auth
from config.config_settings import get_settings,get_firebase_auth
from database.mongoHandler import MongoDBHandler
from models.user import UserLogin,UserRegister


# Create an instance of the FastAPI router
authRouter = APIRouter()
settings = get_settings()
firebase_config = get_firebase_auth()
firebase = pyrebase.initialize_app(firebase_config)
mongo = MongoDBHandler()

# Initialize Firebase Admin SDK with credentials
firebase_admin.initialize_app(firebase_admin.credentials.Certificate(settings.FIREBASE_ADMIN_CREDENTIALS))



# Define a route for user registration
@authRouter.post("/register")
async def register_user(data: UserRegister):
    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user(
            email=data.email,
            password=data.password
        )
        mongo.insert_one_document({
            "user_fullname": data.user_fullname,
            "email" : data.email
        })
        return {"message": "User registered successfully", "uid": user.uid}
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")


@authRouter.post("/login")
async def login(data: UserLogin):
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email = data.email,
            password = data.password,
        )
        jwt = user['idToken']
        return JSONResponse(content={'token': jwt}, status_code=200)
    except Exception as e:
        # Return the error message in the response
        return HTTPException(detail={'message': str(e)}, status_code=400)

@authRouter.post("/ping")
async def validate(request: Request):
   headers = request.headers
   jwt = headers.get('authorization')
   
   try:
       user = auth.verify_id_token(jwt)
       return JSONResponse(content={"user_id": user["uid"]},status_code=200)
   except auth.InvalidIdTokenError as e:
       raise HTTPException(status_code=400, detail="Invalid ID token")
   except Exception as e:
       raise HTTPException(status_code=500, detail="Internal server error")

# You can add more routes and functionality as needed
