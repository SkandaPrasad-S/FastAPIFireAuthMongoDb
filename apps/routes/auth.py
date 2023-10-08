from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
import pyrebase
import firebase_admin
from pathlib import Path

import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from firebase_admin import auth
from config.config_settings import get_settings
from models.user import UserLogin,UserRegister
# Create an instance of the FastAPI router
authRouter = APIRouter()

settings = get_settings()
# Load configuration settings from the .env file
firebase_config = {
    "apiKey": settings.firebase_api_key,
    "authDomain": settings.firebase_auth_domain,
    "projectId": settings.firebase_project_id,
    "storageBucket": settings.firebase_storage_bucket,
    "messagingSenderId": settings.firebase_messaging_sender_id,
    "appId": settings.firebase_app_id,
    "measurementId": settings.firebase_measurement_id,
    "databaseURL" : ""
}
firebase = pyrebase.initialize_app(firebase_config)

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
