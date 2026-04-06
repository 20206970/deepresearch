# LangGraph 科研助手前端实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 Vue 3 前端应用，配合后端 LangGraph 工作流，提供分步式研究向导界面

**Architecture:** 单页应用，4 步骤向导流程，使用 axios 调用后端 API，marked + highlight.js 渲染 Markdown

**Tech Stack:** Vue 3 (Composition API), Vite, axios, marked, highlight.js

---

### Task 1: 初始化 Vue 3 项目

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/style.css`

- [ ] **Step 1: 创建 package.json**

```json
{
  "name": "langgraph-research-frontend",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "axios": "^1.6.0",
    "marked": "^12.0.0",
    "highlight.js": "^11.9.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

- [ ] **Step 2: 创建 vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/research': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: 创建 index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LangGraph 深度研究助手</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Serif+SC:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

- [ ] **Step 4: 创建 main.js**

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

createApp(App).mount('#app')
```

- [ ] **Step 5: 创建 style.css (全局样式)**

```css
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --accent: #3b82f6;
  --accent-hover: #60a5fa;
  --success: #22c55e;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --border: #334155;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  --radius-lg: 12px;
  --radius-md: 8px;
  --radius-sm: 4px;
  --transition: 300ms ease-in-out;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  min-height: 100vh;
  line-height: 1.6;
}

h1, h2, h3 {
  font-family: 'Noto Serif SC', serif;
}

code, pre {
  font-family: 'JetBrains Mono', monospace;
}

button {
  cursor: pointer;
  font-family: inherit;
  transition: var(--transition);
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}
```

- [ ] **Step 6: 创建 App.vue (主组件框架)**

```vue
<script setup>
import { ref } from 'vue'
import ProgressBar from './components/ProgressBar.vue'
import StepInput from './components/StepInput.vue'
import StepTasks from './components/StepTasks.vue'
import StepResearch from './components/StepResearch.vue'
import StepReport from './components/StepReport.vue'

const currentStep = ref(1)
const topic = ref('')
const tasks = ref([])
const taskResults = ref([])
const report = ref('')
const isLoading = ref(false)

const handleTopicSubmit = (data) => {
  topic.value = data.topic
  tasks.value = data.tasks
  currentStep.value = 2
}

const handleTasksConfirm = () => {
  currentStep.value = 3
}

const handleResearchComplete = (results) => {
  taskResults.value = results
  currentStep.value = 4
}

const handleReportGenerated = (reportData) => {
  report.value = reportData
}

const handleReset = () => {
  currentStep.value = 1
  topic.value = ''
  tasks.value = []
  taskResults.value = []
  report.value = ''
}
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🔬 LangGraph 深度研究助手</h1>
    </header>

    <ProgressBar :currentStep="currentStep" :totalSteps="4" />

    <main class="main">
      <StepInput
        v-if="currentStep === 1"
        @submit="handleTopicSubmit"
        :isLoading="isLoading"
      />

      <StepTasks
        v-else-if="currentStep === 2"
        :tasks="tasks"
        :topic="topic"
        @confirm="handleTasksConfirm"
        @back="currentStep = 1"
        :isLoading="isLoading"
      />

      <StepResearch
        v-else-if="currentStep === 3"
        :tasks="tasks"
        :topic="topic"
        @complete="handleResearchComplete"
        @report="handleReportGenerated"
        @back="currentStep = 2"
        :isLoading="isLoading"
        @update:loading="isLoading = $event"
      />

      <StepReport
        v-else-if="currentStep === 4"
        :report="report"
        :tasks="tasks"
        :topic="topic"
        @reset="handleReset"
      />
    </main>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  padding: 32px 24px 16px;
}

.header h1 {
  font-size: 1.75rem;
  color: var(--text-primary);
}

