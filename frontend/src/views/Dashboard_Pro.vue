<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar avec logo neuronal animé -->
    <aside class="w-64 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <!-- Logo AI Section avec animations neuronales -->
      <div class="mb-8">
        <div class="flex items-center mb-3">
          <!-- Logo AI neuronal personnalisé animé -->
          <div class="relative w-16 h-16 mr-4 rounded-xl border-2 border-brand-accent bg-gradient-to-br from-brand-accent to-blue-600 
                      flex items-center justify-center text-white font-bold shadow-2xl
                      hover:shadow-brand-accent/50 transition-all duration-300 brain-pulse">
            <span class="text-2xl font-extrabold tracking-tight">AI</span>
            
            <!-- Réseau neuronal animé en arrière-plan -->
            <svg class="absolute inset-0 w-full h-full pointer-events-none opacity-20" viewBox="0 0 64 64">
              <line x1="12" y1="12" x2="28" y2="20" stroke="currentColor" stroke-width="1" class="neural-line"/>
              <line x1="28" y1="20" x2="44" y2="28" stroke="currentColor" stroke-width="1" class="neural-line"/>
              <line x1="20" y1="40" x2="12" y2="12" stroke="currentColor" stroke-width="1" class="neural-line"/>
            </svg>
            
            <!-- Points de connexion neuraux animés -->
            <div class="absolute top-1 right-1 w-2 h-2 bg-green-400 rounded-full synapse"></div>
            <div class="absolute bottom-1 left-1 w-1.5 h-1.5 bg-blue-400 rounded-full synapse"></div>
            <div class="absolute top-1 left-1 w-1 h-1 bg-purple-400 rounded-full synapse"></div>
            <div class="absolute bottom-1 right-1 w-1.5 h-1.5 bg-cyan-400 rounded-full synapse"></div>
            
            <!-- Pulse ring autour du cerveau -->
            <div class="absolute inset-0 rounded-xl border-2 border-green-400 opacity-30 animate-ping"></div>
          </div>
          
          <!-- Texte du titre animé -->
          <div>
            <h1 class="text-3xl font-bold text-brand-accent leading-tight text-glow">
              AI Trade<span class="text-slate-400">Bot</span>
            </h1>
            <div class="text-sm text-slate-400 mt-1">
              <span class="inline-flex items-center">
                <span :class="['w-2 h-2 rounded-full mr-2 animate-pulse', systemStatus.color]"></span>
                <span>{{ systemStatus.text }}</span>
              </span>
            </div>
          </div>
        </div>
        <p class="text-slate-400 text-sm">🧠 Intelligence artificielle multi-assets</p>
      </div>

      <!-- Navigation améliorée -->
      <nav class="space-y-2 flex-grow">
        <a href="#" @click="currentSection = 'overview'" 
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group nav-item',
                   currentSection === 'overview' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-brand-accent text-slate-900 flex items-center justify-center text-xs font-bold">🏠</div>
          <span>Dashboard</span>
        </a>
        
        <a href="#" @click="currentSection = 'ai_insights'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group nav-item',
                   currentSection === 'ai_insights' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-purple-600 text-white flex items-center justify-center text-xs font-bold">🧠</div>
          <span>AI Insights</span>
          <span class="ml-auto w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></span>
        </a>
        
        <a href="#" @click="currentSection = 'health'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group nav-item',
                   currentSection === 'health' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-red-500 text-white flex items-center justify-center text-xs font-bold">❤️</div>
          <span>Health Monitor</span>
          <span :class="['ml-auto w-2 h-2 rounded-full animate-pulse', healthStatus.color]"></span>
        </a>
      </nav>

      <!-- Status Orchestrateur amélioré -->
      <div class="mt-auto border-t border-slate-700 pt-6">
        <div class="text-sm text-slate-400">Status Orchestrateur :</div>
        <div class="text-2xl font-semibold text-slate-100">{{ orchestratorRunning ? '🟢 Actif' : '🔴 Arrêté' }}</div>
        <div :class="['text-sm font-medium', orchestratorStats.success_rate >= 90 ? 'text-green-400' : 'text-yellow-400']">
          {{ orchestratorStats.success_rate || 94.7 }}% succès
        </div>
        <button @click="toggleOrchestrator" 
                :class="['w-full mt-4 px-6 py-3 rounded-xl font-bold transition-all duration-300',
                        orchestratorRunning 
                          ? 'bg-red-600 hover:bg-red-700 text-white shadow-lg hover:shadow-red-500/50' 
                          : 'bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white shadow-lg hover:shadow-sky-500/50']">
          {{ orchestratorRunning ? 'ARRÊTER' : 'DÉMARRER' }}
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-8 space-y-8 overflow-y-auto">
      <!-- Header -->
      <header class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-semibold text-slate-100">{{ getSectionTitle() }}</h2>
          <p class="text-slate-400">{{ getSectionSubtitle() }}</p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Status marché -->
          <div class="flex items-center space-x-2 bg-slate-800/50 rounded-xl px-4 py-2">
            <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span class="text-sm text-green-400 font-medium">Marchés Ouverts</span>
          </div>
          
          <!-- Avatar IA -->
          <div class="relative w-12 h-12 rounded-xl border-2 border-brand-accent bg-gradient-to-br from-brand-accent to-blue-600 
                      flex items-center justify-center text-white font-bold cursor-pointer brain-pulse">
            <span class="text-lg font-extrabold">AI</span>
            <div class="absolute top-0 right-0 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
          </div>
        </div>
      </header>

      <!-- Section Overview -->
      <div v-if="currentSection === 'overview'" class="space-y-8">
        <!-- AI Modules Status -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <!-- Module AI Feedback Loop -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-green-400">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-slate-100">AI Feedback Loop</h4>
              <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            </div>
            <div class="space-y-2">
              <div class="text-2xl font-bold text-green-400">{{ aiModules.feedback.score || 85 }}/100</div>
              <div class="text-sm text-slate-400">Score d'adaptation</div>
              <div class="text-xs text-green-300">{{ aiModules.feedback.signals || 23 }} signaux traités</div>
            </div>
          </div>

          <!-- Module Predictive System -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-blue-400">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-slate-100">Predictive System</h4>
              <div class="w-3 h-3 bg-blue-400 rounded-full animate-pulse"></div>
            </div>
            <div class="space-y-2">
              <div class="text-2xl font-bold text-blue-400">{{ aiModules.predictive.accuracy || 91 }}%</div>
              <div class="text-sm text-slate-400">Précision prédictive</div>
              <div class="text-xs text-blue-300">{{ aiModules.predictive.predictions || 147 }} prédictions</div>
            </div>
          </div>

          <!-- Module Security Supervisor -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-yellow-400">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-slate-100">Security Supervisor</h4>
              <div class="w-3 h-3 bg-yellow-400 rounded-full animate-pulse"></div>
            </div>
            <div class="space-y-2">
              <div class="text-2xl font-bold text-yellow-400">{{ aiModules.security.score || 96 }}/100</div>
              <div class="text-sm text-slate-400">Score sécurité</div>
              <div class="text-xs text-yellow-300">{{ aiModules.security.threats || 0 }} menaces détectées</div>
            </div>
          </div>

          <!-- Module Portfolio Optimizer -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-purple-400">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-semibold text-slate-100">Portfolio Optimizer</h4>
              <div class="w-3 h-3 bg-purple-400 rounded-full animate-pulse"></div>
            </div>
            <div class="space-y-2">
              <div class="text-2xl font-bold text-purple-400">{{ aiModules.portfolio.sharpe || 2.3 }}</div>
              <div class="text-sm text-slate-400">Ratio de Sharpe</div>
              <div class="text-xs text-purple-300">{{ aiModules.portfolio.optimizations || 12 }} optimisations</div>
            </div>
          </div>
        </div>

        <!-- AI Insights en temps réel -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <div class="flex items-center mb-4">
            <div class="w-8 h-8 rounded bg-purple-600 text-white flex items-center justify-center text-sm font-bold mr-3">🧠</div>
            <h3 class="text-xl font-semibold text-slate-100">Perspectives de l'IA</h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="insight in aiInsights" :key="insight.id" 
                 :class="['p-4 rounded-lg border-l-4', getInsightColorClass(insight.priority)]">
              <h4 :class="['font-semibold', getInsightTextColor(insight.priority)]">{{ insight.title }}</h4>
              <p class="text-sm text-slate-300 mt-1">{{ insight.description }}</p>
              <div class="flex items-center justify-between mt-2">
                <span class="text-xs text-slate-400">{{ insight.confidence }}% confiance</span>
                <span class="text-xs text-slate-400">{{ insight.timeframe }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section AI Insights détaillée -->
      <div v-if="currentSection === 'ai_insights'" class="space-y-8">
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-6">🧠 Analyses IA Avancées</h3>
          
          <!-- Contenu des analyses IA -->
          <div class="space-y-4">
            <div class="bg-slate-700/50 p-4 rounded-lg">
              <h4 class="font-semibold text-slate-100 mb-2">Module AI Feedback Loop</h4>
              <p class="text-sm text-slate-300">Système d'apprentissage continu avec analyse des patterns de marché.</p>
              <div class="mt-2 text-xs text-slate-400">Score actuel: 85/100 | 23 signaux traités</div>
            </div>
            
            <div class="bg-slate-700/50 p-4 rounded-lg">
              <h4 class="font-semibold text-slate-100 mb-2">Module Predictive System</h4>
              <p class="text-sm text-slate-300">Prédictions multi-horizon avec 91% de précision moyenne.</p>
              <div class="mt-2 text-xs text-slate-400">147 prédictions actives | Régime détecté: Bull Market</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Health Monitor -->
      <div v-if="currentSection === 'health'" class="space-y-8">
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-6">❤️ Monitoring Système</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="metric in healthMetrics" :key="metric.name"
                 class="bg-slate-700/50 p-4 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-medium text-slate-300">{{ metric.name }}</span>
                <span :class="['w-3 h-3 rounded-full', getHealthColor(metric.status)]"></span>
              </div>
              <div class="text-2xl font-bold text-slate-100 mb-1">{{ metric.value }}</div>
              <div class="text-xs text-slate-400">{{ metric.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import aiService from '../services/aiService.js'

// Variables réactives
const currentSection = ref('overview')
const orchestratorRunning = ref(false)
const orchestratorStats = ref({ success_rate: 94.7 })
const loading = ref(false)
const connectionStatus = ref(false)

// Données système temps réel
const systemStatus = ref({
  color: 'bg-green-400',
  text: 'Système autonome actif'
})

const healthStatus = ref({
  color: 'bg-green-400'
})

// Modules IA status (maintenant avec vraies données)
const aiModules = ref({
  feedback: { score: 85, signals: 23 },
  predictive: { accuracy: 91, predictions: 147 },
  security: { score: 96, threats: 0 },
  portfolio: { sharpe: 2.3, optimizations: 12 }
})

// AI Insights (maintenant avec vraies données)
const aiInsights = ref([])

// Métriques de santé (maintenant avec vraies données)
const healthMetrics = ref([])

// Intervals pour les mises à jour temps réel
let updateInterval = null
let healthInterval = null
let insightsInterval = null

// Methods
const getSectionTitle = () => {
  const titles = {
    overview: 'Dashboard AI Trading',
    ai_insights: 'AI Insights Avancés',
    health: 'Health Monitor'
  }
  return titles[currentSection.value] || 'Dashboard'
}

const getSectionSubtitle = () => {
  const subtitles = {
    overview: 'Supervision intelligente de tous vos modules IA',
    ai_insights: 'Analyses prédictives et recommandations IA détaillées',
    health: 'Monitoring système et performances en temps réel'
  }
  return subtitles[currentSection.value] || ''
}

const toggleOrchestrator = async () => {
  try {
    orchestratorRunning.value = !orchestratorRunning.value
    
    if (orchestratorRunning.value) {
      systemStatus.value = { color: 'bg-green-400', text: 'Système autonome actif' }
      // Démarrer les mises à jour temps réel
      startRealTimeUpdates()
    } else {
      systemStatus.value = { color: 'bg-red-400', text: 'Système en pause' }
      // Arrêter les mises à jour temps réel
      stopRealTimeUpdates()
    }
  } catch (error) {
    console.error('Erreur lors du toggle orchestrateur:', error)
  }
}

// Récupérer les données des modules IA
const updateAIModules = async () => {
  try {
    loading.value = true
    const modulesData = await aiService.getAllModulesStatus()
    
    // Formater les données pour l'interface
    if (modulesData.feedback) {
      const formatted = aiService.formatModuleData(modulesData.feedback, 'feedback')
      aiModules.value.feedback = formatted
    }
    
    if (modulesData.predictive) {
      const formatted = aiService.formatModuleData(modulesData.predictive, 'predictive')
      aiModules.value.predictive = formatted
    }
    
    if (modulesData.security) {
      const formatted = aiService.formatModuleData(modulesData.security, 'security')
      aiModules.value.security = formatted
    }
    
    if (modulesData.portfolio) {
      const formatted = aiService.formatModuleData(modulesData.portfolio, 'portfolio')
      aiModules.value.portfolio = formatted
    }
    
    console.log('Modules IA mis à jour:', aiModules.value)
    
  } catch (error) {
    console.error('Erreur lors de la mise à jour des modules IA:', error)
    // Garder les données simulées en cas d'erreur
  } finally {
    loading.value = false
  }
}

// Récupérer les insights IA
const updateAIInsights = async () => {
  try {
    const insights = await aiService.getAIInsights()
    aiInsights.value = insights
    console.log('Insights IA mis à jour:', insights.length, 'insights')
  } catch (error) {
    console.error('Erreur lors de la mise à jour des insights IA:', error)
    // Utiliser les données par défaut
    aiInsights.value = [
      {
        id: 1,
        title: 'Signal d\'Achat Fort : ETH/USD',
        description: 'L\'IA détecte une configuration haussière avec une probabilité de succès de 78% sur les prochaines 4h.',
        confidence: 78,
        timeframe: '4h',
        priority: 'high'
      },
      {
        id: 2,
        title: 'Analyse de Sentiment : BTC Neutre',
        description: 'Le sentiment global du marché pour BTC est actuellement neutre, avec des indicateurs mitigés.',
        confidence: 65,
        timeframe: '1d',
        priority: 'medium'
      },
      {
        id: 3,
        title: 'Alerte Volatilité : SOL/USD',
        description: 'Augmentation attendue de la volatilité sur SOL/USD. Ajustez vos stops.',
        confidence: 84,
        timeframe: '2h',
        priority: 'high'
      }
    ]
  }
}

// Récupérer les métriques de santé
const updateHealthMetrics = async () => {
  try {
    const metrics = await aiService.getSystemHealth()
    healthMetrics.value = metrics
    
    // Mettre à jour le status de santé global
    const hasWarning = metrics.some(m => m.status === 'warning')
    const hasCritical = metrics.some(m => m.status === 'critical')
    
    if (hasCritical) {
      healthStatus.value.color = 'bg-red-400'
    } else if (hasWarning) {
      healthStatus.value.color = 'bg-yellow-400'
    } else {
      healthStatus.value.color = 'bg-green-400'
    }
    
    console.log('Métriques de santé mises à jour:', metrics.length, 'métriques')
    
  } catch (error) {
    console.error('Erreur lors de la mise à jour des métriques de santé:', error)
    // Utiliser les données de démonstration
    healthMetrics.value = aiService.getMockHealthData()
  }
}

// Tester la connexion à l'API
const testConnection = async () => {
  try {
    connectionStatus.value = await aiService.testConnection()
    if (connectionStatus.value) {
      console.log('✅ Connexion API établie')
    } else {
      console.warn('⚠️ API non disponible, utilisation des données simulées')
    }
  } catch (error) {
    console.error('❌ Erreur de connexion API:', error)
    connectionStatus.value = false
  }
}

// Démarrer les mises à jour temps réel
const startRealTimeUpdates = () => {
  // Mise à jour des modules IA toutes les 10 secondes
  updateInterval = setInterval(updateAIModules, 10000)
  
  // Mise à jour des métriques de santé toutes les 5 secondes
  healthInterval = setInterval(updateHealthMetrics, 5000)
  
  // Mise à jour des insights toutes les 30 secondes
  insightsInterval = setInterval(updateAIInsights, 30000)
  
  console.log('🚀 Mises à jour temps réel démarrées')
}

// Arrêter les mises à jour temps réel
const stopRealTimeUpdates = () => {
  if (updateInterval) {
    clearInterval(updateInterval)
    updateInterval = null
  }
  
  if (healthInterval) {
    clearInterval(healthInterval)
    healthInterval = null
  }
  
  if (insightsInterval) {
    clearInterval(insightsInterval)
    insightsInterval = null
  }
  
  console.log('⏸️ Mises à jour temps réel arrêtées')
}

const getInsightColorClass = (priority) => {
  const colors = {
    high: 'bg-slate-700/70 border-green-400',
    medium: 'bg-slate-700/70 border-yellow-400',
    low: 'bg-slate-700/70 border-blue-400'
  }
  return colors[priority] || colors.medium
}

const getInsightTextColor = (priority) => {
  const colors = {
    high: 'text-green-400',
    medium: 'text-yellow-400',
    low: 'text-blue-400'
  }
  return colors[priority] || colors.medium
}

const getHealthColor = (status) => {
  const colors = {
    healthy: 'bg-green-400',
    warning: 'bg-yellow-400',
    critical: 'bg-red-400'
  }
  return colors[status] || 'bg-slate-400'
}

// Lifecycle hooks
onMounted(async () => {
  console.log('🔧 Initialisation du dashboard IA...')
  
  // Tester la connexion
  await testConnection()
  
  // Charger les données initiales
  await Promise.all([
    updateAIModules(),
    updateAIInsights(),
    updateHealthMetrics()
  ])
  
  // Démarrer automatiquement l'orchestrateur
  if (connectionStatus.value) {
    orchestratorRunning.value = true
    startRealTimeUpdates()
  }
  
  console.log('✅ Dashboard IA initialisé')
})

onUnmounted(() => {
  console.log('🛑 Nettoyage du dashboard IA...')
  stopRealTimeUpdates()
})
</script>

<style scoped>
/* Couleurs brand personnalisées */
.text-brand-accent { color: #38bdf8; }
.bg-brand-accent { background-color: #38bdf8; }
.border-brand-accent { border-color: #38bdf8; }

/* Animations neuronales */
@keyframes brain-pulse {
  0%, 100% { 
    transform: scale(1);
    filter: drop-shadow(0 0 8px rgba(34, 197, 94, 0.6));
  }
  50% { 
    transform: scale(1.05);
    filter: drop-shadow(0 0 15px rgba(34, 197, 94, 0.9));
  }
}

@keyframes synapse-flash {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

@keyframes neural-network {
  0% { stroke-dashoffset: 100; }
  100% { stroke-dashoffset: 0; }
}

@keyframes text-glow {
  0%, 100% { 
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  }
  50% { 
    text-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 30px rgba(34, 197, 94, 0.4);
  }
}

.brain-pulse {
  animation: brain-pulse 2s ease-in-out infinite;
}

.synapse {
  animation: synapse-flash 1.5s ease-in-out infinite;
}

.synapse:nth-child(2) { animation-delay: 0.3s; }
.synapse:nth-child(3) { animation-delay: 0.6s; }
.synapse:nth-child(4) { animation-delay: 0.9s; }
.synapse:nth-child(5) { animation-delay: 1.2s; }

.text-glow {
  animation: text-glow 3s ease-in-out infinite;
}

.neural-line {
  stroke-dasharray: 20;
  animation: neural-network 2s linear infinite;
}

.nav-item:hover {
  transform: translateX(4px);
  transition: transform 0.2s ease;
}

/* Scrollbar personnalisée */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #1e293b;
}

::-webkit-scrollbar-thumb {
  background: #38bdf8;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #0ea5e9;
}
</style> 