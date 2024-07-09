from fastapi import FastAPI, APIRouter
from routers import auth, todos, admin, users
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# Heartbit of app

@app.get("/healthy", status_code=200)
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
