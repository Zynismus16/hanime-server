# syntax=docker/dockerfile:1

# ---------- 前端构建 ----------
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend

# 使用国内 NPM 镜像
RUN npm config set registry https://registry.npmmirror.com

# 依赖单独一层，源码改动可命中缓存
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY frontend/ ./
RUN npx vite build

# ---------- 运行镜像 ----------
FROM python:3.10-slim

ENV TZ=Asia/Shanghai \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    DEBIAN_FRONTEND=noninteractive

# 配置国内镜像源，安装 nginx / curl（健康检查用）/ tzdata
RUN set -ex && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /etc/apt/sources.list.d/* /etc/apt/sources.list && \
    printf '%s\n' \
      'deb http://mirrors.ustc.edu.cn/debian bookworm main contrib non-free non-free-firmware' \
      'deb http://mirrors.ustc.edu.cn/debian bookworm-updates main contrib non-free non-free-firmware' \
      'deb http://mirrors.ustc.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware' \
      > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nginx curl ca-certificates tzdata && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/* /var/log/apt/* /var/log/dpkg.log

WORKDIR /app

# 先装依赖，改业务代码不会让这层失效
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# 后端代码
COPY backend/ /app/backend/

# 前端产物与站点配置
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Debian 的 nginx 默认还会加载 sites-enabled，去掉以免额外监听 80
RUN rm -f /etc/nginx/sites-enabled/default && nginx -t

# 启动脚本
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh && \
    mkdir -p /app/backend/downloads /app/backend/db /app/backend/logs

# 数据目录：不挂载时容器内自洽，挂载后数据持久化
VOLUME ["/app/backend/downloads", "/app/backend/db"]

EXPOSE 7788

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD curl -fsS http://127.0.0.1:7788/api/health || exit 1

CMD ["/app/start.sh"]
