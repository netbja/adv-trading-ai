<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <!-- Logo AI personnalisé SANS dépendance externe -->
      <div class="mb-8">
        <div class="flex items-center mb-3">
          <!-- Logo AI neuronal personnalisé et GROS -->
          <div class="relative w-16 h-16 mr-4 rounded-xl border-2 border-brand-accent bg-gradient-to-br from-brand-accent to-blue-600 
                      flex items-center justify-center text-white font-bold shadow-2xl
                      hover:shadow-brand-accent/50 transition-all duration-300">
            <span class="text-2xl font-extrabold tracking-tight">AI</span>
            <!-- Effet réseau neuronal en arrière-plan -->
            <div class="absolute inset-0 rounded-xl border-2 border-brand-accent/20 scale-110 opacity-0 
                        hover:opacity-100 hover:scale-125 transition-all duration-500"></div>
            <!-- Points de connexion neuraux -->
            <div class="absolute top-1 right-1 w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <div class="absolute bottom-1 left-1 w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse delay-300"></div>
            <div class="absolute top-1 left-1 w-1 h-1 bg-purple-400 rounded-full animate-pulse delay-700"></div>
          </div>
          
          <!-- Texte du titre -->
          <div>
            <h1 class="text-3xl font-bold text-brand-accent leading-tight">
              AI Trade<span class="text-slate-400">Bot</span>
            </h1>
            <div class="text-sm text-slate-400 mt-1">
              <span class="inline-flex items-center">
                <span class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                Système autonome actif
              </span>
            </div>
          </div>
        </div>
        <p class="text-slate-400 text-sm">🧠 Intelligence artificielle multi-assets</p>
      </div>

      <nav class="space-y-2 flex-grow">
        <!-- Navigation items restent identiques mais sans les icônes problématiques -->
        <a href="#" @click="currentSection = 'overview'" 
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'overview' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-brand-accent text-slate-900 flex items-center justify-center text-xs font-bold">🏠</div>
          <span>Dashboard</span>
        </a>
        
        <a href="#" @click="currentSection = 'meme_coins'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'meme_coins' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-purple-500 text-white flex items-center justify-center text-xs font-bold">🪙</div>
          <span>Meme Coins</span>
        </a>
        
        <a href="#" @click="currentSection = 'crypto_lt'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'crypto_lt' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-orange-500 text-white flex items-center justify-center text-xs font-bold">₿</div>
          <span>Crypto Long Terme</span>
        </a>
        
        <a href="#" @click="currentSection = 'forex'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'forex' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-blue-500 text-white flex items-center justify-center text-xs font-bold">💱</div>
          <span>Forex</span>
        </a>
        
        <a href="#" @click="currentSection = 'etf'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'etf' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-green-500 text-white flex items-center justify-center text-xs font-bold">📈</div>
          <span>ETF</span>
        </a>
        
        <a href="#" @click="currentSection = 'ai_insights'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'ai_insights' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-purple-600 text-white flex items-center justify-center text-xs font-bold">🧠</div>
          <span>AI Insights</span>
        </a>
        
        <a href="#" @click="currentSection = 'health'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'health' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-red-500 text-white flex items-center justify-center text-xs font-bold">❤️</div>
          <span>Health Monitor</span>
        </a>
        
        <a href="#" @click="currentSection = 'settings'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'settings' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-slate-600 text-white flex items-center justify-center text-xs font-bold">⚙️</div>
          <span>Settings</span>
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

    <!-- Main Content reste identique... -->
    <main class="flex-1 p-8 space-y-8 overflow-y-auto">
      <header class="flex justify-between items-center">
        <div>
          <h2 class="text-3xl font-semibold text-slate-100">{{ getSectionTitle() }}</h2>
          <p class="text-slate-400">{{ getSectionSubtitle() }}</p>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Bouton DÉMARRER/ARRÊTER plus visible -->
          <div class="relative">
            <button @click="toggleOrchestrator" 
                    :class="['px-8 py-4 rounded-xl font-bold transition-all duration-300 text-xl shadow-2xl relative overflow-hidden group',
                            orchestratorRunning 
                              ? 'bg-red-600 hover:bg-red-700 text-white ring-4 ring-red-300/50 hover:ring-red-300 hover:shadow-red-400/50' 
                              : 'bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white ring-4 ring-sky-300/50 hover:ring-sky-300 hover:shadow-sky-400/50']">
              <span class="relative z-10">{{ orchestratorRunning ? 'ARRÊTER' : 'DÉMARRER' }}</span>
            </button>
          </div>
          
          <!-- Avatar IA ENCORE plus gros -->
          <div class="relative w-20 h-20 rounded-2xl border-4 border-brand-accent bg-gradient-to-br from-brand-accent to-blue-500 
                      flex items-center justify-center text-white font-bold shadow-2xl
                      hover:shadow-brand-accent/50 transition-all duration-300 cursor-pointer group">
            <span class="text-3xl font-extrabold">AI</span>
            <!-- Points neuraux multiples -->
            <div class="absolute top-2 right-2 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <div class="absolute bottom-2 left-2 w-2 h-2 bg-blue-400 rounded-full animate-pulse delay-300"></div>
            <div class="absolute top-2 left-2 w-1.5 h-1.5 bg-purple-400 rounded-full animate-pulse delay-700"></div>
            <div class="absolute bottom-2 right-2 w-2 h-2 bg-pink-400 rounded-full animate-pulse delay-1000"></div>
          </div>
        </div>
      </header>

      <!-- Le reste du contenu... Message pour dire que c'est un aperçu -->
      <div class="bg-slate-800 p-8 rounded-xl shadow-2xl text-center">
        <h3 class="text-2xl font-bold text-brand-accent mb-4">✅ LOGO CORRIGÉ !</h3>
        <div class="space-y-4 text-slate-300">
          <p><strong>🔧 Problèmes résolus :</strong></p>
          <ul class="text-left space-y-2">
            <li>✅ Logo AI plus GROS (64x64px au lieu de 40x40px)</li>
            <li>✅ Plus de flash de texte "TradeBot AI" (SparklesIcon supprimé)</li>
            <li>✅ Logo neuronal personnalisé avec effets visuels</li>
            <li>✅ Points de connexion neuraux animés</li>
            <li>✅ Bouton DÉMARRER/ARRÊTER plus visible</li>
            <li>✅ Avatar AI encore plus gros dans l'en-tête</li>
          </ul>
          <p class="text-brand-accent font-semibold">Copie ce fichier vers Dashboard.vue pour appliquer les corrections !</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Variables réactives de base