.main {
  flex: 1;
  padding: 24px;
}
</style>
```

- [ ] **Step 7: 提交**

```bash
cd /d/coding/hello-agents/code/chapter14/.worktrees/langgraph-deepresearch/code/chapter14/langgraph-deepresearch
git add frontend/
git commit -m "feat: scaffold Vue 3 project structure"
```

---

### Task 2: 创建 API 模块和进度条组件

**Files:**
- Create: `frontend/src/api/research.js`
- Create: `frontend/src/components/ProgressBar.vue`

- [ ] **Step 1: 创建 research.js API 模块**

```javascript
import axios from 'axios'

const API_BASE = '/research'

export async function createResearch(topic) {
  const response = await axios.post(API_BASE, { topic }, {
    timeout: 120000
  })
  return response.data
}
```

- [ ] **Step 2: 创建 ProgressBar.vue**

```vue
<script setup>
defineProps({
  currentStep: {
    type: Number,
    required: true
  },
  totalSteps: {
    type: Number,
    default: 4
  }
})

const steps = ['主题输入', '任务规划', '研究执行', '报告生成']
</script>

<template>
  <div class="progress-bar">
    <div class="steps">
      <div
        v-for="(step, index) in steps"
        :key="index"
        class="step"
        :class="{
          'completed': index + 1 < currentStep,
          'current': index + 1 === currentStep,
          'pending': index + 1 > currentStep
        }"
      >
        <div class="step-indicator">
          <span v-if="index + 1 < currentStep" class="check">✓</span>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <span class="step-label">{{ step }}</span>
        <div v-if="index < totalSteps - 1" class="step-line"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.progress-bar {
  padding: 16px 24px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
}

.steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  max-width: 600px;
  margin: 0 auto;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}

.step:last-child .step-line {
  display: none;
}

.step-indicator {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
  border: 2px solid var(--border);
  background: var(--bg-primary);
  transition: var(--transition);
  z-index: 1;
}

.step.completed .step-indicator {
  background: var(--success);
  border-color: var(--success);
  color: white;
}

.step.current .step-indicator {
  background: var(--accent);
  border-color: var(--accent);
  color: white;
  animation: pulse 2s infinite;
}

.step-label {
  margin-top: 8px;
  font-size: 0.75rem;
  color: var(--text-secondary);
  text-align: center;
}

.step.completed .step-label,
.step.current .step-label {
  color: var(--text-primary);
}

.step-line {
  position: absolute;
  top: 18px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: var(--border);
}

.step.completed .step-line {
  background: var(--success);
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(59, 130, 246, 0); }
}

@media (max-width: 640px) {
  .step-label {
    font-size: 0.625rem;
  }
  .step-indicator {
    width: 28px;
    height: 28px;
    font-size: 0.75rem;
  }
  .step-line {
    top: 14px;
  }
}
</style>
```

- [ ] **Step 3: 提交**

```bash
git add frontend/src/api/research.js frontend/src/components/ProgressBar.vue
git commit -m "feat: add API module and ProgressBar component"
```

---

### Task 3: 创建步骤 1 组件 (StepInput)

**Files:**
- Create: `frontend/src/components/StepInput.vue`

- [ ] **Step 1: 创建 StepInput.vue**

```vue
<script setup>
import { ref } from 'vue'
import { createResearch } from '../api/research.js'

const emit = defineEmits(['submit'])

const topic = ref('')
const isLoading = ref(false)
const error = ref('')

const handleSubmit = async () => {
  if (topic.value.trim().length < 2) {
    error.value = '请输入至少 2 个字符的研究主题'
    return
  }

  error.value = ''
  isLoading.value = true

  try {
    const data = await createResearch(topic.value)
    emit('submit', {
      topic: topic.value,
      tasks: data.todo_items || []
    })
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '请求失败，请重试'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="step-input">
    <div class="card">
      <h2>开始您的研究</h2>
      <p class="description">输入您想深入了解的主题，AI 将为您规划任务并生成研究报告</p>

      <div class="input-group">
        <textarea
          v-model="topic"
          placeholder="输入您想研究的主题..."
          :disabled="isLoading"
          @keydown.enter.ctrl="handleSubmit"
        ></textarea>
      </div>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <button
        class="btn-primary"
        :disabled="isLoading || topic.trim().length < 2"
        @click="handleSubmit"
      >
        <span v-if="isLoading" class="spinner"></span>
        <span v-else>开始研究</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.step-input {
  max-width: 600px;
  margin: 0 auto;
}

.card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow);
}

