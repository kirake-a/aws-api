from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api.professor_route import router as professor_router
from api.student_router import router as student_router
from db.schemas import Base
from db.database import engine
from config.exception_config import register_exception_handlers
from dtos.response_wrapper import ResponseWrapper
from utils.constants import (
    OPEN_API_DESCRIPTION,
    OPEN_API_SUMMARY,
    OPEN_API_TAGS,
    OPEN_API_VERSION
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(professor_router)
app.include_router(student_router)

@app.get("/", status_code=status.HTTP_200_OK, response_model=ResponseWrapper[dict])
async def root() -> ResponseWrapper[dict]:
    return ResponseWrapper(
        success=True,
        message=f"Hey there! Welcome to the AWS API version {OPEN_API_VERSION}.",
        data={"message": f"Hey there! Welcome to the AWS API version {OPEN_API_VERSION}."}
    )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AWS API",
        version=OPEN_API_VERSION,
        contact={
            "name": "Ruben Alvarado",
            "email": "ruben_aalvarado@outlook.com",
            "url": "https://github.com/kirake-a"
        },
        summary=OPEN_API_SUMMARY,
        description=OPEN_API_DESCRIPTION,
        routes=app.routes,
        tags="",
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    openapi_schema["info"]["x-contacts"] = [
        {"name": "Ruben Alvarado", "email": "ruben_aalvarado@outlook.com"},
    ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema

app.openapi = custom_openapi

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)