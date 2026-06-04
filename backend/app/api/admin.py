from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from app.core.database import get_db
from app.models.user import User
from app.models.study import StudyPlan, CompetitionGuide, ProjectGeneration

router = APIRouter(prefix="/api/admin", tags=["数据管理"])

# 简单的管理员认证（比赛演示够用）
ADMIN_KEY = "xueban2026"

def verify_admin(key: str = Query(...)):
    if key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="管理密钥错误")

@router.get("/stats")
def stats(key: str = Query(...), db: Session = Depends(get_db)):
    verify_admin(key)
    return {
        "users": db.query(User).count(),
        "study_plans": db.query(StudyPlan).count(),
        "competition_guides": db.query(CompetitionGuide).count(),
        "project_generations": db.query(ProjectGeneration).count(),
    }

@router.get("/users")
def list_users(key: str = Query(...), db: Session = Depends(get_db)):
    verify_admin(key)
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [{"id": u.id, "username": u.username, "email": u.email, "major": u.major, "grade": u.grade, "created_at": str(u.created_at)} for u in users]

@router.get("/plans")
def list_plans(key: str = Query(...), limit: int = 50, db: Session = Depends(get_db)):
    verify_admin(key)
    plans = db.query(StudyPlan).order_by(StudyPlan.created_at.desc()).limit(limit).all()
    return [{"id": p.id, "user_id": p.user_id, "major": p.major, "grade": p.grade, "goal": p.goal, "is_favorite": p.is_favorite, "created_at": str(p.created_at)} for p in plans]

@router.get("/competitions")
def list_competitions(key: str = Query(...), limit: int = 50, db: Session = Depends(get_db)):
    verify_admin(key)
    items = db.query(CompetitionGuide).order_by(CompetitionGuide.created_at.desc()).limit(limit).all()
    return [{"id": c.id, "user_id": c.user_id, "competition": c.competition, "role": c.role, "is_favorite": c.is_favorite, "created_at": str(c.created_at)} for c in items]

@router.get("/projects")
def list_projects(key: str = Query(...), limit: int = 50, db: Session = Depends(get_db)):
    verify_admin(key)
    items = db.query(ProjectGeneration).order_by(ProjectGeneration.created_at.desc()).limit(limit).all()
    return [{"id": p.id, "user_id": p.user_id, "direction": p.direction, "project_name": p.project_name, "project_type": p.project_type, "is_favorite": p.is_favorite, "created_at": str(p.created_at)} for p in items]

@router.delete("/users/{user_id}")
def delete_user(user_id: int, key: str = Query(...), db: Session = Depends(get_db)):
    verify_admin(key)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 删除关联数据
    db.query(StudyPlan).filter(StudyPlan.user_id == user_id).delete()
    db.query(CompetitionGuide).filter(CompetitionGuide.user_id == user_id).delete()
    db.query(ProjectGeneration).filter(ProjectGeneration.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": "已删除"}

@router.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, key: str = Query(...), db: Session = Depends(get_db)):
    verify_admin(key)
    item = db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
    if not item: raise HTTPException(404, "不存在")
    db.delete(item); db.commit()
    return {"message": "已删除"}

@router.delete("/projects/{proj_id}")
def delete_project(proj_id: int, key: str = Query(...), db: Session = Depends(get_db)):
    verify_admin(key)
    item = db.query(ProjectGeneration).filter(ProjectGeneration.id == proj_id).first()
    if not item: raise HTTPException(404, "不存在")
    db.delete(item); db.commit()
    return {"message": "已删除"}