const currentSection = ref('overview')
const orchestratorRunning = ref(false)
const orchestratorStats = ref({})

// Methods de base
const getSectionTitle = () => {
  const titles = {
    overview: 'Dashboard Multi-Assets',
    meme_coins: 'Meme Coins Trading',
    crypto_lt: 'Crypto Long Terme', 
    forex: 'Forex Trading',
    etf: 'ETF Portfolio',
    ai_insights: 'AI Insights',
    health: 'Health Monitor',
    settings: 'Configuration'
  }
  return titles[currentSection.value] || 'Dashboard'
}

const getSectionSubtitle = () => {
  const subtitles = {
    overview: 'Supervision intelligente de tous vos workflows de trading',
    meme_coins: 'Trading haute fréquence sur tokens volatils',
    crypto_lt: 'Stratégie DCA et holding long terme',
    forex: 'Trading algorithmique sur devises',
    etf: 'Allocation portfolio diversifié',
    ai_insights: 'Analyses prédictives et recommandations IA',
    health: 'Monitoring système et performances',
    settings: 'Configuration des paramètres IA'
  }
  return subtitles[currentSection.value] || ''
}

const toggleOrchestrator = () => {
  orchestratorRunning.value = !orchestratorRunning.value
}

onMounted(() => {
  console.log('Dashboard corrigé chargé !')
})
</script>

<style scoped>
/* Style personnalisé pour la scrollbar */
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

.brand-accent {
  color: #38bdf8;
}
</style> 