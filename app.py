# imports
from fastapi import FastAPI
from routes.user import user

# defining main app
app = FastAPI()
# anexing routes
app.include_router(user)