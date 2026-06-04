from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.study import ProjectGeneration
from app.schemas.study import ProjectRequest, RegenerateStepRequest
from app.services.ai_service import (
    generate_project_name, generate_project_summary,
    generate_tech_route, generate_business_model, generate_feasibility
)

router = APIRouter(prefix="/api/project", tags=["项目生成"])

DIRECTIONS = [
    "AI+医疗", "AI+教育", "AI+金融", "AI+农业", "AI+环保",
    "AI+文旅", "AI+交通", "AI+法律", "智能家居", "物联网",
    "区块链", "大数据", "云计算", "网络安全", "机器人"
]

@router.get("/directions")
def list_directions():
    return {"code": 200, "data": DIRECTIONS}

@router.post("/generate")
async def generate(data: ProjectRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Step 1: 项目命名
    name_result = await generate_project_name(data.direction, data.project_type, data.tech_preference, data.keywords)
    project_name = name_result.get("name", "未命名项目")
    subtitle = name_result.get("subtitle", "")

    # Step 2: 项目简介
    summary_result = await generate_project_summary(project_name, subtitle, data.direction, data.project_type)

    # Step 3: 技术路线
    tech_result = await generate_tech_route(project_name, data.direction, data.tech_preference, data.team_size)

    # Step 4: 商业模式
    biz_result = await generate_business_model(project_name, data.direction, data.project_type)

    # Step 5: 可行性分析
    feas_result = await generate_feasibility(project_name, data.direction, data.project_type, data.team_size)

    proj = ProjectGeneration(
        user_id=user.id,
        direction=data.direction,
        project_type=data.project_type,
        tech_preference=data.tech_preference,
        team_size=data.team_size,
        keywords=data.keywords,
        project_name=project_name,
        summary=json.dumps(summary_result, ensure_ascii=False),
        tech_route=json.dumps(tech_result, ensure_ascii=False),
        business_model=json.dumps(biz_result, ensure_ascii=False),
        feasibility=json.dumps(feas_result, ensure_ascii=False),
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)

    return {"code": 200, "data": {
        "id": proj.id,
        "project_name": project_name,
        "subtitle": subtitle,
        "naming": name_result,
        "summary": summary_result,
        "tech_route": tech_result,
        "business_model": biz_result,
        "feasibility": feas_result,
        "created_at": str(proj.created_at)
    }}

@router.post("/regenerate-step")
async def regenerate_step(data: RegenerateStepRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    proj = db.query(ProjectGeneration).filter(
        ProjectGeneration.id == data.project_id,
        ProjectGeneration.user_id == user.id
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="项目不存在")

    if data.step == "name":
        result = await generate_project_name(proj.direction, proj.project_type, proj.tech_preference, proj.keywords)
        proj.project_name = result.get("name", proj.project_name)
    elif data.step == "summary":
        result = await generate_project_summary(proj.project_name, "", proj.direction, proj.project_type)
        proj.summary = json.dumps(result, ensure_ascii=False)
    elif data.step == "tech_route":
        result = await generate_tech_route(proj.project_name, proj.direction, proj.tech_preference, proj.team_size)
        proj.tech_route = json.dumps(result, ensure_ascii=False)
    elif data.step == "business_model":
        result = await generate_business_model(proj.project_name, proj.direction, proj.project_type)
        proj.business_model = json.dumps(result, ensure_ascii=False)
    elif data.step == "feasibility":
        result = await generate_feasibility(proj.project_name, proj.direction, proj.project_type, proj.team_size)
        proj.feasibility = json.dumps(result, ensure_ascii=False)
    else:
        raise HTTPException(status_code=400, detail="无效的步骤")

    db.commit()
    return {"code": 200, "data": {"step": data.step, "result": result}}

@router.get("/history")
def history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    projs = db.query(ProjectGeneration).filter(ProjectGeneration.user_id == user.id).order_by(ProjectGeneration.created_at.desc()).limit(20).all()
    return {"code": 200, "data": [
        {"id": p.id, "direction": p.direction, "project_type": p.project_type,
         "project_name": p.project_name, "is_favorite": p.is_favorite,
         "created_at": str(p.created_at)}
        for p in projs
    ]}

@router.get("/{proj_id}")
def detail(proj_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    proj = db.query(ProjectGeneration).filter(
        ProjectGeneration.id == proj_id, ProjectGeneration.user_id == user.id
    ).first()
    if not proj:
        raise HTTPException(status_code=404, detail="项目不存在")
    return {"code": 200, "data": {
        "id": proj.id, "direction": proj.direction, "project_type": proj.project_type,
        "tech_preference": proj.tech_preference, "team_size": proj.team_size,
        "keywords": proj.keywords, "project_name": proj.project_name,
        "summary": json.loads(proj.summary) if proj.summary else None,
        "tech_route": json.loads(proj.tech_route) if proj.tech_route else None,
        "business_model": json.loads(proj.business_model) if proj.business_model else None,
        "feasibility": json.loads(proj.feasibility) if proj.feasibility else None,
        "is_favorite": proj.is_favorite, "created_at": str(proj.created_at)
    }}
