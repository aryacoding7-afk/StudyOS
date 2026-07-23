from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.modules.search.schemas import (
    SearchRequest,
    SearchResponse,
)
from app.modules.search.service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
)
def search(
    request: SearchRequest,
    db: Session = Depends(get_db),
):
    service = SearchService(db)
    return service.search(request)