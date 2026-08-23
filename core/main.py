from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from core.app.database import Base, engine
from core.auth.jwtauth import get_authenticated_user
from core.costs.routes import router as costs_router
from core.user.model import UserModel
from core.user.routes import router as auth_router

tags_metada=[
    {
        "name":"costs",
        "description":"cost management"
    }
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")

    Base.metadata.create_all(engine)

    yield

    print("Application shutdown")

app = FastAPI(
    title="Simple Cost Manager App",
    version="1.0.0",
    docs_url="/swagger",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(costs_router)


@app.get("/private")
def private_route(current_user: UserModel = Depends(get_authenticated_user)):
    return {"message": f"Hello {current_user.username}, this is a private route."}


@app.get("/public")
def public_route():
    return {"message": "This is a public route."}
