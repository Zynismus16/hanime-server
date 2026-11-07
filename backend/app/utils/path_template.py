"""
下载路径 / 文件名模板引擎

支持在「子路径」和「文件名」中使用变量，例如：

    子路径模板:  {studio}/{series}
    文件名模板:  {title} [{quality}]

语法：`${变量名}` 或 `{变量名}`（两种写法等价，推荐 `${}`，避免与普通花括号混淆）。
子路径模板中用 `/` 分隔层级，每一层分别做非法字符清洗；
未提供值的变量会被替换为空字符串，并自动丢弃因此变空的路径层级（不会产生 `//`）。
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 默认模板：保持与原版一致的「视频ID_标题.mp4」命名
DEFAULT_SUB_PATH_TEMPLATE = ""
DEFAULT_FILENAME_TEMPLATE = "{video_id}_{title}"
DEFAULT_EXT = ".mp4"

# 可在模板中使用的变量（前端据此渲染「可用变量」提示）
VARIABLES: List[Dict[str, str]] = [
    {"key": "title", "label": "视频标题", "sample": "作品标题"},
    {"key": "subtitle", "label": "副标题", "sample": "副标题"},
    {"key": "series", "label": "系列名", "sample": "系列名"},
    {"key": "studio", "label": "发行商 / 上传者", "sample": "发行商"},
    {"key": "video_type", "label": "视频类型", "sample": "类型"},
    {"key": "video_id", "label": "视频 ID", "sample": "123456"},
    {"key": "tags", "label": "标签（逗号分隔）", "sample": "标签A,标签B"},
    {"key": "upload_date", "label": "发布日期 YYYY-MM-DD", "sample": "2025-06-21"},
    {"key": "year", "label": "发布年", "sample": "2025"},
    {"key": "month", "label": "发布月", "sample": "06"},
    {"key": "day", "label": "发布日", "sample": "21"},
    {"key": "date", "label": "下载日期 YYYY-MM-DD", "sample": "2025-08-01"},
    {"key": "duration", "label": "时长", "sample": "24:00"},
    {"key": "quality", "label": "清晰度", "sample": "1080p"},
    {"key": "ext", "label": "扩展名（不含点）", "sample": "mp4"},
]

VARIABLE_KEYS = {item["key"] for item in VARIABLES}

# ${name} 或 {name}
_PLACEHOLDER_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Windows / POSIX 都不允许出现在文件名中的字符
_ILLEGAL_CHARS = '<>:"\\|?*'
_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")

# Windows 保留设备名
_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL"} | {
    f"{prefix}{i}" for prefix in ("COM", "LPT") for i in range(1, 10)
}

# 允许的扩展名（未命中则自动补 .mp4）
_KNOWN_EXTS = {".mp4", ".mkv", ".ts", ".flv", ".avi", ".mov", ".webm", ".m4v"}

MAX_SEGMENT_LEN = 80      # 单个路径层级最大长度
MAX_FILENAME_LEN = 180    # 文件名最大长度（含扩展名）


class TemplateError(ValueError):
    """模板非法"""


def extract_variables(template: str) -> List[str]:
    """提取模板中引用到的变量名"""
    if not template:
        return []
    keys = []
    for match in _PLACEHOLDER_RE.finditer(template):
        keys.append(match.group(1) or match.group(2))
    return keys


def validate_template(template: str, field: str = "模板") -> List[str]:
    """
    校验模板，返回警告信息列表（不抛异常，交由调用方决定是否拦截）

    - 空模板：子路径允许，文件名不允许
    - 未知变量：视为错误
    - `..`：视为错误（防路径穿越）
    """
    warnings: List[str] = []
    if ".." in (template or "").replace("${", "").replace("{", ""):
        raise TemplateError(f"{field}不能包含相对路径符号 '..'")

    unknown = sorted({key for key in extract_variables(template) if key not in VARIABLE_KEYS})
    if unknown:
        raise TemplateError(f"{field}包含未知变量: {', '.join(unknown)}")

    # 去掉变量后若完全没有字面量，说明模板只由变量构成，属于正常情况
    return warnings


def render(template: str, variables: Dict[str, Any]) -> str:
    """替换模板中的变量；未取到值的变量替换为空串"""
    if not template:
        return ""

    def _replace(match: "re.Match[str]") -> str:
        key = match.group(1) or match.group(2)
        value = variables.get(key, "")
        if value is None:
            return ""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        return str(value)

    return _PLACEHOLDER_RE.sub(_replace, template)


def sanitize_segment(value: str, max_len: int = MAX_SEGMENT_LEN) -> str:
    """清洗单个路径层级（目录名或文件名主体）"""
    text = _CONTROL_CHARS.sub("", value or "")
    for char in _ILLEGAL_CHARS:
        text = text.replace(char, "_")
    text = text.replace("/", "_").replace("\\", "_")
    text = re.sub(r"\s+", " ", text)
    text = text.strip(" .")
    if len(text) > max_len:
        text = text[:max_len].rstrip(" .")
    if not text or set(text) <= {"."}:
        text = "_"
    if text.split(".")[0].upper() in _RESERVED_NAMES:
        text = f"_{text}"
    return text


def _ensure_extension(filename: str, default_ext: str = DEFAULT_EXT) -> str:
    """保证文件名带扩展名"""
    suffix = Path(filename).suffix.lower()
    if suffix in _KNOWN_EXTS:
        return filename
    if suffix and len(suffix) <= 5:
        # 用户显式写了别的扩展名，尊重其选择
        return filename
    return filename + default_ext


def sanitize_filename(value: str, default_ext: str = DEFAULT_EXT) -> str:
    """清洗完整文件名（保留扩展名）"""
    text = value.strip()
    stem, suffix = os.path.splitext(text)
    if not stem:
        stem, suffix = text, ""
    stem = sanitize_segment(stem, MAX_FILENAME_LEN - len(suffix) - 1)
    filename = _ensure_extension(f"{stem}{suffix}", default_ext)
    if len(filename) > MAX_FILENAME_LEN:
        stem, suffix = os.path.splitext(filename)
        filename = f"{stem[: MAX_FILENAME_LEN - len(suffix) - 1]}{suffix}"
    return filename


def build_relative_path(
    sub_path_template: str,
    filename_template: str,
    variables: Dict[str, Any],
    default_ext: str = DEFAULT_EXT,
) -> str:
    """
    渲染出相对路径（POSIX 分隔符），例如 `发行商/系列/标题.mp4`
    """
    segments: List[str] = []
    for raw in (sub_path_template or "").split("/"):
        rendered = render(raw, variables).strip()
        if not rendered:
            # 变量为空导致的空层级直接丢弃
            continue
        segment = sanitize_segment(rendered)
        if segment:
            segments.append(segment)

    filename = sanitize_filename(
        render(filename_template or DEFAULT_FILENAME_TEMPLATE, variables),
        default_ext=default_ext,
    )
    segments.append(filename)
    return "/".join(segments)


def resolve_target(
    base_dir: Path,
    sub_path_template: str,
    filename_template: str,
    variables: Dict[str, Any],
    default_ext: str = DEFAULT_EXT,
) -> Tuple[str, str, Path]:
    """
    计算最终落盘位置

    Returns:
        (相对目录, 文件名, 绝对路径)
    """
    relative = build_relative_path(sub_path_template, filename_template, variables, default_ext)
    abs_path = (Path(base_dir) / relative)
    _assert_inside(base_dir, abs_path)

    rel_dir = os.path.dirname(relative)
    return rel_dir, os.path.basename(relative), abs_path


def _assert_inside(base_dir: Path, abs_path: Path) -> None:
    """防止路径穿越：结果必须落在下载根目录内"""
    try:
        base = Path(base_dir).resolve()
        target = abs_path.resolve()
    except OSError:
        return
    if target != base and base not in target.parents:
        raise TemplateError("模板解析出的路径超出下载目录范围")


def unique_path(path: Path) -> Path:
    """目标已存在时，追加 (1)(2)… 生成不冲突的新路径"""
    if not path.exists():
        return path
    stem, suffix = os.path.splitext(str(path))
    index = 1
    while True:
        candidate = Path(f"{stem} ({index}){suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def build_variables(video: Any, quality: str = "", ext: str = "mp4") -> Dict[str, str]:
    """
    从视频详情对象构造变量表

    任何字段缺失都退化为空串，保证模板不会因为个别字段解析失败而报错。
    """
    def _attr(name: str, default: Any = "") -> Any:
        value = getattr(video, name, default)
        return default if value is None else value

    studio = getattr(video, "studio", None)
    video_type = getattr(video, "video_type", None)
    tags = getattr(video, "tags", None) or []

    upload_date = _attr("upload_date", "")
    parsed_date: Optional[datetime] = None
    if isinstance(upload_date, datetime):
        parsed_date = upload_date
    elif isinstance(upload_date, str) and upload_date.strip():
        raw = upload_date.strip()[:19].replace("/", "-")
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m", "%Y"):
            try:
                parsed_date = datetime.strptime(raw, fmt)
                break
            except ValueError:
                continue

    variables: Dict[str, str] = {
        "title": str(_attr("title", "")).strip(),
        "subtitle": str(_attr("subtitle", "")).strip(),
        "series": str(_attr("series", "")).strip(),
        "studio": str(getattr(studio, "name", "") or "").strip(),
        "video_type": str(getattr(video_type, "name", "") or "").strip(),
        "video_id": str(_attr("video_id", "")).strip(),
        "tags": ",".join(str(getattr(tag, "name", "") or "") for tag in tags).strip(","),
        "duration": str(_attr("duration", "")).strip(),
        "quality": (quality or "").strip(),
        "ext": (ext or "mp4").lstrip(".").strip() or "mp4",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "upload_date": parsed_date.strftime("%Y-%m-%d") if parsed_date else "",
        "year": parsed_date.strftime("%Y") if parsed_date else "",
        "month": parsed_date.strftime("%m") if parsed_date else "",
        "day": parsed_date.strftime("%d") if parsed_date else "",
    }
    return variables


def sample_variables() -> Dict[str, str]:
    """用于前端预览的示例变量值"""
    return {item["key"]: item["sample"] for item in VARIABLES}