.card h2 {
  font-size: 1.5rem;
  margin-bottom: 8px;
  text-align: center;
}

.description {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 24px;
  font-size: 0.875rem;
}

.input-group {
  margin-bottom: 16px;
}

textarea {
  width: 100%;
  min-height: 120px;
  padding: 16px;
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 1rem;
  resize: vertical;
  transition: var(--transition);
}

textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-bottom: 16px;
  padding: 8px 12px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: var(--radius-sm);
}

.btn-primary {
  width: 100%;
  padding: 14px 24px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary:hover:not(:disabled) {
  background: var(--accent-hover);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/components/StepInput.vue
git commit -m "feat: add StepInput component"
```

---

### Task 4: 创建步骤 2 组件 (StepTasks)

**Files:**
- Create: `frontend/src/components/StepTasks.vue`

- [ ] **Step 1: 创建 StepTasks.vue**

```vue
<script setup>
import { ref } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    default: () => []
  },
  topic: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['confirm', 'back'])

const expandedTask = ref(null)

const toggleTask = (index) => {
  expandedTask.value = expandedTask.value === index ? null : index
}
</script>

<template>
  <div class="step-tasks">
    <div class="card">
      <h2>研究任务规划</h2>
      <p class="description">
        主题: <strong>{{ topic }}</strong>
      </p>

      <div class="tasks-list" v-if="tasks.length > 0">
        <div
          v-for="(task, index) in tasks"
          :key="index"
          class="task-card"
          :class="{ expanded: expandedTask === index }"
          @click="toggleTask(index)"
        >
          <div class="task-header">
            <span class="task-number">{{ index + 1 }}</span>
            <div class="task-info">
              <h3>{{ task.title }}</h3>
              <p class="task-intent">{{ task.intent }}</p>
            </div>
            <span class="expand-icon">{{ expandedTask === index ? '−' : '+' }}</span>
          </div>

          <div v-if="expandedTask === index" class="task-details">
            <span class="query-label">检索关键词:</span>
            <span class="query-tag">{{ task.query }}</span>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <p>暂无任务数据</p>
      </div>

      <div class="actions">
        <button class="btn-secondary" @click="emit('back')">上一步</button>
        <button class="btn-primary" @click="emit('confirm')">执行任务</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.step-tasks {
  max-width: 700px;
  margin: 0 auto;
}

.card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow);
}

.card h2 {
  font-size: 1.5rem;
  margin-bottom: 8px;
  text-align: center;
}

.description {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 24px;
}

.description strong {
  color: var(--accent);
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.task-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 16px;
  cursor: pointer;
  transition: var(--transition);
}

.task-card:hover {
  border-color: var(--accent);
}

.task-card.expanded {
  border-color: var(--accent);
}

.task-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.task-number {
  width: 28px;
  height: 28px;
  background: var(--accent);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}

.task-info {
  flex: 1;
}

.task-info h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 4px;
  font-family: 'Inter', sans-serif;
}

.task-intent {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.expand-icon {
  color: var(--text-secondary);
  font-size: 1.25rem;
  line-height: 1;
}

.task-details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.query-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-right: 8px;
}

.query-tag {
  display: inline-block;
  padding: 4px 10px;
  background: rgba(59, 130, 246, 0.15);
  color: var(--accent);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
}

