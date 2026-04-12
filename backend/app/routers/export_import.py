"""
数据导入导出模块
支持 JSON 格式的全量数据备份和恢复
"""
import json
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from app.models import User, Category, Bookmark
from app.auth import get_current_user
from io import BytesIO

router = APIRouter(prefix="/export-import", tags=["export-import"])

EXPORT_VERSION = "1.0"
APP_NAME = "mrstrawberry-navigation"


def serialize_bookmark(bm: Bookmark) -> dict:
    """序列化书签"""
    return {
        "title": bm.title,
        "url": bm.url,
        "description": bm.description or "",
        "favicon_url": bm.favicon_url or "",
        "sort_order": bm.sort_order,
    }


def serialize_category(cat: Category) -> dict:
    """序列化分类及其书签"""
    bookmarks = [serialize_bookmark(bm) for bm in cat.bookmarks]
    # 按 sort_order 排序
    bookmarks.sort(key=lambda x: x["sort_order"])
    return {
        "name": cat.name,
        "sort_order": cat.sort_order,
        "bookmarks": bookmarks,
    }


@router.get("/export")
def export_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    导出当前用户的所有数据（分类和书签）
    """
    # 获取所有分类及其书签
    categories = (
        db.query(Category)
        .filter(Category.owner_id == current_user.id)
        .order_by(Category.sort_order, Category.created_at)
        .all()
    )

    export_data = {
        "version": EXPORT_VERSION,
        "export_time": datetime.now(timezone.utc).isoformat(),
        "app": APP_NAME,
        "data": {
            "categories": [serialize_category(cat) for cat in categories],
        },
    }

    # 生成文件名
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"{APP_NAME}_backup_{timestamp}.json"

    # 转换为 JSON 字节
    json_bytes = json.dumps(export_data, ensure_ascii=False, indent=2).encode("utf-8")

    return StreamingResponse(
        BytesIO(json_bytes),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.post("/import", status_code=status.HTTP_200_OK)
def import_data(
    file: UploadFile = File(...),
    mode: str = "merge",  # merge: 合并, replace: 替换
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    导入数据
    mode:
      - merge: 合并模式，保留现有数据，同名分类合并书签
      - replace: 替换模式，清空现有数据后导入
    """
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith(("application/json", "text/")):
        raise HTTPException(status_code=400, detail="请上传 JSON 文件")

    try:
        content = file.file.read().decode("utf-8")
        import_data = json.loads(content)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"JSON 格式错误: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"文件读取失败: {str(e)}")

    # 验证数据结构
    if not isinstance(import_data, dict):
        raise HTTPException(status_code=400, detail="无效的导入格式")

    version = import_data.get("version", "1.0")
    data = import_data.get("data", {})
    categories_data = data.get("categories", [])

    if not isinstance(categories_data, list):
        raise HTTPException(status_code=400, detail="categories 必须是数组")

    # 替换模式：先删除现有数据
    if mode == "replace":
        db.query(Bookmark).filter(Bookmark.owner_id == current_user.id).delete(
            synchronize_session=False
        )
        db.query(Category).filter(Category.owner_id == current_user.id).delete(
            synchronize_session=False
        )
        db.commit()

    # 导入数据
    imported_categories = 0
    imported_bookmarks = 0
    errors = []

    for cat_data in categories_data:
        cat_name = cat_data.get("name", "").strip()
        if not cat_name:
            errors.append(f"跳过无名分类")
            continue

        cat_sort_order = cat_data.get("sort_order", 0)
        bookmarks_data = cat_data.get("bookmarks", [])

        # 查找或创建分类
        category = (
            db.query(Category)
            .filter(Category.owner_id == current_user.id, Category.name == cat_name)
            .first()
        )

        if not category:
            category = Category(
                name=cat_name,
                sort_order=cat_sort_order,
                owner_id=current_user.id,
            )
            db.add(category)
            db.flush()  # 获取 category.id
            imported_categories += 1

        # 导入书签
        for bm_data in bookmarks_data:
            title = bm_data.get("title", "").strip()
            url = bm_data.get("url", "").strip()

            if not title or not url:
                errors.append(f"分类 '{cat_name}' 中有书签缺少标题或 URL")
                continue

            # 检查是否已存在相同 URL 的书签
            existing = (
                db.query(Bookmark)
                .filter(Bookmark.owner_id == current_user.id, Bookmark.url == url)
                .first()
            )

            if existing:
                # 更新现有书签
                existing.title = title
                existing.description = bm_data.get("description", "")
                existing.favicon_url = bm_data.get("favicon_url", "")
                existing.sort_order = bm_data.get("sort_order", 0)
                existing.category_id = category.id
            else:
                # 创建新书签
                bookmark = Bookmark(
                    title=title,
                    url=url,
                    description=bm_data.get("description", ""),
                    favicon_url=bm_data.get("favicon_url", ""),
                    sort_order=bm_data.get("sort_order", 0),
                    owner_id=current_user.id,
                    category_id=category.id,
                )
                db.add(bookmark)
                imported_bookmarks += 1

    db.commit()

    return {
        "success": True,
        "imported_categories": imported_categories,
        "imported_bookmarks": imported_bookmarks,
        "errors": errors if errors else None,
        "version": version,
    }


@router.post("/validate")
def validate_import_file(
    file: UploadFile = File(...),
):
    """
    验证导入文件格式是否正确（不实际导入）
    """
    try:
        content = file.file.read().decode("utf-8")
        data = json.loads(content)

        # 基本结构验证
        if not isinstance(data, dict):
            return {"valid": False, "error": "根对象必须是字典"}

        version = data.get("version", "unknown")
        app = data.get("app", "unknown")
        data_section = data.get("data", {})
        categories = data_section.get("categories", [])

        if not isinstance(categories, list):
            return {"valid": False, "error": "data.categories 必须是数组"}

        # 统计
        bookmark_count = sum(
            len(cat.get("bookmarks", [])) for cat in categories
        )

        return {
            "valid": True,
            "version": version,
            "app": app,
            "categories_count": len(categories),
            "bookmarks_count": bookmark_count,
        }

    except json.JSONDecodeError as e:
        return {"valid": False, "error": f"JSON 解析错误: {str(e)}"}
    except Exception as e:
        return {"valid": False, "error": str(e)}
