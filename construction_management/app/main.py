from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, Request, status

from db.database import Base, engine
from models.user import User
from models.site import ConstructionSite, SiteMember
from models.work_item import WorkItem


# from routers.auth import 
# from routers.users import 
# from routers.site import 
# from routers.work_item import 


from utils.response import error_response, success_response

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Construction Management API",
    description="API quản lý công trình thi công",
    version="1.0.0"
)

@app.exception_handler(HTTPException)
def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            request=request,
            status_code=exc.status_code,
            message=str(exc.detail),
            errors=None
        )
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=error_response(
            request=request,
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            message="Validation error",
            errors=exc.errors()
        )
    )


@app.exception_handler(Exception)
def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            request=request,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            errors=None
        )
    )

# app.include_router(auth.router)
# app.include_router(users.router)
# app.include_router(site.router)
# app.include_router(work_item.router)

@app.get("/health",tags=["Health"])
def health_check(request: Request):
    return success_response(
        data="ok",
        message="Construction Management API is running",
        request=request
    )