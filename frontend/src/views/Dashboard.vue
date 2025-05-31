<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <div>
        <!-- Logo AI Trade Bot (vrai logo avec couleurs) -->
        <div class="text-3xl font-bold text-brand-accent flex items-center justify-center py-4">
          <img src="/src/assets/images/ai-trade-bot-logo.png" alt="AI Trade Bot" class="w-24 h-24 object-contain">
        </div>
      </div>

      <nav class="space-y-2 flex-grow">
        <a href="#" @click="currentSection = 'overview'" 
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'overview' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="currentSection === 'overview' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
          </svg>
          <span>Dashboard</span>
        </a>
        
        <a href="#" @click="currentSection = 'meme_coins'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'meme_coins' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" :class="currentSection === 'meme_coins' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 00-.707.293l-3 3a1 1 0 001.414 1.414L10 5.414l2.293 2.293a1 1 0 001.414-1.414l-3-3A1 1 0 0010 3zm-3.707 9.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L10 14.586l-2.293-2.293z" clip-rule="evenodd" />
          </svg>
          <span>🪙 Meme Coins</span>
        </a>
        
        <a href="#" @click="currentSection = 'crypto_lt'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'crypto_lt' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" :class="currentSection === 'crypto_lt' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m15 3a3 3 0 11-6 0m6 0a3 3 0 11-6 0" />
          </svg>
          <span>₿ Crypto Long Terme</span>
        </a>
        
        <a href="#" @click="currentSection = 'forex'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'forex' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" :class="currentSection === 'forex' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>💱 Forex</span>
        </a>
        
        <a href="#" @click="currentSection = 'etf'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'etf' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" :class="currentSection === 'etf' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93s.844.091 1.205-.192l.738-.563c.43-.329.957-.326 1.384.007l.494.33c.432.288.597.842.344 1.311l-.437.825c-.24.45-.135 1.003.25 1.372l.738.562c.43.329.432.877 0 1.207l-.738.562c-.386.293-.882.337-1.308.133l-.142-.072a1.192 1.192 0 01-.87-.87c-.063-.299-.22-.574-.455-.791l-.138-.127c-.21-.193-.476-.323-.758-.376s-.587-.01-.844.12L9.07 11.273c-.257.13-.476.337-.656.587l-.26.364a1.19 1.19 0 01-1.037.625H6.018c-.553 0-1.028-.405-1.118-.952L4.73 10.76c-.07-.424-.384-.764-.78-.93s-.844-.091-1.205.192l-.738.563c-.43.329-.957.326-1.384-.007L.13 10.233c-.432-.288-.597-.842-.344-1.311L.223 8.1c.24-.45.135-1.003-.25-1.372L-.765 6.167c-.43-.329-.432-.877 0-1.207l.738-.562c.386-.293.882-.337-1.308.133l.142.072c.299.142.62.199.932.127s.582-.222.772-.477l.35-.456C1.953 2.832 2.5 2.5 3.097 2.5h1.408c.597 0 1.129.303 1.42.772l.26.364c.18.25.438.436.728.533s.597.061.856-.099l.738-.563c.43-.329.957-.326 1.384-.007l.494.33zM19.5 12c0 .996-.386 1.904-.98 2.625L17.545 15.5c-1.084 1.084-2.46 1.84-3.978 2.285S10.5 18.5 9 18.5c-1.582 0-3.1-.598-4.272-1.641S2.5 14.582 2.5 13c0-.996.386-1.904.98-2.625L4.455 9.5c1.084-1.084 2.46-1.84 3.978-2.285S11.5 4.5 13 4.5c1.582 0 3.1.598 4.272 1.641S19.5 8.418 19.5 10c0 .59-.123 1.155-.348 1.672l-.256.606c-.19.45-.135 1.003.25 1.372l.738.562c.05.038.092.082.126.132.212.316.334.69.334 1.093z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8.25a.75.75 0 01.75.75v3.75a.75.75 0 01-1.5 0V9a.75.75 0 01.75-.75z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15a.75.75 0 01.75-.75h.008a.75.75 0 01.75.75v.008a.75.75 0 01-.75.75H12a.75.75 0 01-.75-.75V15z" />
          </svg>
          <span>📈 ETF</span>
        </a>
        
        <a href="#" @click="currentSection = 'ai_insights'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'ai_insights' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" :class="currentSection === 'ai_insights' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 1.255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.759 6.759 0 010-1.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>🧠 AI Insights</span>
        </a>
      </nav>

      <!-- Status Orchestrateur (style professionnel) -->
      <div class="mt-auto border-t border-slate-700 pt-6">
        <div class="text-sm text-slate-400">Status Orchestrateur :</div>
        <div class="text-2xl font-semibold text-slate-100">{{ orchestratorRunning ? '🟢 Actif' : '🔴 Arrêté' }}</div>
        <div :class="['text-sm font-medium', orchestratorStats.success_rate >= 90 ? 'text-green-400' : 'text-yellow-400']">
          {{ orchestratorStats.success_rate || 0 }}% succès
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 space-y-8 overflow-y-auto">
      <header class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-semibold text-slate-100">{{ getSectionTitle() }}</h2>
          <p class="text-slate-400">{{ getSectionSubtitle() }}</p>
        </div>
        <div class="flex items-center space-x-4">
          <button @click="refreshData" class="p-2 rounded-full hover:bg-slate-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
          <!-- Bouton Orchestrateur avec effet aurore professionnel -->
          <button @click="toggleOrchestrator" 
                  :class="['px-4 py-2 rounded-lg font-bold transition-colors text-lg shadow-lg',
                          orchestratorRunning ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-brand-accent hover:bg-sky-500 text-white']">
            {{ orchestratorRunning ? 'ARRÊTER' : 'DÉMARRER' }}
          </button>
          <img src="https://via.placeholder.com/40/38bdf8/ffffff?text=AI" alt="User Avatar" class="w-10 h-10 rounded-full border-2 border-brand-accent">
        </div>
      </header>

      <!-- Overview Section -->
      <div v-if="currentSection === 'overview'" class="space-y-8">
        <!-- Stats Grid -->
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

        <!-- AI Insights Section -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <div class="flex items-center mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-8 h-8 mr-3 text-brand-accent">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.898 20.62L16.5 21.75l-.398-1.13a3.375 3.375 0 00-2.455-2.456L12.75 18l1.13-.398a3.375 3.375 0 002.455-2.456L16.5 14.25l.398 1.13a3.375 3.375 0 002.456 2.456L20.25 18l-1.13.398a3.375 3.375 0 00-2.456 2.456z" />
            </svg>
            <h3 class="text-xl font-semibold text-slate-100">Perspectives de l'IA Orchestrateur</h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="rec in globalRecommendations.slice(0, 3)" :key="`${rec.asset_type}-${rec.task_type}`" class="bg-slate-700/70 p-4 rounded-lg">
              <h4 class="font-semibold text-brand-accent">{{ getAssetEmoji(rec.asset_type) }} {{ formatTaskType(rec.task_type) }}</h4>
              <p class="text-sm text-slate-300 mt-1">{{ rec.reason }}</p>
              <div class="mt-2 flex items-center justify-between text-xs">
                <span class="text-slate-400">{{ rec.frequency_minutes }}min</span>
                <span :class="['px-2 py-1 rounded', getPriorityClass(rec.priority)]">{{ rec.priority }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Asset-specific sections -->
      <div v-if="currentSection !== 'overview'" class="space-y-8">
        <AssetDashboard 
          :asset-type="currentSection"
          :asset-name="getAssetName(currentSection)"
          :recommendations="recommendations[currentSection] || []"
          :color="getAssetColor(currentSection)"
          :description="getAssetDescription(currentSection)"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AssetDashboard from '../components/AssetDashboard.vue'

// État réactif
const currentSection = ref('overview')
const orchestratorRunning = ref(false)
const orchestratorStats = ref({})
const marketConditions = ref({})
const systemStatus = ref({})
const assetStats = ref({})
const recommendations = ref({})
const globalRecommendations = ref([])
const refreshInterval = ref(null)

// Méthodes
const getSectionTitle = () => {
  const titles = {
    overview: 'Dashboard Multi-Assets',
    meme_coins: '🪙 Meme Coins Station',
    crypto_lt: '₿ Crypto Long Terme Station',
    forex: '💱 Forex Trading Station',
    etf: '📈 ETF Investment Station',
    ai_insights: '🧠 AI Insights Hub'
  }
  return titles[currentSection.value] || 'Dashboard'
}

const getSectionSubtitle = () => {
  const subtitles = {
    overview: 'Supervision intelligente de tous vos workflows de trading',
    meme_coins: 'Trading haute fréquence sur meme coins (volatilité > 0.8 requise)',
    crypto_lt: 'Accumulation et rebalancing crypto long terme (optimal en période calme)',
    forex: 'Trading devises pendant sessions actives (8h-17h UTC)',
    etf: 'Investissement systématique ETF (stratégie always-on)',
    ai_insights: 'Analyses prédictives et recommandations de l\'orchestrateur'
  }
  return subtitles[currentSection.value] || 'Tableau de bord'
}

const getAssetName = (assetType) => {
  const names = {
    meme_coins: '🪙 Meme Coins',
    crypto_lt: '₿ Crypto Long Terme',
    forex: '💱 Forex',
    etf: '📈 ETF'
  }
  return names[assetType] || assetType
}

const getAssetColor = (assetType) => {
  const colors = {
    meme_coins: 'purple',
    crypto_lt: 'orange',
    forex: 'blue',
    etf: 'green'
  }
  return colors[assetType] || 'blue'
}

const getAssetDescription = (assetType) => {
  const descriptions = {
    meme_coins: 'Trading haute fréquence sur meme coins (volatilité > 0.8 requise)',
    crypto_lt: 'Accumulation et rebalancing crypto long terme (optimal en période calme < 0.4)',
    forex: 'Trading paires Forex pendant sessions actives (8h-17h UTC)',
    etf: 'Investissement systématique ETF (toujours actif)'
  }
  return descriptions[assetType] || ''
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

const formatTaskType = (taskType) => {
  return taskType
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
}

const getPriorityClass = (priority) => {
  const classes = {
    HIGH: 'bg-red-600 text-white text-xs',
    MEDIUM: 'bg-yellow-600 text-white text-xs',
    LOW: 'bg-green-600 text-white text-xs'
  }
  return classes[priority] || 'bg-slate-600 text-white text-xs'
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
      try {
        const response = await fetch(`/api/orchestrator/recommendations/${assetType}`)
        if (response.ok) {
          const data = await response.json()
          recommendations.value[assetType] = data.recommendations || []
          assetStats.value[assetType] = {
            recommendations: (data.recommendations || []).length,
            active: (data.recommendations || []).length > 0
          }
        }
      } catch (e) {
        console.warn(`Recommandations ${assetType} indisponibles:`, e)
        recommendations.value[assetType] = []
        assetStats.value[assetType] = { recommendations: 0, active: false }
      }
    }
    
    // Global recommendations
    try {
      const globalResponse = await fetch('/api/orchestrator/recommendations')
      if (globalResponse.ok) {
        const globalData = await globalResponse.json()
        globalRecommendations.value = globalData.recommendations || []
      }
    } catch (e) {
      console.warn('Recommandations globales indisponibles:', e)
    }
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
/* Style personnalisé pour la scrollbar (comme dans ton fichier original) */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-track {
  background: #1e293b; /* slate-800 */
}
::-webkit-scrollbar-thumb {
  background: #38bdf8; /* sky-400 */
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #0ea5e9; /* sky-500 */
}

.brand-accent {
  color: #38bdf8;
}
</style> 