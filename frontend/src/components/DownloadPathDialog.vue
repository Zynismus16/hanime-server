<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="handleVisibleChange"
    :title="mode === 'settings' ? '下载命名设置' : '自定义下载位置'"
    width="680px"
    append-to-body
    destroy-on-close
    class="download-path-dialog"
  >
    <div class="dp-body">
      <p class="dp-tip">
        <template v-if="mode === 'settings'">
          设置所有下载任务的默认命名规则。点击下方变量可插入到当前输入框。
        </template>
        <template v-else>
          仅对本次下载生效；留空则使用「下载管理 → 命名设置」中的默认规则。
        </template>
      </p>

      <div class="dp-field">
        <label class="dp-label">子路径模板</label>
        <el-input
          ref="subPathInputRef"
          v-model="subPath"
          placeholder="留空表示放在下载根目录，例如：{studio}/{series}"
          clearable
          @focus="activeField = 'sub'"
        />
        <span class="dp-hint">用 / 分隔层级；变量为空时该层级自动省略</span>
      </div>

      <div class="dp-field">
        <label class="dp-label">文件名模板</label>
        <el-input
          ref="filenameInputRef"
          v-model="filename"
          placeholder="{video_id}_{title}"
          clearable
          @focus="activeField = 'name'"
        />
        <span class="dp-hint">无需写扩展名，缺省自动补 .mp4</span>
      </div>

      <div class="dp-vars">
        <span class="dp-vars-label">可用变量</span>
        <div class="dp-vars-list">
          <el-tag
            v-for="item in variables"
            :key="item.key"
            size="small"
            class="dp-var"
            :title="`${item.label}（示例：${item.sample}）`"
            @click="insertVariable(item.key)"
          >
            {{ item.label }}
          </el-tag>
        </div>
      </div>

      <div class="dp-preview">
        <div class="dp-preview-head">
          <span>预览</span>
          <span v-if="previewLoading" class="dp-preview-loading">解析中…</span>
        </div>
        <code class="dp-preview-path">{{ previewPathText }}</code>
        <div v-if="previewExists" class="dp-preview-warn">
          目标位置已存在同名文件，下载时会自动重命名，不会覆盖
        </div>
        <div v-if="previewTip" class="dp-preview-tip">{{ previewTip }}</div>
      </div>

      <div v-if="examples && examples.length" class="dp-examples">
        <span class="dp-examples-label">快速套用：</span>
        <a v-for="example in examples" :key="example.name" class="dp-example" @click="applyExample(example)">
          {{ example.name }}
        </a>
      </div>
    </div>

    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button v-if="mode === 'settings'" @click="restoreDefault">恢复默认</el-button>
      <el-button type="primary" :loading="submitting" @click="submit">
        {{ mode === 'settings' ? '保存' : '开始下载' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { ElMessage } from 'element-plus';
import { DownloadApi } from '../api/download';
import type { DownloadSettings, DownloadTemplateExample } from '../types/download';

interface Props {
  modelValue: boolean;
  /** settings: 全局命名设置；download: 单次自定义下载位置 */
  mode?: 'settings' | 'download';
  /** download 模式下必填：用于解析真实路径 */
  videoId?: string;
  /** 打开时的初始值 */
  initialSubPath?: string;
  initialFilename?: string;
  /** 是否已加载好设置（避免重复请求） */
  settings?: DownloadSettings | null;
}

const props = withDefaults(defineProps<Props>(), {
  mode: 'settings',
  videoId: '',
  initialSubPath: '',
  initialFilename: '',
  settings: null,
});

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
  submit: [payload: { subPath: string; filename: string }];
  saved: [payload: { subPath: string; filename: string }];
}>();

const subPath = ref(props.initialSubPath);
const filename = ref(props.initialFilename);
const activeField = ref<'sub' | 'name'>('name');
const subPathInputRef = ref<any>(null);
const filenameInputRef = ref<any>(null);

const variables = ref<DownloadSettings['variables']>(props.settings?.variables || []);
const examples = ref<DownloadTemplateExample[]>(props.settings?.examples || []);

const submitting = ref(false);
const previewLoading = ref(false);
const previewPathText = ref('');
const previewExists = ref(false);
const previewTip = ref('');

/** 本地渲染（设置模式没有具体视频，用变量示例值模拟） */
const localPreview = computed(() => {
  const samples: Record<string, string> = {};
  variables.value.forEach((item) => (samples[item.key] = item.sample));

  const render = (template: string) =>
    (template || '').replace(/\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\{([A-Za-z_][A-Za-z0-9_]*)\}/g, (_, a, b) => {
      const key = a || b;
      return samples[key] ?? '';
    });

  const segs = render(subPath.value)
    .split('/')
    .map((s) => s.trim())
    .filter(Boolean)
    .map((s) => s.replace(/[<>:"\\|?*\x00-\x1f]/g, '_').replace(/\s+/g, ' ').trim())
    .filter((s) => s && s !== '.' && s !== '..');

  let name = render(filename.value).trim();
  if (!name) name = '未命名';
  if (!/\.(mp4|mkv|ts|flv|avi|mov|webm|m4v)$/i.test(name)) name += '.mp4';

  return [...segs, name].join('/');
});

/** 设置模式：本地模拟预览；下载模式：请求后端按真实视频信息解析 */
async function refreshPreview() {
  if (props.mode === 'settings') {
    previewPathText.value = localPreview.value;
    previewExists.value = false;
    previewTip.value = '以上为示例值，实际路径会按每个视频的信息生成';
    return;
  }

  if (!props.videoId) return;

  previewLoading.value = true;
  try {
    const result = await DownloadApi.previewPath(props.videoId, {
      subPath: subPath.value,
      filename: filename.value,
    });
    if (result) {
      previewPathText.value = result.rel_path;
      previewExists.value = result.exists;
      previewTip.value = `实际落盘：${result.absolute_path}`;
    } else {
      previewPathText.value = localPreview.value;
      previewTip.value = '预览失败，以上为本地估算结果';
    }
  } finally {
    previewLoading.value = false;
  }
}

let previewTimer: ReturnType<typeof setTimeout> | null = null;
watch([subPath, filename], () => {
  if (previewTimer) clearTimeout(previewTimer);
  previewTimer = setTimeout(refreshPreview, 350);
});

/** 设置只加载一次，避免每次打开弹窗都打后端 */
const loadedSettings = ref<DownloadSettings | null>(props.settings);

async function ensureSettings(): Promise<DownloadSettings | null> {
  if (loadedSettings.value && variables.value.length) {
    return loadedSettings.value;
  }
  const fetched = props.settings || (await DownloadApi.getSettings());
  if (fetched) {
    loadedSettings.value = fetched;
    variables.value = fetched.variables || [];
    examples.value = fetched.examples || [];
  }
  return loadedSettings.value;
}

watch(
  () => props.modelValue,
  async (visible) => {
    if (!visible) return;
    const settings = await ensureSettings();
    subPath.value = props.initialSubPath || settings?.sub_path_template || '';
    filename.value = props.initialFilename || settings?.filename_template || '';
    previewExists.value = false;
    previewTip.value = '';
    refreshPreview();
  }
);

function insertVariable(key: string) {
  const token = `{${key}}`;
  const target = activeField.value === 'sub' ? subPathInputRef.value : filenameInputRef.value;
  const model = activeField.value === 'sub' ? subPath : filename;
  const el: HTMLInputElement | undefined = target?.input;

  if (el && typeof el.selectionStart === 'number' && document.activeElement === el) {
    const start = el.selectionStart;
    const end = el.selectionEnd ?? start;
    model.value = `${model.value.slice(0, start)}${token}${model.value.slice(end)}`;
    requestAnimationFrame(() => {
      el.focus();
      el.setSelectionRange(start + token.length, start + token.length);
    });
  } else {
    model.value = `${model.value}${token}`;
  }
}

function applyExample(example: DownloadTemplateExample) {
  subPath.value = example.sub_path;
  filename.value = example.filename;
}

function restoreDefault() {
  subPath.value = '';
  filename.value = '{video_id}_{title}';
}

function handleVisibleChange(visible: boolean) {
  emit('update:modelValue', visible);
}

function close() {
  emit('update:modelValue', false);
}

async function submit() {
  if (props.mode === 'download') {
    emit('submit', { subPath: subPath.value.trim(), filename: filename.value.trim() });
    emit('update:modelValue', false);
    return;
  }

  if (!filename.value.trim()) {
    ElMessage.warning('文件名模板不能为空');
    return;
  }

  submitting.value = true;
  try {
    const result = await DownloadApi.saveSettings(subPath.value.trim(), filename.value.trim());
    if (result.ok) {
      const savedSub = result.settings?.sub_path_template ?? subPath.value.trim();
      const savedName = result.settings?.filename_template ?? filename.value.trim();
      // 更新本地缓存，避免下次打开弹窗还显示旧值
      loadedSettings.value = {
        sub_path_template: savedSub,
        filename_template: savedName,
        variables: variables.value,
        examples: examples.value,
      };
      ElMessage.success('命名设置已保存');
      emit('saved', { subPath: savedSub, filename: savedName });
      emit('update:modelValue', false);
    } else {
      ElMessage.error(result.message || '保存失败');
    }
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.dp-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.dp-tip {
  margin: 0;
  font-size: 13px;
  color: var(--text-secondary, #909399);
  line-height: 1.6;
}

.dp-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.dp-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary, #e5e7eb);
}

.dp-hint {
  font-size: 12px;
  color: var(--text-secondary, #909399);
}

.dp-vars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.dp-vars-label {
  font-size: 13px;
  font-weight: 600;
}

.dp-vars-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.dp-var {
  cursor: pointer;
  user-select: none;
}

.dp-preview {
  border: 1px dashed var(--border-color, #3f3f46);
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: rgba(127, 127, 127, 0.06);
}

.dp-preview-head {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-secondary, #909399);
}

.dp-preview-path {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 13px;
  word-break: break-all;
  color: var(--primary-color, #409eff);
}

.dp-preview-warn {
  font-size: 12px;
  color: #e6a23c;
}

.dp-preview-tip {
  font-size: 12px;
  color: var(--text-secondary, #909399);
  word-break: break-all;
}

.dp-examples {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  font-size: 12px;
}

.dp-examples-label {
  color: var(--text-secondary, #909399);
}

.dp-example {
  color: var(--primary-color, #409eff);
  cursor: pointer;
}
</style>
