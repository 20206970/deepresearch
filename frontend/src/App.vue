<script setup>
import { ref } from 'vue'
import ProgressBar from './components/ProgressBar.vue'
import StepInput from './components/StepInput.vue'
import StepTasks from './components/StepTasks.vue'
import StepResearch from './components/StepResearch.vue'
import StepReport from './components/StepReport.vue'
import StepHistory from './components/StepHistory.vue'

const currentStep = ref(1)
const topic = ref('')
const tasks = ref([])
const taskResults = ref([])
const report = ref('')
const isLoading = ref(false)

// 保存当前研究状态（用于从历史页面返回时恢复）
let savedState = null

const handleTopicSubmit = (data) => {
  topic.value = data.topic
  tasks.value = data.tasks
  currentStep.value = 2
}

const handleTasksConfirm = () => {
  currentStep.value = 3
}

const handleResearchComplete = (results, reportData) => {
  taskResults.value = results
  report.value = reportData
  currentStep.value = 4
}

const handleReset = () => {
  currentStep.value = 1
  topic.value = ''
  tasks.value = []
  taskResults.value = []
  report.value = ''
}

const goToHistory = () => {
  // 保存当前研究状态
  savedState = {
    topic: topic.value,
    tasks: tasks.value,
    taskResults: taskResults.value,
    report: report.value,
    currentStep: currentStep.value
  }
  currentStep.value = 5
}

const goHome = () => {
  // 恢复之前的研究状态
  if (savedState) {
    topic.value = savedState.topic
    tasks.value = savedState.tasks
    taskResults.value = savedState.taskResults
    report.value = savedState.report
    currentStep.value = savedState.currentStep
    savedState = null
  } else {
    currentStep.value = 1
  }
}
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🔬 LangGraph 深度研究助手</h1>
      <button v-if="currentStep !== 5" class="btn-history" @click="goToHistory">
        历史记录
      </button>
    </header>

    <ProgressBar v-if="currentStep < 5" :currentStep="currentStep" :totalSteps="4" />

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
        @report="(data) => report = data"
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

      <StepHistory
        v-else-if="currentStep === 5"
        @back="goHome"
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
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 32px 24px 16px;
  position: relative;
}

.header h1 {
  font-size: 1.75rem;
  color: var(--text-primary);
}

.btn-history {
  position: absolute;
  right: 24px;
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: var(--transition);
}

.btn-history:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.main {
  flex: 1;
  padding: 24px;
}
</style>