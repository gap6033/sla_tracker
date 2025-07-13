from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Health Check"])
def root():
    return {"status": "running"}