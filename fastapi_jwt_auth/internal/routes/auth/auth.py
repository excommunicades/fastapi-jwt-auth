from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1',
    tags=['Identity Management']
)


@router.post('/register')
def registration():

    pass

@router.post('/login')
def login():

    pass

@router.post('/token')
def refresh_token():

    pass