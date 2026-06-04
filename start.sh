#!/bin/bash
# 学伴AI 一键启动脚本

echo "🎓 学伴AI - 大学生智能学习平台"
echo "================================"

# 启动后端
echo "🚀 启动后端服务 (端口 8000)..."
cd "$(dirname "$0")/backend"
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 启动前端
echo "🚀 启动前端服务 (端口 5173)..."
cd "$(dirname "$0")/frontend"
npx vite --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

echo ""
echo "✅ 启动完成！"
echo "   前端: http://localhost:5173"
echo "   后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止所有服务"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
