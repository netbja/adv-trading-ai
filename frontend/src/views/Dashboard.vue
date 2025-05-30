<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <div>
        <h1 class="text-3xl font-bold text-brand-accent flex items-center">
          <SparklesIcon class="w-8 h-8 mr-2" />
          AI Trade<span class="text-slate-400">Bot</span>
        </h1>
      </div>

      <nav class="space-y-2 flex-grow">
        <a href="#" @click="currentSection = 'dashboard'" 
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'dashboard' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <HomeIcon class="h-5 w-5" />
          <span>Dashboard</span>
        </a>
        <a href="#" @click="currentSection = 'trading'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'trading' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <ChartBarIcon class="h-5 w-5" />
          <span>Trade Station</span>
        </a>
        <a href="#" @click="currentSection = 'portfolio'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'portfolio' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <WalletIcon class="h-5 w-5" />
          <span>Portefeuille ETF</span>
        </a>
        <a href="#" @click="currentSection = 'ai'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'ai' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <CpuChipIcon class="h-5 w-5" />
          <span>AI Insights</span>
        </a>
        <a href="#" @click="currentSection = 'settings'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'settings' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <Cog6ToothIcon class="h-5 w-5" />
          <span>Paramètres</span>
        </a>
      </nav>

      <div class="mt-auto border-t border-slate-700 pt-6">
        <div class="text-sm text-slate-400">Capital Total ETF :</div>
        <div class="text-2xl font-semibold text-slate-100">${{ portfolioValue.toLocaleString() }}</div>
        <div :class="['text-sm font-medium', dailyChange >= 0 ? 'text-green-400' : 'text-red-400']">
          {{ dailyChange >= 0 ? '+' : '' }}{{ dailyChange.toFixed(2) }}% aujourd'hui
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

      <!-- Dashboard Section -->
      <div v-if="currentSection === 'dashboard'" class="space-y-8">
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-brand-accent">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">Capital ETF</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">${{ portfolioValue.toLocaleString() }}</p>
            <span :class="['text-sm font-medium', dailyChange >= 0 ? 'text-green-400' : 'text-red-400']">
              {{ dailyChange >= 0 ? '+' : '' }}{{ dailyChange.toFixed(2) }}%
            </span>
          </div>

          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-green-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">ETF Actifs</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ activeETFs }}</p>
            <span class="text-sm font-medium text-green-400">Diversifié</span>
          </div>

          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-blue-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">Signaux IA</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ aiSignals }}</p>
            <span class="text-sm font-medium text-slate-300">Aujourd'hui</span>
          </div>

          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl border-l-4 border-yellow-500">
            <h3 class="text-sm text-slate-400 uppercase tracking-wide">Système IA</h3>
            <p class="text-2xl font-bold text-slate-100 mt-2">{{ systemHealth }}%</p>
            <span class="text-sm font-medium text-green-400">Opérationnel</span>
          </div>
        </div>

        <!-- AI Insights Section -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <div class="flex items-center mb-4">
            <CpuChipIcon class="w-8 h-8 mr-3 text-brand-accent" />
            <h3 class="text-xl font-semibold text-slate-100">Perspectives IA ETF</h3>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="insight in aiInsights" :key="insight.id" class="bg-slate-700/70 p-4 rounded-lg">
              <h4 :class="['font-semibold', getInsightColor(insight.type)]">{{ insight.title }}</h4>
              <p class="text-sm text-slate-300 mt-1">{{ insight.description }}</p>
              <div class="mt-2 flex items-center text-xs text-slate-400">
                <ClockIcon class="w-4 h-4 mr-1" />
                {{ insight.timestamp }}
              </div>
            </div>
          </div>
        </div>

        <!-- Portfolio Allocation -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">Allocation ETF Intelligente</h3>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div class="space-y-4">
              <div v-for="allocation in portfolioAllocations" :key="allocation.symbol" 
                   class="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                <div class="flex items-center space-x-3">
                  <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: allocation.color }"></div>
                  <div>
                    <div class="font-medium text-slate-100">{{ allocation.name }}</div>
                    <div class="text-sm text-slate-400">{{ allocation.symbol }}</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-slate-100">{{ allocation.percentage }}%</div>
                  <div :class="['text-sm', allocation.change >= 0 ? 'text-green-400' : 'text-red-400']">
                    {{ allocation.change >= 0 ? '+' : '' }}{{ allocation.change.toFixed(2) }}%
                  </div>
                </div>
              </div>
            </div>
            <div class="flex items-center justify-center">
              <div class="text-slate-400">
                [Graphique en anneau allocation ETF]
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Trading Section -->
      <div v-if="currentSection === 'trading'" class="space-y-8">
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">Station de Trading ETF</h3>
          <p class="text-slate-400">Les ordres ETF sont gérés automatiquement par l'IA. Interface de monitoring uniquement.</p>
        </div>
      </div>

      <!-- Portfolio Section -->
      <div v-if="currentSection === 'portfolio'" class="space-y-8">
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">Portefeuille ETF Détaillé</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-sm text-left text-slate-300">
              <thead class="text-xs text-slate-400 uppercase bg-slate-700/50">
                <tr>
                  <th class="px-6 py-3">ETF</th>
                  <th class="px-6 py-3">Allocation</th>
                  <th class="px-6 py-3">Valeur</th>
                  <th class="px-6 py-3">Performance</th>
                  <th class="px-6 py-3">Statut IA</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-700">
                <tr v-for="etf in detailedPortfolio" :key="etf.symbol" class="hover:bg-slate-700/30">
                  <td class="px-6 py-4 font-medium text-slate-100">{{ etf.name }}</td>
                  <td class="px-6 py-4">{{ etf.allocation }}%</td>
                  <td class="px-6 py-4">${{ etf.value.toLocaleString() }}</td>
                  <td :class="['px-6 py-4', etf.performance >= 0 ? 'text-green-400' : 'text-red-400']">
                    {{ etf.performance >= 0 ? '+' : '' }}{{ etf.performance.toFixed(2) }}%
                  </td>
                  <td class="px-6 py-4">
                    <span :class="['px-2 py-1 text-xs rounded-full', getStatusClass(etf.aiStatus)]">
                      {{ etf.aiStatus }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { 
  SparklesIcon, 
  HomeIcon, 
  ChartBarIcon, 
  WalletIcon, 
  CpuChipIcon,
  Cog6ToothIcon,
  ArrowPathIcon,
  PowerIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

// État réactif
const currentSection = ref('dashboard')
const portfolioValue = ref(125430.50)
const dailyChange = ref(2.45)
const activeETFs = ref(8)
const aiSignals = ref(12)
const systemHealth = ref(98)

// Données mock pour démonstration
const aiInsights = ref([
  {
    id: 1,
    type: 'buy',
    title: 'Signal d\'Achat Fort : VTI',
    description: 'L\'IA détecte une opportunité d\'accumulation sur l\'ETF Vanguard Total Stock Market avec une probabilité de succès de 82%.',
    timestamp: 'Il y a 15 min'
  },
  {
    id: 2,
    type: 'neutral',
    title: 'Analyse Sectorielle : Tech Stable',
    description: 'Le secteur technologique (QQQ) montre des signaux neutres. Maintien de l\'allocation recommandé.',
    timestamp: 'Il y a 1h'
  },
  {
    id: 3,
    type: 'warning',
    title: 'Alerte Rebalancing : VXUS',
    description: 'L\'ETF international dépasse l\'allocation cible de 2%. Rebalancing automatique programmé.',
    timestamp: 'Il y a 2h'
  }
])

const portfolioAllocations = ref([
  { symbol: 'VTI', name: 'Vanguard Total Stock Market', percentage: 35, change: 1.2, color: '#22c55e' },
  { symbol: 'VTIAX', name: 'Vanguard Total International', percentage: 25, change: -0.5, color: '#3b82f6' },
  { symbol: 'QQQ', name: 'Invesco QQQ Trust', percentage: 20, change: 2.1, color: '#8b5cf6' },
  { symbol: 'BND', name: 'Vanguard Total Bond Market', percentage: 15, change: 0.1, color: '#f59e0b' },
  { symbol: 'VNQ', name: 'Vanguard Real Estate', percentage: 5, change: -1.2, color: '#ef4444' }
])

const detailedPortfolio = ref([
  { symbol: 'VTI', name: 'Vanguard Total Stock Market ETF', allocation: 35, value: 43900, performance: 1.2, aiStatus: 'HOLD' },
  { symbol: 'VTIAX', name: 'Vanguard Total International', allocation: 25, value: 31350, performance: -0.5, aiStatus: 'ACCUMULATE' },
  { symbol: 'QQQ', name: 'Invesco QQQ Trust', allocation: 20, value: 25086, performance: 2.1, aiStatus: 'HOLD' },
  { symbol: 'BND', name: 'Vanguard Total Bond Market', allocation: 15, value: 18814, performance: 0.1, aiStatus: 'REDUCE' },
  { symbol: 'VNQ', name: 'Vanguard Real Estate ETF', allocation: 5, value: 6270, performance: -1.2, aiStatus: 'HOLD' }
])

// Méthodes
const getSectionTitle = () => {
  const titles = {
    dashboard: 'Dashboard ETF IA',
    trading: 'Station de Trading',
    portfolio: 'Portefeuille ETF',
    ai: 'Intelligence Artificielle',
    settings: 'Paramètres'
  }
  return titles[currentSection.value] || 'Dashboard'
}

const getSectionSubtitle = () => {
  const subtitles = {
    dashboard: 'Vue d\'ensemble de votre portefeuille ETF intelligent',
    trading: 'Monitoring des ordres automatiques IA',
    portfolio: 'Analyse détaillée de vos investissements ETF',
    ai: 'Insights et recommandations de l\'IA',
    settings: 'Configuration du système de trading'
  }
  return subtitles[currentSection.value] || 'Tableau de bord'
}

const getInsightColor = (type) => {
  const colors = {
    buy: 'text-brand-buy',
    sell: 'text-brand-sell',
    neutral: 'text-slate-200',
    warning: 'text-yellow-400'
  }
  return colors[type] || 'text-slate-200'
}

const getStatusClass = (status) => {
  const classes = {
    'HOLD': 'bg-blue-900 text-blue-300',
    'ACCUMULATE': 'bg-green-900 text-green-300',
    'REDUCE': 'bg-red-900 text-red-300'
  }
  return classes[status] || 'bg-slate-900 text-slate-300'
}

const refreshData = () => {
  console.log('🔄 Actualisation des données ETF...')
  // Simulation d'actualisation
  portfolioValue.value = portfolioValue.value + (Math.random() - 0.5) * 1000
  dailyChange.value = dailyChange.value + (Math.random() - 0.5) * 0.5
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3498db;
}

.stat-card h3 {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  text-transform: uppercase;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
  color: #2c3e50;
}

.stat-change.positive {
  color: #27ae60;
}

.stat-change.neutral {
  color: #7f8c8d;
}

.stat-status.active {
  color: #27ae60;
  font-weight: bold;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background: #7f8c8d;
}
</style> 