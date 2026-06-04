from pydantic import BaseModel
from typing import Optional, List

class StudyPlanRequest(BaseModel):
    major: str
    grade: str
    goal: str
    basics: Optional[List[str]] = []
    target_school: Optional[str] = None

class CompetitionRequest(BaseModel):
    competition: str
    role: str = "队员"
    time_remaining: str = "3个月"
    level: str = "入门"

class ProjectRequest(BaseModel):
    direction: str
    project_type: str = "竞赛项目"
    tech_preference: str = "不限"
    team_size: int = 3
    keywords: Optional[str] = ""

class RegenerateStepRequest(BaseModel):
    project_id: int
    step: str  # name/summary/tech_route/business_model/feasibility

class ToggleFavoriteRequest(BaseModel):
    type: str  # plan/competition/project
    ref_id: int