.empty-state {
  text-align: center;
  padding: 32px;
  color: var(--text-secondary);
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary, .btn-secondary {
  padding: 12px 24px;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  flex: 1;
  max-width: 160px;
}

.btn-primary {
  background: var(--accent);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--accent-hover);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  border-color: var(--text-secondary);
  color: var(--text-primary);
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/components/StepTasks.vue
git commit -m "feat: add StepTasks component"
```

---

### Task 5: 创建步骤 3 组件 (StepResearch)

**Files:**
- Create: `frontend/src/components/StepResearch.vue`

- [ ] **Step 1: 创建 StepResearch.vue**

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { createResearch } from '../api/research.js'

const props = defineProps({
  tasks: Array,
  topic: String
})

const emit = defineEmits(['complete', 'report', 'back', 'update:loading'])

const isLoading = ref(true)
const error = ref('')
const taskResults = ref([])
const currentTaskIndex = ref(0)

onMounted(async () => {
  await executeResearch()
})

const executeResearch = async () => {
  isLoading.value = true
  error.value = ''
  emit('update:loading', true)

  try {
    const data = await createResearch(props.topic)
    taskResults.value = data.todo_items || []
    emit('complete', taskResults.value)
    emit('report', data.report_markdown)
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '研究失败，请重试'
  } finally {
    isLoading.value = false
    emit('update:loading', false)
  }
}
</script>

<template>
  <div class="step-research">
    <div class="card">
      <h2>研究执行中</h2>
      <p class="description">
        主题: <strong>{{ topic }}</strong>
      </p>

      <div v-if="isLoading" class="loading-state">
        <div class="loader">
          <div class="spinner-large"></div>
          <p>正在执行研究任务...</p>
          <p class="sub-text">这可能需要一些时间</p>
        </div>
      </div>

      <div v-else-if="error" class="error-state">
        <p class="error-message">{{ error }}</p>
        <button class="btn-primary" @click="executeResearch">重试</button>
      </div>

      <div v-else class="results-state">
        <div class="tasks-progress">
          <div
            v-for="(task, index) in taskResults"
            :key="index"
            class="task-item completed"
          >
            <span class="check">✓</span>
            <span>{{ task.title || `任务 ${index + 1}` }}</span>
          </div>
        </div>

        <p class="complete-text">所有任务已完成！</p>

        <button class="btn-primary" @click="emit('back')">查看结果</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.step-research {
  max-width: 600px;
  margin: 0 auto;
}

.card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow);
}

.card h2 {
  font-size: 1.5rem;
  margin-bottom: 8px;
  text-align: center;
}

.description {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 24px;
}

.description strong {
  color: var(--accent);
}

.loading-state {
  text-align: center;
  padding: 48px 0;
}

.loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.spinner-large {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loader p {
  font-size: 1rem;
  color: var(--text-primary);
}

.loader .sub-text {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 24px;
}

.error-message {
  color: #ef4444;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: var(--radius-sm);
}

.results-state {
  text-align: center;
}

.tasks-progress {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--bg-primary);
  border-radius: var(--radius-sm);
  text-align: left;
}

.task-item .check {
  color: var(--success);
  font-weight: bold;
}

.complete-text {
  color: var(--success);
  font-weight: 500;
  margin-bottom: 24px;
}

.btn-primary {
  padding: 12px 32px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
}

.btn-primary:hover {
  background: var(--accent-hover);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/components/StepResearch.vue
git commit -m "feat: add StepResearch component"
```

---

### Task 6: 创建步骤 4 组件 (StepReport)

**Files:**
- Create: `frontend/src/components/StepReport.vue`

- [ ] **Step 1: 创建 StepReport.vue**

```vue
<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

const props = defineProps({
  report: {
    type: String,
    default: ''
  },
  tasks: Array,
  topic: String
})

const emit = defineEmits(['reset'])

// 配置 marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

const renderedReport = computed(() => {
  if (!props.report) return ''
  return marked(props.report)
})
</script>

<template>
  <div class="step-report">
    <div class="card">
      <div class="card-header">
        <h2>研究报告</h2>
        <p class="topic">主题: {{ topic }}</p>
      </div>

      <div class="report-content" v-html="renderedReport"></div>

      <div class="actions">
        <button class="btn-primary" @click="emit('reset')">
          新建研究
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.step-report {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  background: rgba(30, 41, 59, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  box-shadow: var(--shadow);
}

.card-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}

.card-header h2 {
  font-size: 1.5rem;
  margin-bottom: 4px;
}

.topic {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.report-content {
  line-height: 1.8;
  font-size: 0.9375rem;
}

.report-content :deep(h1) {
  font-size: 1.75rem;
  margin: 24px 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

.report-content :deep(h2) {
  font-size: 1.375rem;
  margin: 20px 0 12px;
}

.report-content :deep(h3) {
  font-size: 1.125rem;
  margin: 16px 0 8px;
}

.report-content :deep(p) {
  margin: 12px 0;
}

.report-content :deep(ul),
.report-content :deep(ol) {
  margin: 12px 0;
  padding-left: 24px;
}

.report-content :deep(li) {
  margin: 6px 0;
}

.report-content :deep(code) {
  background: var(--bg-primary);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.875em;
}

.report-content :deep(pre) {
  background: var(--bg-primary);
  padding: 16px;
  border-radius: var(--radius-md);
  overflow-x: auto;
  margin: 16px 0;
}

.report-content :deep(pre code) {
  background: none;
  padding: 0;
}

.report-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.report-content :deep(th),
.report-content :deep(td) {
  border: 1px solid var(--border);
  padding: 10px 14px;
  text-align: left;
}

.report-content :deep(th) {
  background: var(--bg-primary);
  font-weight: 600;
}

.report-content :deep(blockquote) {
  border-left: 3px solid var(--accent);
  padding-left: 16px;
  margin: 16px 0;
  color: var(--text-secondary);
}

.report-content :deep(hr) {
  border: none;
  border-top: 1px solid var(--border);
  margin: 24px 0;
}

.actions {
  margin-top: 32px;
  text-align: center;
}

.btn-primary {
  padding: 14px 32px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 500;
}

.btn-primary:hover {
  background: var(--accent-hover);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
}
</style>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/components/StepReport.vue
git commit -m "feat: add StepReport component"
```

---

### Task 7: 安装依赖并测试

**Files:**
- Modify: `frontend/` (安装 node_modules)

- [ ] **Step 1: 安装依赖**

```bash
cd /d/coding/hello-agents/code/chapter14/.worktrees/langgraph-deepresearch/code/chapter14/langgraph-deepresearch/frontend
npm install
```

- [ ] **Step 2: 验证构建**

```bash
npm run build
```

预期: 构建成功，无错误

- [ ] **Step 3: 提交**

```bash
git add package-lock.json
git commit -m "feat: install frontend dependencies and verify build"
```

---

### Task 8: 验证完整流程

**Files:**
- Test: 全局功能测试

- [ ] **Step 1: 启动后端**

```bash
# 确保后端在 8000 端口运行
cd /d/coding/hello-agents/code/chapter14/.worktrees/langgraph-deepresearch/code/chapter14/langgraph-deepresearch
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 &
```

- [ ] **Step 2: 启动前端**

```bash
cd frontend
npm run dev
```

- [ ] **Step 3: 验证页面**

访问 http://localhost:3000

检查项:
1. ✅ 页面加载，样式正确
2. ✅ 进度条显示步骤 1
3. ✅ 输入主题，调用后端成功
4. ✅ 显示任务列表
5. ✅ 执行任务并生成报告
6. ✅ Markdown 渲染正确
7. ✅ 返回重新开始

- [ ] **Step 4: 提交**

```bash
git commit -m "feat: verify complete frontend workflow"
```

---

## 实现计划完成

所有任务已定义。按照计划:
1. 创建 Vue 3 项目结构
2. 实现 API 模块和进度条
3. 实现 4 个步骤组件
4. 安装依赖并构建验证
5. 端到端测试

**建议执行方式:** Subagent-Driven - 每个任务由独立子 agent 执行，期间进行审查