# imports
from fastapi import FastAPI
from routes.user import user
from routes.queue import queue

# defining main app
app = FastAPI()
# anexing routes
app.include_router(user)
app.include_router(queue)