from fastapi import APIRouter

router = APIRouter(
    prefix='/api',
    tags=['Server services']
)


@router.get("/health")
def healthcheck():
    return {"message": "All work correctly!"}
