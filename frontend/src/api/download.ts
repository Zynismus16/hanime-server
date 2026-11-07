import request from '../utils/request.ts';
import type {
  DownloadProgress,
  DownloadActionType,
  DownloadStartResult,
  DownloadSettings,
  DownloadCheckResult,
  PathPreview,
} from '../types/download';

/**
 * 下载相关API服务
 */
export const DownloadApi = {
  /**
   * 获取下载历史
   */
  getDownloadHistory: async (): Promise<DownloadProgress[]> => {
    try {
      const response = await request.get<DownloadProgress[]>('/downloads/history');
      return response.data;
    } catch (error) {
      console.error('获取下载历史失败:', error);
      return [];
    }
  },

  /**
   * 开始下载视频
   * @param videoId 视频ID
   * @param force 是否强制重新下载（二次确认后传 true）
   * @param options 本次下载的路径模板覆盖
   */
  startDownload: async (
    videoId: string,
    force: boolean = false,
    options: { subPath?: string; filename?: string } = {}
  ): Promise<DownloadStartResult> => {
    try {
      const response = await request.post<DownloadStartResult>('/downloads/start', {
        video_id: videoId,
        force,
        sub_path: options.subPath,
        filename: options.filename,
      });
      return response.data;
    } catch (error) {
      console.error('开始下载失败:', error);
      return { status: 'error', message: '开始下载失败' };
    }
  },

  /**
   * 下载前置检查：判断是否需要二次确认
   */
  checkDownload: async (videoId: string): Promise<DownloadCheckResult | null> => {
    try {
      const response = await request.post<DownloadCheckResult>('/downloads/check', {
        video_id: videoId,
      });
      return response.data;
    } catch (error) {
      console.error('下载检查失败:', error);
      return null;
    }
  },

  /**
   * 预览按模板生成的落盘路径
   */
  previewPath: async (
    videoId: string,
    options: { subPath?: string; filename?: string } = {}
  ): Promise<PathPreview | null> => {
    try {
      const response = await request.post<PathPreview>('/downloads/preview', {
        video_id: videoId,
        sub_path: options.subPath,
        filename: options.filename,
      });
      return response.data;
    } catch (error) {
      console.error('路径预览失败:', error);
      return null;
    }
  },

  /**
   * 获取下载命名设置
   */
  getSettings: async (): Promise<DownloadSettings | null> => {
    try {
      const response = await request.get<DownloadSettings>('/downloads/settings');
      return response.data;
    } catch (error) {
      console.error('获取下载设置失败:', error);
      return null;
    }
  },

  /**
   * 保存下载命名设置
   */
  saveSettings: async (
    subPathTemplate: string,
    filenameTemplate: string
  ): Promise<{ ok: boolean; message?: string; settings?: DownloadSettings }> => {
    try {
      const response = await request.put<DownloadSettings>('/downloads/settings', {
        sub_path_template: subPathTemplate,
        filename_template: filenameTemplate,
      });
      return { ok: true, settings: response.data };
    } catch (error: any) {
      const detail = error?.response?.data?.detail;
      return { ok: false, message: detail || '保存失败' };
    }
  },

  /**
   * 执行下载操作 (暂停/继续/取消/重试/删除)
   * @param videoId 视频ID
   * @param action 操作类型
   */
  handleDownloadAction: async (videoId: string, action: DownloadActionType) => {
    try {
      const response = await request.post('/downloads/action', {
        video_id: videoId,
        action
      });
      return response.data;
    } catch (error) {
      console.error(`${action}操作失败:`, error);
      return { status: 'error', message: `${action}操作失败` };
    }
  },

  /**
   * 获取API基础URL
   * @returns 返回API基础URL，如果是相对路径则返回完整URL
   */
  getBaseUrl: (): string => {
    const baseURL = request.defaults.baseURL || '';
    // 如果是相对路径，转换为绝对路径
    if (baseURL.startsWith('/')) {
      const protocol = window.location.protocol;
      const host = window.location.host;
      return `${protocol}//${host}${baseURL}`;
    }
    return baseURL;
  },

  /**
   * 获取已下载视频的访问链接
   * @param videoId 视频ID
   */
  getVideoFileUrl: (videoId: string): string => {
    return `/api/downloads/file/${videoId}`;
  },

  /**
   * 获取封面URL
   * 统一通过本地API获取，后端会自动处理：
   * - 如果本地存在，直接返回
   * - 如果不存在，实时下载后返回
   * @param videoId 视频ID
   */
  getCoverUrl: (videoId: string): string => {
    return `/api/downloads/cover/${videoId}`;
  },

  /**
   * 创建WebSocket连接以接收下载进度更新
   * @param onMessage 消息处理函数
   */
  createWebSocket: (onMessage: (data: DownloadProgress) => void): WebSocket => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const baseUrl = request.defaults.baseURL || '';
    const baseUrlObj = new URL(baseUrl);
    const wsPath = `${protocol}//${baseUrlObj.host || host}/api/downloads/ws`;
    
    const ws = new WebSocket(wsPath);
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as DownloadProgress;
        onMessage(data);
      } catch (error) {
        console.error('解析WebSocket消息失败:', error);
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket错误:', error);
    };
    
    return ws;
  },
  
  /**
   * 格式化文件大小
   * @param bytes 字节数
   */
  formatFileSize: (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },
  
  /**
   * 格式化下载速度
   * @param bytesPerSecond 每秒字节数
   */
  formatSpeed: (bytesPerSecond: number): string => {
    return `${DownloadApi.formatFileSize(bytesPerSecond)}/s`;
  }
}; 