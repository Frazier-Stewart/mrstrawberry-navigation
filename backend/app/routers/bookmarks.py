from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from app.models import User, Bookmark
from app.schemas import BookmarkCreate, BookmarkUpdate, BookmarkResponse
from app.auth import get_current_user

router = APIRouter(prefix="/bookmarks", tags=["bookmarks"])


@router.get("", response_model=List[BookmarkResponse])
def list_bookmarks(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Bookmark).filter(Bookmark.owner_id == current_user.id)
    if category_id is not None:
        q = q.filter(Bookmark.category_id == category_id)
    return q.order_by(Bookmark.sort_order, Bookmark.created_at).all()


@router.post("", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def create_bookmark(
    body: BookmarkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bm = Bookmark(**body.model_dump(), owner_id=current_user.id)
    db.add(bm)
    db.commit()
    db.refresh(bm)
    return bm


@router.put("/{bookmark_id}", response_model=BookmarkResponse)
def update_bookmark(
    bookmark_id: int,
    body: BookmarkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bm = db.query(Bookmark).filter(Bookmark.id == bookmark_id, Bookmark.owner_id == current_user.id).first()
    if not bm:
        raise HTTPException(status_code=404, detail="书签不存在")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(bm, field, value)
    db.commit()
    db.refresh(bm)
    return bm


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    bookmark_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bm = db.query(Bookmark).filter(Bookmark.id == bookmark_id, Bookmark.owner_id == current_user.id).first()
    if not bm:
        raise HTTPException(status_code=404, detail="书签不存在")
    db.delete(bm)
    db.commit()
