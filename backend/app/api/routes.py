from fastapi import APIRouter
from app.api.endpoints import videos, downloads
from app.services.download_service import download_manager
from app.config import settings, logger

api_router = APIRouter()


@api_router.get("/health", tags=["系统"], summary="健康检查")
async def health_check():
    """供容器健康检查与反向代理探活使用，不做任何 IO"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }

# 视频相关路由
api_router.include_router(
    videos.router,
    prefix="/videos",
    tags=["视频"]
)

api_router.include_router(
    downloads.router,
    prefix="/downloads",
    tags=["下载"]
)

@api_router.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的清理操作"""
    logger.info("应用关闭，清理连接池资源...")
    # 关闭所有HTTP客户端连接
    await download_manager.close_http_clients()
