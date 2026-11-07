from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


class DownloadStatus(str, Enum):
    """下载状态枚举"""
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"


class DownloadSegment(BaseModel):
    """下载分段模型"""
    start: int
    end: int
    downloaded: int = 0
    status: str = DownloadStatus.PENDING


class DownloadRequest(BaseModel):
    """下载请求模型"""
    video_id: str
    filename: Optional[str] = None      # 自定义文件名模板，留空则使用全局设置
    sub_path: Optional[str] = None      # 自定义子路径模板，留空则使用全局设置
    force: Optional[bool] = False       # 二次确认后置为 True，会覆盖已有记录


class DownloadAction(BaseModel):
    """下载操作模型"""
    video_id: str
    action: str  # 'pause', 'resume', 'cancel', 'retry', 'delete'


class DownloadSettings(BaseModel):
    """下载命名设置"""
    sub_path_template: str = ""
    filename_template: str = "{video_id}_{title}"
    variables: List[Dict[str, str]] = Field(default_factory=list, description="可用变量说明")
    examples: List[Dict[str, Any]] = Field(default_factory=list, description="预设模板示例")


class PathPreviewRequest(BaseModel):
    """路径预览请求"""
    video_id: str
    sub_path: Optional[str] = None
    filename: Optional[str] = None


class PathPreview(BaseModel):
    """路径预览结果"""
    sub_path: str = ""
    filename: str = ""
    rel_path: str = ""
    absolute_path: str = ""
    exists: bool = False
    variables: Dict[str, str] = Field(default_factory=dict)


class DownloadConflict(BaseModel):
    """下载冲突信息（用于前端二次确认）"""
    type: str = ""                      # in_progress / completed / completed_missing / file_exists
    title: str = ""
    message: str = ""
    detail: str = ""
    existing_status: Optional[str] = None
    existing_progress: Optional[float] = None
    existing_size: Optional[int] = None
    rel_path: Optional[str] = None


class DownloadProgress(BaseModel):
    """下载进度模型"""
    video_id: str
    filename: str
    title: Optional[str] = None
    cover_url: Optional[str] = None
    total_size: int
    downloaded: int
    status: str
    speed: float  # bytes per second
    error_message: Optional[str] = None
    url: str = ""
    created_at: datetime
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    segments: Optional[List[DownloadSegment]] = None
    # 自定义路径相关
    sub_path: str = ""
    rel_path: str = ""
    variables: Optional[Dict[str, str]] = None


class DownloadConfig(BaseModel):
    """下载配置模型"""
    chunk_size: int = 1024 * 1024 * 16  # 16MB
    buffer_size: int = 1024 * 1024 * 4  # 4MB
    max_segments: int = 4
    min_segment_size: int = 40 * 1024 * 1024  # 40MB
    max_retries: int = 3
    timeout: float = 30.0
    progress_update_interval: float = 0.5 