from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.database import engine, Base
from app.api import auth, study, competition, project, favorite, admin
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="学伴AI", description="大学生智能学习平台API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(study.router)
app.include_router(competition.router)
app.include_router(project.router)
app.include_router(favorite.router)
app.include_router(admin.router)

@app.get("/api/health")
def health():
    return {"status": "ok"}

# 后台管理页面
@app.get("/admin")
def admin_page():
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    return FileResponse(os.path.join(static_dir, "admin.html"))

# 生产环境：服务前端静态文件
possible_paths = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist"),
    os.path.join("/app", "frontend", "dist"),
    os.path.join(os.path.dirname(__file__), "static"),
]

frontend_dist = None
for p in possible_paths:
    if os.path.isdir(p):
        frontend_dist = p
        break

if frontend_dist:
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
