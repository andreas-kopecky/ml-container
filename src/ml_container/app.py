from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import JSONResponse

API_KEY_FIELD = "access_token"
API_KEY = "some_key" # XXX replace by docker secret or something

api_key_query = APIKeyQuery(name=API_KEY_FIELD, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


async def extract_api_key(query_key: str = Security(api_key_query)) -> str:
    if query_key == API_KEY:
        return query_key
    else:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="No valid API Key was provided")


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="FastAPI prediction test", version="0.0.1", routes=app.routes))


@app.get("/documentation", tags=["documentation"])
async def get_documentation():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/predict", tags=["prediction"])
async def get_open_api_endpoint(access_token: APIKey = Depends(extract_api_key)):
    return {"some": "prediction"}
