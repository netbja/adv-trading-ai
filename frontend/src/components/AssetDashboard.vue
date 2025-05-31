<template>
  <div class="space-y-6">
    <!-- Asset Header -->
    <div :class="['bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4', getBorderColor()]">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-2xl font-semibold text-slate-100">{{ assetName }}</h3>
        <div :class="['px-3 py-1 rounded-full text-sm font-medium', getStatusClass()]">
          {{ getStatusText() }}
        </div>
      </div>
      <p class="text-slate-400 mb-4">{{ description }}</p>
      
      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-slate-700/50 p-3 rounded-lg">
          <div class="text-slate-400 text-sm">Recommandations</div>
          <div class="text-xl font-semibold text-slate-100">{{ recommendations.length }}</div>
        </div>
        <div class="bg-slate-700/50 p-3 rounded-lg">
          <div class="text-slate-400 text-sm">Priorité Max</div>
          <div class="text-xl font-semibold" :class="getHighestPriorityColor()">{{ getHighestPriority() }}</div>
        </div>
        <div class="bg-slate-700/50 p-3 rounded-lg">
          <div class="text-slate-400 text-sm">Fréquence Min</div>
          <div class="text-xl font-semibold text-slate-100">{{ getMinFrequency() }}min</div>
        </div>
      </div>
    </div>

    <!-- Recommendations List -->
    <div v-if="recommendations.length > 0" class="bg-slate-800 p-6 rounded-xl shadow-2xl">
      <h4 class="text-xl font-semibold text-slate-100 mb-4">🎯 Recommandations Actives</h4>
      <div class="space-y-4">
        <div 
          v-for="(rec, index) in recommendations" 
          :key="`${rec.task_type}-${index}`"
          class="bg-slate-700/50 p-4 rounded-lg border-l-4"
          :class="getRecommendationBorder(rec.priority)"
        >
          <div class="flex items-center justify-between mb-2">
            <h5 class="font-semibold text-slate-200">{{ formatTaskType(rec.task_type) }}</h5>
            <span :class="['px-2 py-1 text-xs rounded font-medium', getPriorityClass(rec.priority)]">
              {{ rec.priority }}
            </span>
          </div>
          <p class="text-sm text-slate-300 mb-2">{{ rec.reason }}</p>
          <div class="flex items-center justify-between text-xs">
            <span class="text-slate-400">
              ⏱️ Fréquence: {{ rec.frequency_minutes }} minutes
            </span>
            <span class="text-slate-400">
              🎯 Asset: {{ assetType }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- No Recommendations State -->
    <div v-else class="bg-slate-800 p-6 rounded-xl shadow-2xl">
      <div class="text-center py-8">
        <div class="text-6xl mb-4">{{ getInactiveEmoji() }}</div>
        <h4 class="text-xl font-semibold text-slate-100 mb-2">Workflow Inactif</h4>
        <p class="text-slate-400">{{ getInactiveReason() }}</p>
      </div>
    </div>

    <!-- Asset-Specific Features -->
    <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
      <h4 class="text-xl font-semibold text-slate-100 mb-4">📊 Caractéristiques {{ assetName }}</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <!-- Meme Coins Features -->
        <div v-if="assetType === 'meme_coins'" class="space-y-3">
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-purple-400 font-medium">🔥 Seuil d'Activation</div>
            <div class="text-slate-300">Volatilité > 0.8 requise</div>
          </div>
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-purple-400 font-medium">⚡ Fréquence Trading</div>
            <div class="text-slate-300">1-2 minutes (haute vitesse)</div>
          </div>
        </div>

        <!-- Crypto Long Term Features -->
        <div v-if="assetType === 'crypto_lt'" class="space-y-3">
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-orange-400 font-medium">😴 Conditions Optimales</div>
            <div class="text-slate-300">Volatilité < 0.4 (périodes calmes)</div>
          </div>
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-orange-400 font-medium">💰 Stratégie DCA</div>
            <div class="text-slate-300">Accumulation progressive BTC/ETH/SOL</div>
          </div>
        </div>

        <!-- Forex Features -->
        <div v-if="assetType === 'forex'" class="space-y-3">
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-blue-400 font-medium">🌐 Heures de Trading</div>
            <div class="text-slate-300">8h00 - 17h00 UTC uniquement</div>
          </div>
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-blue-400 font-medium">💱 Paires Principales</div>
            <div class="text-slate-300">EUR/USD, GBP/USD, USD/JPY</div>
          </div>
        </div>

        <!-- ETF Features -->
        <div v-if="assetType === 'etf'" class="space-y-3">
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-green-400 font-medium">🚀 Always-On</div>
            <div class="text-slate-300">Toujours actif (24/7)</div>
          </div>
          <div class="bg-slate-700/50 p-3 rounded">
            <div class="text-green-400 font-medium">📈 Diversification</div>
            <div class="text-slate-300">VTI, QQQ, VXUS, BND</div>
          </div>
        </div>

        <!-- Performance Placeholder -->
        <div class="bg-slate-700/50 p-3 rounded">
          <div :class="['font-medium', getAccentColor()]">📊 Performance (Simulation)</div>
          <div class="text-slate-300">Graphiques temps réel disponibles prochainement</div>
        </div>
      </div>
    </div>

    <!-- Configuration Preview -->
    <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
      <h4 class="text-xl font-semibold text-slate-100 mb-4">⚙️ Configuration Workflow</h4>
      <div class="bg-slate-700/30 p-4 rounded-lg">
        <pre class="text-sm text-slate-300">{{getConfigPreview()}}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  assetType: {
    type: String,
    required: true
  },
  assetName: {
    type: String,
    required: true
  },
  recommendations: {
    type: Array,
    default: () => []
  },
  color: {
    type: String,
    default: 'blue'
  },
  description: {
    type: String,
    default: ''
  }
})

