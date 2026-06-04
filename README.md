# 🎓 学伴AI — 大学生智能学习平台

> 2026年中国国际大学生创新大赛参赛项目

## 项目简介

学伴AI是一个基于大语言模型的大学生智能学习平台，提供三大核心功能：
- **AI学习规划** — 根据专业、年级、目标生成个性化学习路径
- **AI竞赛辅导** — 为各类学科竞赛生成专业备赛方案
- **AI项目生成** — 自动生成完整创新创业项目方案（核心功能）

## 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Element Plus + Pinia |
| 后端 | FastAPI + SQLAlchemy + JWT |
| AI | 兼容OpenAI API格式的大模型 |

## 快速启动

### 方式一：一键启动（Linux/Mac）
```bash
chmod +x start.sh
./start.sh
```

### 方式二：一键启动（Windows）
双击 `start.bat`

### 方式三：手动启动

**后端：**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

### 访问地址
- 前端: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 配置AI接口

编辑 `backend/.env` 文件：
```env
AI_API_KEY=你的API密钥
AI_BASE_URL=https://api.deepseek.com
AI_MODEL=deepseek-chat
```

支持任何兼容OpenAI格式的API（DeepSeek、通义千问、Kimi等）。

## 项目结构

```
xueban-ai/
├── backend/                 # 后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 配置、数据库、安全
│   │   ├── models/         # 数据库模型
│   │   ├── services/       # AI服务、Prompt模板
│   │   └── main.py         # FastAPI入口
│   └── .env                # 环境变量
├── frontend/               # 前端
│   ├── src/
│   │   ├── api/            # API请求封装
│   │   ├── router/         # 路由
│   │   ├── stores/         # 状态管理
│   │   └── views/          # 页面组件
│   └── vite.config.js
├── start.sh                # Linux启动脚本
├── start.bat               # Windows启动脚本
└── README.md
```
