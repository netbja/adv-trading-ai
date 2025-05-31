<template>
  <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-xl font-semibold text-slate-100 flex items-center">
        <svg class="w-6 h-6 mr-3 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
        </svg>
        Workflow Process Monitor
      </h3>
      <div class="flex items-center space-x-2">
        <div class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
        <span class="text-sm text-slate-300">{{ activeWorkflows }} processus actifs</span>
      </div>
    </div>

    <!-- Workflow Pipeline -->
    <div class="space-y-6">
      <!-- Market Analysis Pipeline -->
      <div class="relative">
        <h4 class="text-md font-medium text-slate-200 mb-4 flex items-center">
          📊 Market Analysis Pipeline
          <span :class="['ml-2 px-2 py-1 text-xs rounded-full', getStatusBadge('market_analysis')]">
            {{ workflows.market_analysis.status }}
          </span>
        </h4>
        
        <div class="relative flex items-center space-x-4">
          <!-- Data Collection -->
          <div :class="['relative flex-1 p-4 rounded-lg border-2 transition-all duration-500', getStepClass('data_collection')]">
            <div class="flex items-center justify-between">
              <div>
                <h5 class="font-medium text-sm">📡 Data Collection</h5>
                <p class="text-xs text-slate-400 mt-1">Binance, Coinbase, Forex APIs</p>
              </div>
              <div :class="['w-3 h-3 rounded-full', getStepIndicator('data_collection')]"></div>
            </div>
            
            <!-- Progress bar -->
            <div class="w-full bg-slate-700 rounded-full h-1 mt-3">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('data_collection')]" 
                   :style="{ width: workflows.market_analysis.steps.data_collection + '%' }"></div>
            </div>
          </div>

          <!-- Arrow -->
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </div>

          <!-- AI Processing -->
          <div :class="['relative flex-1 p-4 rounded-lg border-2 transition-all duration-500', getStepClass('ai_processing')]">
            <div class="flex items-center justify-between">
              <div>
                <h5 class="font-medium text-sm">🧠 AI Processing</h5>
                <p class="text-xs text-slate-400 mt-1">Pattern recognition & prediction</p>
              </div>
              <div :class="['w-3 h-3 rounded-full', getStepIndicator('ai_processing')]"></div>
            </div>
            
            <div class="w-full bg-slate-700 rounded-full h-1 mt-3">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('ai_processing')]" 
                   :style="{ width: workflows.market_analysis.steps.ai_processing + '%' }"></div>
            </div>
          </div>

          <!-- Arrow -->
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </div>

          <!-- Signal Generation -->
          <div :class="['relative flex-1 p-4 rounded-lg border-2 transition-all duration-500', getStepClass('signal_generation')]">
            <div class="flex items-center justify-between">
              <div>
                <h5 class="font-medium text-sm">🎯 Signal Generation</h5>
                <p class="text-xs text-slate-400 mt-1">Trading signals output</p>
              </div>
              <div :class="['w-3 h-3 rounded-full', getStepIndicator('signal_generation')]"></div>
            </div>
            
            <div class="w-full bg-slate-700 rounded-full h-1 mt-3">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('signal_generation')]" 
                   :style="{ width: workflows.market_analysis.steps.signal_generation + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- Timing info -->
        <div class="flex justify-between text-xs text-slate-500 mt-3">
          <span>Cycle: {{ workflows.market_analysis.cycle_time }}s</span>
          <span>Last run: {{ workflows.market_analysis.last_run }}</span>
          <span>Success rate: {{ workflows.market_analysis.success_rate }}%</span>
        </div>
      </div>

      <!-- Trading Execution Pipeline -->
      <div class="relative">
        <h4 class="text-md font-medium text-slate-200 mb-4 flex items-center">
          ⚡ Trading Execution Pipeline
          <span :class="['ml-2 px-2 py-1 text-xs rounded-full', getStatusBadge('trading_execution')]">
            {{ workflows.trading_execution.status }}
          </span>
        </h4>
        
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <!-- Risk Assessment -->
          <div :class="['p-4 rounded-lg border-2 transition-all duration-500', getStepClass('risk_assessment')]">
            <div class="flex items-center justify-between mb-2">
              <h5 class="font-medium text-sm">🛡️ Risk Assessment</h5>
              <div :class="['w-2 h-2 rounded-full', getStepIndicator('risk_assessment')]"></div>
            </div>
            <div class="text-xs text-slate-400">Max risk: 2%</div>
            <div class="w-full bg-slate-700 rounded-full h-1 mt-2">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('risk_assessment')]" 
                   :style="{ width: workflows.trading_execution.steps.risk_assessment + '%' }"></div>
            </div>
          </div>

          <!-- Position Sizing -->
          <div :class="['p-4 rounded-lg border-2 transition-all duration-500', getStepClass('position_sizing')]">
            <div class="flex items-center justify-between mb-2">
              <h5 class="font-medium text-sm">📏 Position Sizing</h5>
              <div :class="['w-2 h-2 rounded-full', getStepIndicator('position_sizing')]"></div>
            </div>
            <div class="text-xs text-slate-400">Kelly criterion</div>
            <div class="w-full bg-slate-700 rounded-full h-1 mt-2">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('position_sizing')]" 
                   :style="{ width: workflows.trading_execution.steps.position_sizing + '%' }"></div>
            </div>
          </div>

          <!-- Order Execution -->
          <div :class="['p-4 rounded-lg border-2 transition-all duration-500', getStepClass('order_execution')]">
            <div class="flex items-center justify-between mb-2">
              <h5 class="font-medium text-sm">💼 Order Execution</h5>
              <div :class="['w-2 h-2 rounded-full', getStepIndicator('order_execution')]"></div>
            </div>
            <div class="text-xs text-slate-400">Market/Limit orders</div>
            <div class="w-full bg-slate-700 rounded-full h-1 mt-2">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('order_execution')]" 
                   :style="{ width: workflows.trading_execution.steps.order_execution + '%' }"></div>
            </div>
          </div>

          <!-- Monitoring -->
          <div :class="['p-4 rounded-lg border-2 transition-all duration-500', getStepClass('monitoring')]">
            <div class="flex items-center justify-between mb-2">
              <h5 class="font-medium text-sm">👁️ Monitoring</h5>
              <div :class="['w-2 h-2 rounded-full', getStepIndicator('monitoring')]"></div>
            </div>
            <div class="text-xs text-slate-400">Real-time tracking</div>
            <div class="w-full bg-slate-700 rounded-full h-1 mt-2">
              <div :class="['h-1 rounded-full transition-all duration-1000', getProgressColor('monitoring')]" 
                   :style="{ width: workflows.trading_execution.steps.monitoring + '%' }"></div>
            </div>
          </div>
        </div>

        <div class="flex justify-between text-xs text-slate-500 mt-3">
          <span>Avg execution: {{ workflows.trading_execution.execution_time }}ms</span>
          <span>Orders today: {{ workflows.trading_execution.orders_today }}</span>
          <span>Fill rate: {{ workflows.trading_execution.fill_rate }}%</span>
        </div>
      </div>

      <!-- Current Activities -->
      <div class="bg-slate-700/30 p-4 rounded-lg">
        <h4 class="text-md font-medium text-slate-200 mb-3">🔥 Activités en Cours</h4>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div v-for="activity in currentActivities" :key="activity.id" 
               class="flex items-center space-x-3 p-3 bg-slate-800/50 rounded">
            <div :class="['w-2 h-2 rounded-full animate-pulse', activity.color]"></div>
            <div class="flex-1">
              <div class="font-medium text-sm text-slate-200">{{ activity.title }}</div>
              <div class="text-xs text-slate-400">{{ activity.description }}</div>
            </div>
            <div class="text-xs text-slate-500">{{ activity.time }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// Props
const props = defineProps({
  orchestratorRunning: {
    type: Boolean,
    default: false
  }
})

// État réactif
const workflows = ref({
  market_analysis: {
    status: 'RUNNING',
    cycle_time: 12,
    last_run: '2 min ago',
    success_rate: 87,
    steps: {
      data_collection: 100,
      ai_processing: 75,
      signal_generation: 45
    }
  },
  trading_execution: {
    status: 'ACTIVE',
    execution_time: 156,
    orders_today: 23,
    fill_rate: 98,
    steps: {
      risk_assessment: 100,
      position_sizing: 85,
      order_execution: 60,
      monitoring: 100
    }
  }
})

const currentActivities = ref([
  {
    id: 1,
    title: 'Analyse DOGE/USDT',
    description: 'Détection pattern breakout',
    time: '30s',
    color: 'bg-purple-400'
  },
  {
    id: 2,
    title: 'Portfolio Rebalancing',
    description: 'Crypto long terme optimization',
    time: '1m',
    color: 'bg-blue-400'
  },
  {
    id: 3,
    title: 'Risk Monitoring',
    description: 'VaR calculation in progress',
    time: '45s',
    color: 'bg-yellow-400'
  },
  {
    id: 4,
    title: 'Signal Validation',
    description: 'Confidence score: 89%',
    time: '15s',
    color: 'bg-green-400'
  }
])

// Computed
const activeWorkflows = computed(() => {
  return Object.values(workflows.value).filter(w => w.status === 'RUNNING' || w.status === 'ACTIVE').length
})

// Méthodes
const getStatusBadge = (workflowType) => {
  const status = workflows.value[workflowType]?.status
  const badges = {
    RUNNING: 'bg-green-500/20 text-green-400 border border-green-500/30',
    ACTIVE: 'bg-blue-500/20 text-blue-400 border border-blue-500/30',
    PAUSED: 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30',
    ERROR: 'bg-red-500/20 text-red-400 border border-red-500/30'
  }
  return badges[status] || 'bg-slate-500/20 text-slate-400'
}

const getStepClass = (stepName) => {
  // Logique pour déterminer l'état de chaque étape
  const isActive = Math.random() > 0.5 // Simulation
  const isCompleted = Math.random() > 0.3 // Simulation
  
  if (isActive) return 'border-brand-accent bg-brand-accent/5'
  if (isCompleted) return 'border-green-500/50 bg-green-500/5'
  return 'border-slate-600 bg-slate-700/30'
}

const getStepIndicator = (stepName) => {
  const isActive = Math.random() > 0.5
  const isCompleted = Math.random() > 0.3
  
  if (isActive) return 'bg-brand-accent animate-pulse'
  if (isCompleted) return 'bg-green-400'
  return 'bg-slate-500'
}

const getProgressColor = (stepName) => {
  const isActive = Math.random() > 0.5
  if (isActive) return 'bg-gradient-to-r from-brand-accent to-blue-500'
  return 'bg-gradient-to-r from-green-500 to-green-400'
}

// Simulation en temps réel
const updateInterval = ref(null)

const simulateWorkflowProgress = () => {
  // Simuler la progression des étapes
  Object.keys(workflows.value).forEach(workflowName => {
    const workflow = workflows.value[workflowName]
    Object.keys(workflow.steps).forEach(stepName => {
      // Simuler progression réaliste
      if (Math.random() > 0.7) {
        workflow.steps[stepName] = Math.min(100, workflow.steps[stepName] + Math.floor(Math.random() * 10))
        
        // Reset à 0 quand terminé pour nouveau cycle
        if (workflow.steps[stepName] >= 100) {
          setTimeout(() => {
            workflow.steps[stepName] = 0
          }, 2000)
        }
      }
    })
  })
  
  // Mettre à jour activités courantes
  if (Math.random() > 0.8) {
    currentActivities.value.forEach(activity => {
      const timeValue = parseInt(activity.time)
      activity.time = `${timeValue + 1}s`
    })
  }
}

// Lifecycle
onMounted(() => {
  updateInterval.value = setInterval(simulateWorkflowProgress, 3000)
})

onUnmounted(() => {
  if (updateInterval.value) {
    clearInterval(updateInterval.value)
  }
})
</script>

<style scoped>
/* Animation personnalisée pour les indicateurs de progression */
@keyframes pulse-slow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse-slow {
  animation: pulse-slow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style> 