<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar -->
    <aside class="w-72 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <div>
        <h1 class="text-3xl font-bold text-brand-accent flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 mr-2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.898 20.62L16.5 21.75l-.398-1.13a3.375 3.375 0 00-2.455-2.456L12.75 18l1.13-.398a3.375 3.375 0 002.455-2.456L16.5 14.25l.398 1.13a3.375 3.375 0 002.456 2.456L20.25 18l-1.13.398a3.375 3.375 0 00-2.456 2.456z" />
          </svg>
          AI Trade<span class="text-slate-400">Bot</span>
        </h1>
        <p class="text-sm text-slate-400 mt-1">Orchestrateur Multi-Assets</p>
      </div>

      <!-- Orchestrator Controls -->
      <div class="bg-slate-700/50 p-4 rounded-xl">
        <div class="flex items-center justify-between mb-3">
          <h3 class="font-semibold text-slate-200">🧠 Orchestrateur AI</h3>
          <div :class="['w-3 h-3 rounded-full', orchestratorRunning ? 'bg-green-400 animate-pulse' : 'bg-red-400']"></div>
        </div>
        <div class="space-y-2">
          <button 
            @click="toggleOrchestrator" 
            :class="['w-full px-3 py-2 rounded-lg text-sm font-medium transition-colors',
                    orchestratorRunning ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-green-600 hover:bg-green-700 text-white']">
            {{ orchestratorRunning ? '⏹️ ARRÊTER' : '▶️ DÉMARRER' }}
          </button>
          <div class="grid grid-cols-2 gap-2 text-xs text-slate-300">
            <div>Tâches: {{ orchestratorStats.total_tasks || 0 }}</div>
            <div>Succès: {{ (orchestratorStats.success_rate || 0) }}%</div>
          </div>
        </div>
      </div>

      <!-- Asset Navigation -->
      <nav class="space-y-2 flex-grow">
        <div class="text-xs text-slate-400 uppercase tracking-wide mb-4">🌐 Multi-Assets</div>
        
        <a href="#" @click="currentAsset = 'overview'" 
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'overview' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <HomeIcon class="h-5 w-5" />
          <span>📊 Vue d'ensemble</span>
        </a>

        <a href="#" @click="currentAsset = 'meme_coins'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'meme_coins' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <CurrencyDollarIcon class="h-5 w-5" />
          <span>🪙 Meme Coins</span>
          <span v-if="assetStats.meme_coins?.active" class="ml-auto w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
        </a>

        <a href="#" @click="currentAsset = 'crypto_lt'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'crypto_lt' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <ChartBarIcon class="h-5 w-5" />
          <span>₿ Crypto Long Terme</span>
          <span v-if="assetStats.crypto_lt?.active" class="ml-auto w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
        </a>

        <a href="#" @click="currentAsset = 'forex'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'forex' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <GlobeEuropeAfricaIcon class="h-5 w-5" />
          <span>💱 Forex</span>
          <span v-if="assetStats.forex?.active" class="ml-auto w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
        </a>

        <a href="#" @click="currentAsset = 'etf'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'etf' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <WalletIcon class="h-5 w-5" />
          <span>📈 ETF</span>
          <span v-if="assetStats.etf?.active" class="ml-auto w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
        </a>

        <div class="text-xs text-slate-400 uppercase tracking-wide mt-6 mb-4">⚙️ Système</div>
        
        <a href="#" @click="currentAsset = 'ai_insights'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'ai_insights' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <CpuChipIcon class="h-5 w-5" />
          <span>🧠 Insights IA</span>
        </a>

        <a href="#" @click="currentAsset = 'settings'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentAsset === 'settings' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <Cog6ToothIcon class="h-5 w-5" />
          <span>⚙️ Paramètres</span>
        </a>
      </nav>

      <!-- Market Conditions Footer -->
      <div class="mt-auto border-t border-slate-700 pt-6">
        <div class="text-sm text-slate-400">Conditions Marché :</div>
        <div class="grid grid-cols-2 gap-2 text-xs mt-2">
          <div class="text-slate-300">Volatilité: {{ (marketConditions.volatility || 0).toFixed(3) }}</div>
          <div class="text-slate-300">Tendance: {{ (marketConditions.trend_strength || 0).toFixed(3) }}</div>
          <div class="text-slate-300">CPU: {{ (systemStatus.cpu_usage || 0) }}%</div>
          <div class="text-slate-300">RAM: {{ (systemStatus.memory_usage || 0).toFixed(1) }}%</div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 space-y-8 overflow-y-auto">
      <header class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-semibold text-slate-100">{{ getAssetTitle() }}</h2>
          <p class="text-slate-400">{{ getAssetSubtitle() }}</p>
        </div>
        <div class="flex items-center space-x-4">
          <button @click="refreshData" class="p-2 rounded-full hover:bg-slate-700 transition-colors pulse-glow">
            <ArrowPathIcon class="h-6 w-6 text-slate-400" />
          </button>
          <button @click="$router.push('/login')" class="p-2 rounded-full hover:bg-slate-700 transition-colors">
            <PowerIcon class="h-6 w-6 text-slate-400" />
          </button>
          <div class="w-10 h-10 rounded-full border-2 border-brand-accent bg-brand-accent flex items-center justify-center text-white font-bold">
            AI
          </div>
        </div>
      </header>

      <!-- Overview Section -->
      <div v-if="currentAsset === 'overview'" class="space-y-8">
        <!-- Global Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-purple-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">🪙 Meme Coins</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ assetStats.meme_coins?.recommendations || 0 }}</p>
            <span :class="['text-sm font-medium', assetStats.meme_coins?.active ? 'text-green-400' : 'text-slate-400']">
              {{ assetStats.meme_coins?.active ? '🔥 Actif' : '😴 Inactif' }}
            </span>
          </div>

          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-orange-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">₿ Crypto LT</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ assetStats.crypto_lt?.recommendations || 0 }}</p>
            <span :class="['text-sm font-medium', assetStats.crypto_lt?.active ? 'text-green-400' : 'text-slate-400']">
              {{ assetStats.crypto_lt?.active ? '📈 Optimisation' : '💤 Attente' }}
            </span>
          </div>

          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-blue-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">💱 Forex</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ assetStats.forex?.recommendations || 0 }}</p>
            <span :class="['text-sm font-medium', assetStats.forex?.active ? 'text-green-400' : 'text-slate-400']">
              {{ assetStats.forex?.active ? '🌐 Session Active' : '🌙 Hors Session' }}
            </span>
          </div>

          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-green-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">📈 ETF</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ assetStats.etf?.recommendations || 0 }}</p>
            <span :class="['text-sm font-medium', assetStats.etf?.active ? 'text-green-400' : 'text-slate-400']">
              {{ assetStats.etf?.active ? '🚀 Toujours Actif' : '⏸️ Pause' }}
            </span>
          </div>
        </div>

        <!-- AI Decision Engine Status -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <div class="flex items-center mb-4">
            <CpuChipIcon class="w-8 h-8 mr-3 text-brand-accent" />
            <h3 class="text-xl font-semibold text-slate-100">🧠 Decision Engine - État Temps Réel</h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div class="bg-slate-700/70 p-4 rounded-lg">
              <h4 class="font-semibold text-blue-400">📊 Analyse Marché</h4>
              <p class="text-sm text-slate-300 mt-1">Volatilité: {{ (marketConditions.volatility || 0).toFixed(3) }}</p>
              <p class="text-sm text-slate-300">Tendance: {{ (marketConditions.trend_strength || 0).toFixed(3) }}</p>
            </div>
            <div class="bg-slate-700/70 p-4 rounded-lg">
              <h4 class="font-semibold text-green-400">💻 Performance Système</h4>
              <p class="text-sm text-slate-300 mt-1">CPU: {{ systemStatus.cpu_usage || 0 }}%</p>
              <p class="text-sm text-slate-300">RAM: {{ (systemStatus.memory_usage || 0).toFixed(1) }}%</p>
            </div>
            <div class="bg-slate-700/70 p-4 rounded-lg">
              <h4 class="font-semibold text-purple-400">🎯 Orchestrateur</h4>
              <p class="text-sm text-slate-300 mt-1">Tâches: {{ orchestratorStats.total_tasks || 0 }}</p>
              <p class="text-sm text-slate-300">Succès: {{ orchestratorStats.success_rate || 0 }}%</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Meme Coins Section -->
      <div v-if="currentAsset === 'meme_coins'" class="space-y-8">
        <AssetDashboard 
          :asset-type="'meme_coins'"
          :asset-name="'🪙 Meme Coins'"
          :recommendations="recommendations.meme_coins"
          :color="'purple'"
          :description="'Trading haute fréquence sur meme coins (volatilité > 0.8 requise)'"
        />
      </div>

      <!-- Crypto Long Term Section -->
      <div v-if="currentAsset === 'crypto_lt'" class="space-y-8">
        <AssetDashboard 
          :asset-type="'crypto_lt'"
          :asset-name="'₿ Crypto Long Terme'"
          :recommendations="recommendations.crypto_lt"
          :color="'orange'"
          :description="'Accumulation et rebalancing crypto long terme (optimal en période calme < 0.4)'"
        />
      </div>

      <!-- Forex Section -->
      <div v-if="currentAsset === 'forex'" class="space-y-8">
        <AssetDashboard 
          :asset-type="'forex'"
          :asset-name="'💱 Forex'"
          :recommendations="recommendations.forex"
          :color="'blue'"
          :description="'Trading paires Forex pendant sessions actives (8h-17h UTC)'"
        />
      </div>

      <!-- ETF Section -->
      <div v-if="currentAsset === 'etf'" class="space-y-8">
        <AssetDashboard 
          :asset-type="'etf'"
          :asset-name="'📈 ETF'"
          :recommendations="recommendations.etf"
          :color="'green'"
          :description="'Investissement systématique ETF (toujours actif)'"
        />
      </div>

      <!-- AI Insights Section -->
      <div v-if="currentAsset === 'ai_insights'" class="space-y-8">
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">🧠 Insights IA Multi-Assets</h3>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="space-y-4">
              <h4 class="font-semibold text-slate-200">📊 Recommandations Intelligentes</h4>
              <div v-for="rec in globalRecommendations" :key="`${rec.asset_type}-${rec.task_type}`" 
                   class="bg-slate-700/50 p-3 rounded-lg">
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium text-slate-200">{{ getAssetEmoji(rec.asset_type) }} {{ rec.task_type }}</span>
                  <span :class="['px-2 py-1 text-xs rounded', getPriorityClass(rec.priority)]">{{ rec.priority }}</span>
                </div>
                <p class="text-xs text-slate-400 mt-1">{{ rec.reason }}</p>
                <p class="text-xs text-slate-500">Fréquence: {{ rec.frequency_minutes }}min</p>
              </div>
            </div>
            <div class="space-y-4">
              <h4 class="font-semibold text-slate-200">🎯 Métriques Performance</h4>
              <div class="bg-slate-700/50 p-4 rounded-lg">
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <div class="text-slate-400">Tâches Totales</div>
                    <div class="text-lg font-semibold text-slate-100">{{ orchestratorStats.total_tasks || 0 }}</div>
                  </div>
                  <div>
                    <div class="text-slate-400">Taux de Succès</div>
                    <div class="text-lg font-semibold text-green-400">{{ orchestratorStats.success_rate || 0 }}%</div>
                  </div>
                  <div>
                    <div class="text-slate-400">Temps Moyen</div>
                    <div class="text-lg font-semibold text-slate-100">{{ (orchestratorStats.average_execution_time || 0).toFixed(1) }}s</div>
                  </div>
                  <div>
                    <div class="text-slate-400">Statut</div>
                    <div :class="['text-lg font-semibold', orchestratorRunning ? 'text-green-400' : 'text-red-400']">
                      {{ orchestratorRunning ? '🟢 Actif' : '🔴 Arrêté' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings Section -->
      <div v-if="currentAsset === 'settings'" class="space-y-8">
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">⚙️ Configuration Multi-Assets</h3>
          <p class="text-slate-400">Configuration avancée des workflows disponible prochainement...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  SparklesIcon, HomeIcon, CurrencyDollarIcon, ChartBarIcon, 
  GlobeEuropeAfricaIcon, WalletIcon, CpuChipIcon, Cog6ToothIcon,
  ArrowPathIcon, PowerIcon, ClockIcon
} from '@heroicons/vue/24/outline'
import AssetDashboard from '../components/AssetDashboard.vue'

// Reactive data
const currentAsset = ref('overview')
const orchestratorRunning = ref(false)
const orchestratorStats = ref({})
const marketConditions = ref({})
const systemStatus = ref({})
const assetStats = ref({})
const recommendations = ref({})
const globalRecommendations = ref([])
const refreshInterval = ref(null)

// Methods
const getAssetTitle = () => {
  const titles = {
    overview: '📊 Vue d\'Ensemble Multi-Assets',
    meme_coins: '🪙 Meme Coins - Trading Haute Fréquence',
    crypto_lt: '₿ Crypto Long Terme - Accumulation DCA',
    forex: '💱 Forex - Trading Devises',
    etf: '📈 ETF - Investissement Systématique',
    ai_insights: '🧠 Insights IA - Analyse Prédictive',
    settings: '⚙️ Paramètres - Configuration Workflows'
  }
  return titles[currentAsset.value] || 'Dashboard'
}

const getAssetSubtitle = () => {
  const subtitles = {
    overview: 'Supervision intelligente de tous les workflows de trading',
    meme_coins: 'Actif uniquement si volatilité > 0.8 (conditions extrêmes)',
    crypto_lt: 'Optimal pendant périodes calmes < 0.4 (accumulation sûre)',
    forex: 'Trading pendant sessions 8h-17h UTC uniquement',
    etf: 'Stratégie always-on pour investissement long terme',
    ai_insights: 'Analyses prédictives et recommandations temps réel',
    settings: 'Personnalisation avancée des stratégies de trading'
  }
  return subtitles[currentAsset.value] || 'AI Trading Hub'
}

const getAssetEmoji = (assetType) => {
  const emojis = {
    meme_coins: '🪙',
    crypto_lt: '₿',
    forex: '💱',
    etf: '📈'
  }
  return emojis[assetType] || '📊'
}

const getPriorityClass = (priority) => {
  const classes = {
    HIGH: 'bg-red-600 text-white',
    MEDIUM: 'bg-yellow-600 text-white', 
    LOW: 'bg-green-600 text-white'
  }
  return classes[priority] || 'bg-slate-600 text-white'
}

const toggleOrchestrator = async () => {
  try {
    const action = orchestratorRunning.value ? 'stop' : 'start'
    const response = await fetch(`/api/orchestrator/${action}`, { method: 'POST' })
    const data = await response.json()
    
    if (data.success) {
      orchestratorRunning.value = !orchestratorRunning.value
      await refreshData()
    }
  } catch (error) {
    console.error('Erreur toggle orchestrateur:', error)
  }
}

const fetchOrchestratorStatus = async () => {
  try {
    const response = await fetch('/api/orchestrator/status')
    const data = await response.json()
    
    orchestratorRunning.value = data.orchestrator?.running || false
    orchestratorStats.value = data.orchestrator || {}
    marketConditions.value = data.market_conditions || {}
    systemStatus.value = data.system_status || {}
  } catch (error) {
    console.error('Erreur status orchestrateur:', error)
  }
}

const fetchAssetRecommendations = async () => {
  try {
    const assetTypes = ['meme_coins', 'crypto_lt', 'forex', 'etf']
    
    for (const assetType of assetTypes) {
      const response = await fetch(`/api/orchestrator/recommendations/${assetType}`)
      const data = await response.json()
      
      recommendations.value[assetType] = data.recommendations || []
      assetStats.value[assetType] = {
        recommendations: (data.recommendations || []).length,
        active: (data.recommendations || []).length > 0
      }
    }
    
    // Global recommendations
    const globalResponse = await fetch('/api/orchestrator/recommendations')
    const globalData = await globalResponse.json()
    globalRecommendations.value = globalData.all_recommendations || []
  } catch (error) {
    console.error('Erreur recommandations assets:', error)
  }
}

const refreshData = async () => {
  await Promise.all([
    fetchOrchestratorStatus(),
    fetchAssetRecommendations()
  ])
}

// Lifecycle
onMounted(async () => {
  await refreshData()
  
  // Auto-refresh every 5 seconds
  refreshInterval.value = setInterval(refreshData, 5000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
.pulse-glow {
  animation: pulse-glow 2s infinite;
}

@keyframes pulse-glow {
  0%, 100% { 
    box-shadow: 0 0 5px rgba(59, 130, 246, 0.3);
  }
  50% { 
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
  }
}

.brand-accent {
  color: #38bdf8;
}
</style> 