// Computed
const getBorderColor = () => {
  const colors = {
    purple: 'border-purple-500',
    orange: 'border-orange-500',
    blue: 'border-blue-500',
    green: 'border-green-500'
  }
  return colors[props.color] || 'border-blue-500'
}

const getAccentColor = () => {
  const colors = {
    purple: 'text-purple-400',
    orange: 'text-orange-400',
    blue: 'text-blue-400',
    green: 'text-green-400'
  }
  return colors[props.color] || 'text-blue-400'
}

const getStatusClass = () => {
  const isActive = props.recommendations.length > 0
  return isActive 
    ? 'bg-green-600 text-white' 
    : 'bg-slate-600 text-slate-300'
}

const getStatusText = () => {
  return props.recommendations.length > 0 ? '🟢 ACTIF' : '⏸️ INACTIF'
}

const getHighestPriority = () => {
  if (props.recommendations.length === 0) return 'N/A'
  
  const priorities = props.recommendations.map(r => r.priority)
  if (priorities.includes('HIGH')) return 'HIGH'
  if (priorities.includes('MEDIUM')) return 'MEDIUM'
  return 'LOW'
}

const getHighestPriorityColor = () => {
  const priority = getHighestPriority()
  const colors = {
    'HIGH': 'text-red-400',
    'MEDIUM': 'text-yellow-400',
    'LOW': 'text-green-400'
  }
  return colors[priority] || 'text-slate-400'
}

const getMinFrequency = () => {
  if (props.recommendations.length === 0) return 'N/A'
  return Math.min(...props.recommendations.map(r => r.frequency_minutes))
}

const getPriorityClass = (priority) => {
  const classes = {
    HIGH: 'bg-red-600 text-white',
    MEDIUM: 'bg-yellow-600 text-white',
    LOW: 'bg-green-600 text-white'
  }
  return classes[priority] || 'bg-slate-600 text-white'
}

const getRecommendationBorder = (priority) => {
  const borders = {
    HIGH: 'border-red-500',
    MEDIUM: 'border-yellow-500',
    LOW: 'border-green-500'
  }
  return borders[priority] || 'border-slate-500'
}

const formatTaskType = (taskType) => {
  return taskType
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

const getInactiveEmoji = () => {
  const emojis = {
    meme_coins: '😴',
    crypto_lt: '💤',
    forex: '🌙',
    etf: '⏸️'
  }
  return emojis[props.assetType] || '💤'
}

const getInactiveReason = () => {
  const reasons = {
    meme_coins: 'Volatilité trop faible (< 0.8). Attente de conditions extrêmes.',
    crypto_lt: 'Conditions de marché non optimales pour accumulation long terme.',
    forex: 'Hors session de trading (8h-17h UTC). Sessions fermées.',
    etf: 'Workflow temporairement en pause. ETF habituellement toujours actif.'
  }
  return reasons[props.assetType] || 'Workflow temporairement inactif.'
}

const getConfigPreview = () => {
  const configs = {
    meme_coins: `{
  "activation": "volatility > 0.8",
  "frequency": "1-2 minutes",
  "risk_level": "HIGH",
  "targets": ["DOGE", "SHIB", "PEPE"]
}`,
    crypto_lt: `{
  "activation": "volatility < 0.4",
  "strategy": "DCA + Rebalancing",
  "risk_level": "MEDIUM",
  "targets": ["BTC", "ETH", "SOL"]
}`,
    forex: `{
  "activation": "8h-17h UTC",
  "frequency": "15-30 minutes",
  "risk_level": "MEDIUM",
  "pairs": ["EUR/USD", "GBP/USD", "USD/JPY"]
}`,
    etf: `{
  "activation": "Always ON",
  "strategy": "Systematic Investment",
  "risk_level": "LOW",
  "etfs": ["VTI", "QQQ", "VXUS", "BND"]
}`
  }
  return configs[props.assetType] || '{}'
}
</script>

<style scoped>
pre {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  background: rgba(0, 0, 0, 0.2);
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
}
</style> 