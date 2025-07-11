# 前台前端构建阶段
FROM node:18 AS frontend-build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# 排除admin目录
RUN rm -rf admin
RUN npm run build

# 后台前端构建阶段
FROM node:18 AS admin-build
WORKDIR /app/admin
COPY admin/package*.json ./
RUN npm install
COPY admin/ ./
RUN npm run build

# Python后端构建阶段
FROM python:3.9-slim AS backend-build
WORKDIR /app
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# MySQL数据库阶段
FROM mariadb:15 AS db
ENV MYSQL_DATABASE=dance_coach
ENV MYSQL_USER=dance_admin
ENV MYSQL_PASSWORD=dance123456
ENV MYSQL_ROOT_PASSWORD=dance123456
COPY backend/dance_coach_backup.sql /docker-entrypoint-initdb.d/

# 最终运行阶段
FROM python:3.9-slim
WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# 复制前端构建产物
COPY --from=frontend-build /app/dist /app/frontend
COPY --from=admin-build /app/admin/dist /app/admin

# 复制后端
COPY --from=backend-build /app /app/backend
COPY --from=backend-build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-build /usr/local/bin /usr/local/bin

# 配置Nginx
RUN echo 'server { \
    listen 80; \
    \
    # 前台前端路由 \
    location / { \
        root /app/frontend; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
    \
    # 管理后台路由 \
    location /admin { \
        alias /app/admin; \
        index index.html; \
        try_files $uri $uri/ /admin/index.html; \
    } \
    \
    # 静态资源处理 \
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ { \
        expires max; \
        log_not_found off; \
        access_log off; \
        add_header Cache-Control "public, max-age=31536000"; \
        try_files $uri =404; \
    } \
    \
    # API后端代理 \
    location /api { \
        proxy_pass http://localhost:8000; \
        proxy_set_header Host $host; \
        proxy_set_header X-Real-IP $remote_addr; \
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \
        proxy_set_header X-Forwarded-Proto $scheme; \
    } \
}' > /etc/nginx/conf.d/default.conf

# 启动脚本
RUN echo '#!/bin/bash \n\
# 启动Nginx \n\
service nginx start \n\
# 启动后端 \n\
cd /app/backend \n\
uvicorn main:app --host 0.0.0.0 --port 8000 \n\
' > /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 80 8000

CMD ["/app/start.sh"] 