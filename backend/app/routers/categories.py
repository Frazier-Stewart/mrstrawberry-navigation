from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.models import User, Category
from app.schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.auth import get_current_user
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Category)
        .filter(Category.owner_id == current_user.id)
        .order_by(Category.sort_order, Category.created_at)
        .all()
    )


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    body: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(Category)
        .filter(Category.owner_id == current_user.id, Category.name == body.name)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="分类名称已存在")
    cat = Category(name=body.name, sort_order=body.sort_order, owner_id=current_user.id)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    body: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cat = db.query(Category).filter(Category.id == category_id, Category.owner_id == current_user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    if body.name is not None:
        cat.name = body.name
    if body.sort_order is not None:
        cat.sort_order = body.sort_order
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cat = db.query(Category).filter(Category.id == category_id, Category.owner_id == current_user.id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="分类不存在")
    db.delete(cat)
    db.commit()


# ── Batch sort order update ────────────────────────────────────────────────────

class CategorySortItem(BaseModel):
    id: int
    sort_order: int


@router.post("/sort/batch", status_code=status.HTTP_200_OK)
def update_categories_sort_order(
    items: List[CategorySortItem],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """批量更新分类排序"""
    for item in items:
        cat = db.query(Category).filter(Category.id == item.id, Category.owner_id == current_user.id).first()
        if cat:
            cat.sort_order = item.sort_order
    db.commit()
    return {"success": True, "updated": len(items)}
