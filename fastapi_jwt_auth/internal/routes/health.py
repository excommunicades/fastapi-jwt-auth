from fastapi import APIRouter

router = APIRouter(
    prefix='/api'
)


@router.get("/health")
def healthcheck():
    return {"message": "All work correctly!"}
