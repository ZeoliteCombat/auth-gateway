import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define models
class User(BaseModel):
    username: str
    password: str

# Define API routes
app = FastAPI()

# Route for user authentication
@app.post("/auth/login")
async def login(user: User):
    if user.username == "admin" and user.password == "password":
        return {"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaGFuIjoiMjMwfQ.SflKxwRJSMeKKF2QT4fwpMeHqESwltivS3xj1fV4g"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Route for protected endpoint
@app.get("/protected")
async def protected():
    return {"message": "Hello, world!"}

# Run the application
if __name__ == "__main__":
    logger.info("Starting auth-gateway application")
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)