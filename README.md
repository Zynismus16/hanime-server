# Han1me Server

<div align="center">
  <a href="https://github.com/heisenyu/hanime-server">
    <img src="img/logo.png" alt="Han1me Server Logo" width="120" style="margin-bottom: 20px;"/>
  </a>
  <br>
  
  [![GitHub Stars](https://img.shields.io/github/stars/heisenyu/hanime-server?style=flat&color=fc4c02)](https://github.com/heisenyu/hanime-server/stargazers)
  [![Docker Pulls](https://img.shields.io/docker/pulls/heisenyu/hanime-server?color=339933)](https://hub.docker.com/r/heisenyu/hanime-server)
  [![Docker Image Size](https://img.shields.io/docker/image-size/heisenyu/hanime-server)](https://hub.docker.com/r/heisenyu/hanime-server)

  <p>🎬 强大而简洁的Han1me视频浏览与下载解决方案</p>
</div>

<p align="center">
  <a href="#-功能特色">功能特色</a> •
  <a href="#-项目截图">项目截图</a> •
  <a href="#️-技术架构">技术架构</a> •
  <a href="#-部署指南">部署指南</a> •
  <a href="#-免责声明">免责声明</a> •
  <a href="#-许可证">许可证</a>
</p>


## 📜 项目简介

Han1me Server 是一个基于 Python 和 Vue.js 开发的全栈应用，用于浏览和播放 hanime 视频资源。项目采用前后端分离架构，后端使用 FastAPI 提供 RESTful API 接口，前端使用 Vue.js 构建响应式用户界面，支持多平台访问。

整个应用通过 Docker 容器化技术实现一键部署，大大简化了安装和使用流程。适合在NAS设备（如群晖、威联通等）上部署，可作为家庭媒体服务器使用，支持远程访问和视频管理。

> **关于作者**: 作者并非Vue开发者，前端主要借助Cursor AI辅助工具进行开发，如有不足之处，敬请谅解。
> 
> **项目灵感**: 本项目的页面布局和功能设计参考了 [YenalyLiew/Han1meViewer](https://github.com/YenalyLiew/Han1meViewer) Android端应用。由于原项目已标记为不再维护，促使我开发了这个基于Web的替代版本，让更多设备都能方便使用。本项目支持直接下载视频到NAS存储设备，便于媒体库集中管理和随时观看。

---

## <span id="-功能特色">✨ 功能特色</span>

<div align="center">
  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-bottom: 30px;">
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">🎬</div>
      <div><b>视频浏览</b></div>
      <div style="font-size: 14px;">首页推荐、分类浏览</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">🔍</div>
      <div><b>高级搜索</b></div>
      <div style="font-size: 14px;">多条件组合查询</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">🌙</div>
      <div><b>暗黑模式切换</b></div>
      <div style="font-size: 14px;">支持明暗主题切换</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">📥</div>
      <div><b>下载管理</b></div>
      <div style="font-size: 14px;">批量下载与管理</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">💬</div>
      <div><b>视频评论</b></div>
      <div style="font-size: 14px;">查看社区反馈</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">🎮</div>
      <div><b>视频播放</b></div>
      <div style="font-size: 14px;">流畅播放体验</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">📱</div>
      <div><b>响应式设计</b></div>
      <div style="font-size: 14px;">适配多种设备</div>
    </div>
    <div style="text-align: center; width: 200px;">
      <div style="font-size: 32px;">🖥️</div>
      <div><b>NAS 部署</b></div>
      <div style="font-size: 14px;">家庭媒体中心</div>
    </div>
  </div>
</div>

## <span id="-项目截图">📷 项目截图</span>

<table border="0" width="100%">
  <tr>
    <td width="50%" align="center">
      <img src="img/主页.png" alt="主页" width="100%" style="border-radius: 8px;">
      <br><b>主页</b><br>展示推荐内容和分类
    </td>
    <td width="50%" align="center">
      <img src="img/视频详情页.png" alt="视频详情页" width="100%" style="border-radius: 8px;">
      <br><b>视频详情页</b><br>播放器和相关信息
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="img/搜索页.png" alt="搜索页" width="100%" style="border-radius: 8px;">
      <br><b>搜索页</b><br>快速找到想要的内容
    </td>
    <td width="50%" align="center">
      <img src="img/高级搜索.png" alt="高级搜索" width="100%" style="border-radius: 8px;">
      <br><b>高级搜索</b><br>多条件筛选
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="img/下载页.png" alt="下载页" width="100%" style="border-radius: 8px;">
      <br><b>下载页</b><br>管理下载任务
    </td>
    <td width="50%" align="center">
      <img src="img/手机端下载页示例.png" alt="手机端下载页示例" width="50%" style="border-radius: 8px;">
      <br><b>手机端适配</b><br>移动设备完美支持
    </td>
  </tr>
</table>

## <span id="️-技术架构">🛠️ 技术架构</span>

<div align="center">
  <table>
    <tr>
      <th>后端技术</th>
      <th>前端技术</th>
    </tr>
    <tr>
      <td>
        <ul>
          <li>Python 3.10</li>
          <li>FastAPI 框架</li>
          <li>SQLite 数据存储</li>
          <li>异步下载服务</li>
          <li>视频元数据服务</li>
          <li>Cloudflare 绕过实现</li>
          <li>LRU缓存优化</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>Vue.js 框架</li>
          <li>TypeScript 类型支持</li>
          <li>Vite 构建工具</li>
          <li>Vue Router 路由管理</li>
          <li>Pinia 状态管理</li>
          <li>Plyr 视频播放器组件</li>
          <li>响应式布局设计</li>
        </ul>
      </td>
    </tr>
  </table>
</div>

### 核心组件

- **下载服务**: 管理视频下载队列、状态跟踪和错误处理
- **视频服务**: 提供视频搜索、元数据解析和内容推荐
- **数据缓存**: 优化性能和减少网络请求
- **Cloudflare绕过**: 解决访问限制问题
- **Plyr播放器**: 提供流畅的视频播放体验
- **路径模板**: 自定义下载子路径与文件名，支持元数据变量

## 📁 下载命名规则（自定义子路径 / 文件名）

下载文件的落盘位置由两个模板决定，模板中可以使用视频元数据变量：

| 设置项 | 默认值 | 说明 |
|---|---|---|
| 子路径模板 | 空 | 相对下载根目录的层级，用 `/` 分隔，例如 `{studio}/{series}` |
| 文件名模板 | `{video_id}_{title}` | 只需写文件名主体，缺省自动补 `.mp4` |

**入口**：下载管理页 → 「命名设置」；单次下载可在视频详情页用「下载到…」临时覆盖。

### 可用变量

| 变量 | 含义 | 变量 | 含义 |
|---|---|---|---|
| `{title}` | 视频标题 | `{video_id}` | 视频 ID |
| `{subtitle}` | 副标题 | `{studio}` | 发行商 / 上传者 |
| `{series}` | 系列名 | `{video_type}` | 视频类型 |
| `{tags}` | 标签（逗号分隔） | `{quality}` | 清晰度，如 1080p |
| `{upload_date}` | 发布日期 `YYYY-MM-DD` | `{year}` / `{month}` / `{day}` | 发布年 / 月 / 日 |
| `{date}` | 下载当天日期 | `{duration}` | 时长 |
| `{ext}` | 扩展名（不含点） | | |

`${title}` 与 `{title}` 两种写法等价。

### 行为约定

- **空变量自动折叠**：`{series}` 解析不到时，该层目录直接省略，不会产生 `//` 或空目录；
- **非法字符清洗**：`<>:"/\|?*`、控制字符、Windows 保留名（CON/PRN/…）、超长文件名都会自动处理；
- **越界保护**：模板解析结果必须落在下载根目录内，`..` 会被拒绝；
- **同名不覆盖**：目标文件已存在时自动追加 ` (1)`、` (2)`，绝不覆盖已有文件；
- **记录入库**：每条下载都会把「子路径 / 相对路径 / 变量快照」写入 SQLite，旧库启动时自动补列迁移。

### 重复下载二次确认

点击下载时，后端会先判断该视频是否**已在下载列表**（下载中 / 等待 / 已暂停）或**已下载完成**：

- 命中则返回 `status=conflict`，前端弹出确认框并展示「当前状态 / 进度 / 已有文件路径」；
- 用户确认后前端带 `force=true` 重新请求，才会取消旧任务、删除旧文件并重新下载；
- 下载失败或已取消的记录不拦截，可直接重下。

相关接口：

```
GET  /api/downloads/settings   获取命名设置与可用变量
PUT  /api/downloads/settings   保存命名设置（校验未知变量 / 路径穿越）
POST /api/downloads/check      下载前置检查（是否需要二次确认）
POST /api/downloads/preview    按模板预览真实落盘路径
POST /api/downloads/start      开始下载（支持 sub_path / filename / force）
```

## 📝 开发计划

> **当前状态**: 本项目已完成基础功能开发，包括视频浏览、搜索、播放、下载等核心功能，可以满足日常使用需求。

TODO：

- [ ] **新番列表**: 展示最新更新的内容
- [ ] **设置页面**: 用户偏好设置与系统配置
- [ ] **清单列表**: 包括稍后观看、喜欢的影片、播放清单等
- [ ] **观看历史**: 记录和管理已观看内容

> 随缘更新，有需要的话可以自行开发。欢迎提交Issue或PR！

## <span id="-部署指南">🚀 部署指南</span>

### Docker 部署（推荐）

本仓库相对上游增加了**下载命名模板、下载记录入库、重复下载二次确认**等改造，镜像需要从本地源码构建。

#### 1. 准备代码与环境变量

```bash
git clone https://github.com/Zynismus16/hanime-server.git
cd hanime-server
cp .env.example .env
```

编辑 `.env`，至少确认代理配置（元数据抓取要访问 hanime1.me，国内网络需要代理）：

```ini
USE_PROXY=True
PROXY_URL=http://192.168.1.2:7890
```

> 视频下载默认直连 CDN，`USE_DOWNLOAD_PROXY` 保持 `False` 即可；下载慢再打开。

#### 2. 启动

```bash
docker compose up -d --build
```

首次构建约 3-8 分钟（前端 Node 构建 + Python 依赖安装）。完成后访问：

- 前端界面：http://localhost:7788
- 健康检查：http://localhost:7788/api/health

```bash
docker compose ps          # STATUS 显示 healthy 即就绪
docker compose logs -f app # 查看启动日志
```

#### 3. 目录与持久化

| 宿主机 | 容器内 | 内容 |
|---|---|---|
| `./data/downloads` | `/app/backend/downloads` | 视频文件、`covers/` 封面 |
| `./data/db` | `/app/backend/db` | `downloads.db`（下载记录 + 命名设置） |
| `./data/logs` | `/app/backend/logs` | `USE_LOG_FILE=true` 时的滚动日志 |

三个目录首次启动自动创建，迁移机器时整目录拷走即可。

命名规则有两个来源，**页面设置优先**：

1. 页面「下载管理 → 命名设置」，保存在 SQLite；
2. `.env` 中的 `DOWNLOAD_SUB_PATH_TEMPLATE` / `DOWNLOAD_FILENAME_TEMPLATE`，作为初始默认值。

变量说明见上文「📁 下载命名规则（自定义子路径 / 文件名）」。

#### 4. 常用操作

```bash
docker compose logs -f app        # 实时日志
docker compose down               # 停止（./data 保留）
docker compose up -d --build      # 改代码后重建
```

- 改端口：`.env` 中加 `APP_PORT=8899`。
- 换官方镜像：注释 compose 里的 `build:`，`image:` 改为 `heisenyu/hanime-server:latest`（注意官方镜像**不含**本仓库的下载改造）。
- 只想跑后端调试：`docker compose run --rm --service-ports app bash`。

#### 5. 注意事项

- 容器内 nginx 与后端均以 root 运行，`./data` 下文件属主为 root。需要非 root 属主时执行 `sudo chown -R 1000:1000 data`。
- `cf-bypass` 镜像来自 ghcr.io，拉取失败时先单独 `docker pull ghcr.io/sarperavci/cloudflarebypassforscraping:latest`，或给 Docker 配置镜像加速。
- 首次访问需要过 Cloudflare 5 秒盾，等待 5-10 秒属正常，凭证会缓存。
- 容器停止时先收到 SIGTERM，正在进行的下载会中断并在下次启动时按 `downloading` 状态自动续传。

### NAS 部署指南

同一份 `docker-compose.yml` 可直接用于 NAS：

- **群晖 Synology**：套件中心安装 Container Manager →「项目」→ 新建 → 选择本仓库目录下的 `docker-compose.yml`；或 SSH 进 NAS 后在该目录执行 `docker compose up -d --build`。下载目录建议改成 `/volume1/media/anime:/app/backend/downloads`。
- **威联通 QNAP**：Container Station →「应用程序」→ 创建 → 粘贴 compose 内容，同样按需替换 `./data/*` 为共享文件夹路径。
- 其他系统只要支持 Docker + Compose v2 即可。

NAS 上注意两点：

1. 构建需要拉取 node/python 基础镜像和依赖，网络差时先在别的机器 `docker save` 再导入。
2. 下载目录若指向已有媒体库，建议单独建子目录，避免命名清洗规则影响其他文件。

### 手动部署

#### 后端部署
1. 进入 backend 目录
2. 安装依赖：`pip install -r requirements.txt`
3. 运行服务器：`python main.py`

通过 http://localhost:8000/docs 访问 API 文档

#### 前端部署
1. 进入 frontend 目录
2. 安装依赖：`npm install`
3. 开发模式：`npm run dev`
4. 构建生产版：`npm run build`

通过 http://localhost:7788 访问前端页面

## <span id="-免责声明">⚠️ 免责声明</span>

本应用程序（以下简称"本应用"）与原站点及其关联方无任何隶属、合作或授权关系，特此声明如下：

### 🔍 数据来源

本应用通过合法技术手段仅获取目标网站公开显示的信息，不涉及：

* 🔒 用户账户等隐私数据
* 🛑 网站后端数据库访问
* ⚠️ 任何形式的注入攻击

### ⚖️ 使用限制

本应用提供的所有内容仅用于：

* 📚 技术研究学习
* ✨ 用户体验优化
* 🚫 非商业用途展示

### ©️ 版权归属

原始视频/图文内容版权均归原始网站或内容制作/发行方所有，本应用:

* 💾 不存储任何版权内容（除用户主动下载）
* ✂️ 不修改原始内容
* 🏷️ 不声称拥有内容所有权

### 🛡️ 责任豁免

使用者应知晓：

* ⏳ 本应用不保证数据的完整性和实时性
* 🙅‍♂️ 使用产生的一切后果由用户自行承担
* ⛔ 不得用于非法用途

## <span id="-许可证">📄 许可证</span>

本项目采用 Apache License Version 2.0 许可证，详细条款请参阅项目根目录下的 LICENSE 文件。

主要条款包括：
- 允许商用、修改、分发和私有使用
- 要求保留版权声明和许可证文件
- 提供修改说明（如有）
- 不提供质量担保
- 不承担用户使用风险

---

<div align="center">
  <p>ℹ️ 温馨提示：建议通过官方渠道支持原站内容，并点击广告以支持网站运营者。</p>
  <p>🌟 如果您喜欢这个项目，请考虑给它点个星！</p>
</div>