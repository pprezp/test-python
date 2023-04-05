from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import  CORSMiddleware
from routes import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"]
)

app.include_router( router=posts, prefix='/api/v1/tokspersonalfile'  )

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="External API for tokspersonalfile project",
        version="0.0.0",
        description="API creada para enviar archivos al sustema de tokspersonalfile",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi