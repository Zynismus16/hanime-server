/**
 * 下载相关类型定义
 */

// 下载操作类型
export type DownloadActionType = 'pause' | 'resume' | 'cancel' | 'retry' | 'delete';

// 下载状态类型
export type DownloadStatus = 'pending' | 'downloading' | 'paused' | 'completed' | 'cancelled' | 'error';

// 下载分段类型
export interface DownloadSegment {
  start: number;
  end: number;
  downloaded: number;
  status: string;
}

// 下载进度类型
export interface DownloadProgress {
  video_id: string;
  filename: string;
  title?: string;
  cover_url?: string;
  total_size: number;
  downloaded: number;
  status: DownloadStatus;
  speed: number;
  error_message?: string;
  url: string;
  created_at: string;
  completed_at?: string;
  retry_count: number;
  max_retries: number;
  segments?: DownloadSegment[];
  /** 自定义子路径（相对下载根目录） */
  sub_path?: string;
  /** 自定义相对路径（含文件名） */
  rel_path?: string;
  /** 生成路径时使用的变量快照 */
  variables?: Record<string, string>;
  /** 历史记录中：文件是否仍存在于磁盘 */
  exists?: boolean;
}

// 下载请求类型
export interface DownloadRequest {
  video_id: string;
  sub_path?: string;
  filename?: string;
  force?: boolean;
}

// 下载操作请求类型
export interface DownloadAction {
  video_id: string;
  action: DownloadActionType;
}

// 下载冲突类型
export type DownloadConflictType = 'in_progress' | 'completed' | 'completed_missing' | 'file_exists';

// 下载冲突信息（用于二次确认）
export interface DownloadConflict {
  type: DownloadConflictType;
  title?: string;
  message: string;
  detail?: string;
  existing_status?: string;
  existing_progress?: number;
  existing_size?: number;
  rel_path?: string;
}

// 开始下载的返回结果
export interface DownloadStartResult {
  status: 'success' | 'conflict' | 'error';
  message?: string;
  video_id?: string;
  rel_path?: string;
  renamed?: boolean;
  conflict?: DownloadConflict;
}

// 模板变量说明
export interface DownloadTemplateVariable {
  key: string;
  label: string;
  sample: string;
}

// 模板示例
export interface DownloadTemplateExample {
  name: string;
  sub_path: string;
  filename: string;
}

// 下载命名设置
export interface DownloadSettings {
  sub_path_template: string;
  filename_template: string;
  variables: DownloadTemplateVariable[];
  examples?: DownloadTemplateExample[];
}

// 路径预览
export interface PathPreview {
  sub_path: string;
  filename: string;
  rel_path: string;
  absolute_path: string;
  exists: boolean;
  variables: Record<string, string>;
}

// 下载前置检查结果
export interface DownloadCheckResult {
  has_conflict: boolean;
  conflict: DownloadConflict | null;
  existing?: DownloadProgress | null;
  settings: DownloadSettings;
}

// 下载操作响应类型
export interface DownloadResponse {
  status: 'success' | 'conflict' | 'error';
  message?: string;
  video_id?: string;
  existing_download?: DownloadProgress;
}
