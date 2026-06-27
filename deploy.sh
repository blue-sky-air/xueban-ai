#!/bin/bash
set -e

echo "=============================="
echo "  学伴AI 一键部署脚本"
echo "=============================="

# 1. 安装依赖
echo "[1/6] 安装系统依赖..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nodejs npm nginx git > /dev/null 2>&1

# 安装 Node.js 20
if ! command -v node &> /dev/null || [[ $(node -v | cut -d. -f1 | tr -d v) -lt 18 ]]; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - > /dev/null 2>&1
    apt-get install -y -qq nodejs > /dev/null 2>&1
fi

echo "  Python: $(python3 --version)"
echo "  Node: $(node --version)"

# 2. 克隆项目
echo "[2/6] 克隆项目..."
APP_DIR="/opt/xueban-ai"
if [ -d "$APP_DIR" ]; then
    cd "$APP_DIR" && git pull
else
    git clone https://github.com/blue-sky-air/xueban-ai.git "$APP_DIR"
    cd "$APP_DIR"
fi

# 3. 配置环境变量
echo "[3/6] 配置环境变量..."
if [ ! -f "$APP_DIR/backend/.env" ]; then
    echo "请输入你的 AI API Key（直接回车跳过，稍后手动配置）:"
    read -r API_KEY
    if [ -z "$API_KEY" ]; then
        API_KEY="sk-你的key"
    fi

    cat > "$APP_DIR/backend/.env" << EOF
AI_API_KEY=${API_KEY}
AI_BASE_URL=https://token-plan-cn.xiaomimimo.com
AI_MODEL=mimo-v2.5-pro
JWT_SECRET=$(openssl rand -hex 16)
DATABASE_URL=sqlite:///./xueban_ai.db
PORT=8000
EOF
    echo "  环境变量已写入 $APP_DIR/backend/.env"
else
    echo "  .env 已存在，跳过"
fi

# 4. 构建前端
echo "[4/6] 构建前端..."
cd "$APP_DIR/frontend"
npm install --silent 2>/dev/null
npm run build
echo "  前端构建完成"

# 5. 配置域名和SSL
echo "[5/6] 配置域名..."
DOMAIN="bblue.art"

# 安装 certbot 用于申请SSL证书
apt-get install -y -qq certbot python3-certbot-nginx > /dev/null 2>&1

echo "[6/6] 配置服务..."

# 安装后端依赖
cd "$APP_DIR/backend"
pip3 install -r requirements.txt -q 2>/dev/null

# 创建 systemd 服务
cat > /etc/systemd/system/xueban.service << EOF
[Unit]
Description=XueBan AI
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR/backend
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable xueban
systemctl restart xueban

# 配置 Nginx
cat > /etc/nginx/sites-available/xueban << NGINX
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;
    }
}
NGINX

ln -sf /etc/nginx/sites-available/xueban /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# 获取公网IP
PUBLIC_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ip.sb 2>/dev/null || echo "你的服务器IP")

echo ""
echo "=============================="
echo "  部署完成！"
echo "=============================="
echo ""
echo "  访问地址: http://${DOMAIN}"
echo "  备用地址: http://${PUBLIC_IP}"
echo "  API文档:  http://${DOMAIN}/docs"
echo "  数据管理: http://${DOMAIN}/api/admin/stats?key=xueban2026"
echo ""
echo "  ⚠️  重要提醒："
echo "  1. 请确保域名 ${DOMAIN} 已解析到服务器IP: ${PUBLIC_IP}"
echo "  2. 申请HTTPS证书: sudo certbot --nginx -d ${DOMAIN} -d www.${DOMAIN}"
echo "  3. ICP备案号已添加到页面底部"
echo "  4. 请在30日内完成公安联网备案"
echo ""
echo "  修改配置: vim $APP_DIR/backend/.env"
echo "  重启服务: systemctl restart xueban"
echo "  查看日志: journalctl -u xueban -f"
echo ""
