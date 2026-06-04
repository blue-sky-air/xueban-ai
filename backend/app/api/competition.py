from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.study import CompetitionGuide
from app.schemas.study import CompetitionRequest
from app.services.ai_service import generate_competition_guide

router = APIRouter(prefix="/api/competition", tags=["竞赛辅导"])

COMPETITIONS = [
    {"name": "全国大学生数学建模竞赛", "category": "数学建模"},
    {"name": "美国大学生数学建模竞赛(MCM/ICM)", "category": "数学建模"},
    {"name": "ACM/ICPC国际大学生程序设计竞赛", "category": "程序设计"},
    {"name": "蓝桥杯全国软件和信息技术专业人才大赛", "category": "程序设计"},
    {"name": "中国大学生计算机设计大赛", "category": "程序设计"},
    {"name": "中国国际大学生创新大赛(互联网+)", "category": "创新创业"},
    {"name": "挑战杯全国大学生课外学术科技作品竞赛", "category": "创新创业"},
    {"name": "全国大学生电子设计竞赛", "category": "电子设计"},
    {"name": "Kaggle数据科学竞赛", "category": "人工智能"},
    {"name": "天池大数据竞赛", "category": "人工智能"},
    {"name": "全国大学生创新创业训练计划(大创)", "category": "综合"},
]

@router.get("/list")
def list_competitions():
    return {"code": 200, "data": COMPETITIONS}

@router.post("/generate")
async def generate(data: CompetitionRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = await generate_competition_guide(data.competition, data.role, data.time_remaining, data.level)
    guide = CompetitionGuide(
        user_id=user.id,
        competition=data.competition,
        role=data.role,
        time_remaining=data.time_remaining,
        level=data.level,
        result=json.dumps(result, ensure_ascii=False)
    )
    db.add(guide)
    db.commit()
    db.refresh(guide)
    return {"code": 200, "data": {"id": guide.id, "result": result, "created_at": str(guide.created_at)}}

@router.get("/history")
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    guides = db.query(CompetitionGuide).filter(CompetitionGuide.user_id == user.id).order_by(CompetitionGuide.created_at.desc()).limit(20).all()
    return {"code": 200, "data": [
        {"id": g.id, "competition": g.competition, "role": g.role,
         "result": json.loads(g.result) if g.result else None,
         "is_favorite": g.is_favorite, "created_at": str(g.created_at)}
        for g in guides
    ]}
