from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from jose.exceptions import JWTError, ExpiredSignatureError
from routes import router
from core.database import init_database
from core.settings import ALLOWED_HOSTS
from core.exceptions import (
    BadCredentialsError,
    ModelNotfoundError,
    TokenInvalidError,
    TokenExpirateError,
    UnAuthorizedError,
    UniqueFieldError
)


app = FastAPI()

app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def errors_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except ModelNotfoundError as exc:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={'reason': str(exc)})
    except UniqueFieldError as exc:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={'reason': str(exc)})

    except (BadCredentialsError, TokenExpirateError, TokenInvalidError, JWTError, ExpiredSignatureError) as exc:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'reason': str(exc)})
    except UnAuthorizedError as exc:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'reason': str(exc)},
                            headers={"WWW-Authenticate": "Bearer"},)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "errors":  exc.errors()},
#     )


@app.on_event('startup')
async def startup():
    init_database(app)
    print('app started')


@app.on_event('shutdown')
async def shutdown():
    print('app started')
