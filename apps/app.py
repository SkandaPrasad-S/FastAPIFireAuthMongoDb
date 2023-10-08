from fastapi import FastAPI
from pathlib import Path
from config.config_settings import get_settings
from routes.auth import authRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

# Load configuration settings from the .env file
settings = get_settings()

# Create a FastAPI instance
app = FastAPI(
    title=settings.title,
    port = settings.port,
    host = settings.host
)
origins = [
    "http://localhost",
    "http://localhost:8000",
]
app.include_router(authRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define a simple route
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

# Run the FastAPI app if this script is the main module
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.host, port=settings.port)
