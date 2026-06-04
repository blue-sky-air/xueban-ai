from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.study import StudyPlan, CompetitionGuide, ProjectGeneration
from app.schemas.study import ToggleFavoriteRequest

router = APIRouter(prefix="/api/favorite", tags=["收藏"])

@router.post("/toggle")
def toggle(data: ToggleFavoriteRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if data.type == "plan":
        item = db.query(StudyPlan).filter(StudyPlan.id == data.ref_id, StudyPlan.user_id == user.id).first()
    elif data.type == "competition":
        item = db.query(CompetitionGuide).filter(CompetitionGuide.id == data.ref_id, CompetitionGuide.user_id == user.id).first()
    elif data.type == "project":
        item = db.query(ProjectGeneration).filter(ProjectGeneration.id == data.ref_id, ProjectGeneration.user_id == user.id).first()
    else:
        raise HTTPException(status_code=400, detail="无效类型")

    if not item:
        raise HTTPException(status_code=404, detail="记录不存在")

    item.is_favorite = not item.is_favorite
    db.commit()
    return {"code": 200, "data": {"is_favorite": item.is_favorite}}

@router.get("/list")
def list_favorites(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plans = db.query(StudyPlan).filter(StudyPlan.user_id == user.id, StudyPlan.is_favorite == True).all()
    comps = db.query(CompetitionGuide).filter(CompetitionGuide.user_id == user.id, CompetitionGuide.is_favorite == True).all()
    projs = db.query(ProjectGeneration).filter(ProjectGeneration.user_id == user.id, ProjectGeneration.is_favorite == True).all()

    result = []
    for p in plans:
        result.append({"id": p.id, "type": "plan", "title": f"{p.major} · {p.grade} · {p.goal}", "created_at": str(p.created_at)})
    for c in comps:
        result.append({"id": c.id, "type": "competition", "title": c.competition, "created_at": str(c.created_at)})
    for p in projs:
        result.append({"id": p.id, "type": "project", "title": p.project_name or p.direction, "created_at": str(p.created_at)})

    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"code": 200, "data": result}
