from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.study import StudyPlan
from app.schemas.study import StudyPlanRequest
from app.services.ai_service import generate_study_plan

router = APIRouter(prefix="/api/study", tags=["学习规划"])

@router.post("/generate")
async def generate(data: StudyPlanRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = await generate_study_plan(data.major, data.grade, data.goal, data.basics, data.target_school)
    plan = StudyPlan(
        user_id=user.id,
        major=data.major,
        grade=data.grade,
        goal=data.goal,
        result=json.dumps(result, ensure_ascii=False)
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return {"code": 200, "data": {"id": plan.id, "result": result, "created_at": str(plan.created_at)}}

@router.get("/history")
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plans = db.query(StudyPlan).filter(StudyPlan.user_id == user.id).order_by(StudyPlan.created_at.desc()).limit(20).all()
    return {"code": 200, "data": [
        {"id": p.id, "major": p.major, "grade": p.grade, "goal": p.goal,
         "result": json.loads(p.result) if p.result else None,
         "is_favorite": p.is_favorite, "created_at": str(p.created_at)}
        for p in plans
    ]}

@router.get("/{plan_id}")
def detail(plan_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = db.query(StudyPlan).filter(StudyPlan.id == plan_id, StudyPlan.user_id == user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"code": 200, "data": {
        "id": plan.id, "major": plan.major, "grade": plan.grade, "goal": plan.goal,
        "result": json.loads(plan.result) if plan.result else None,
        "is_favorite": plan.is_favorite, "created_at": str(plan.created_at)
    }}
