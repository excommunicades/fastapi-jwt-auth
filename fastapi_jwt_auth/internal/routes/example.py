from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1'
)


@router.get("/")
def read_root():
    return {"message": "Hello World"}