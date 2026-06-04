from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class StudyPlan(Base):
    __tablename__ = "study_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    major = Column(String(50))
    grade = Column(String(10))
    goal = Column(String(50))
    result = Column(Text)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class CompetitionGuide(Base):
    __tablename__ = "competition_guides"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    competition = Column(String(100))
    role = Column(String(20))
    time_remaining = Column(String(20))
    level = Column(String(20))
    result = Column(Text)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class ProjectGeneration(Base):
    __tablename__ = "project_generations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    direction = Column(String(100))
    project_type = Column(String(50))
    tech_preference = Column(String(50))
    team_size = Column(Integer)
    keywords = Column(String(255))
    project_name = Column(String(200))
    summary = Column(Text)
    tech_route = Column(Text)
    business_model = Column(Text)
    feasibility = Column(Text)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
