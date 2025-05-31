<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <!-- Header simplifié -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-brand-accent leading-tight">
          Trading<span class="text-slate-400">Pro</span>
        </h1>
        <div class="text-sm text-slate-400 mt-1">
          <span class="inline-flex items-center">
            <span class="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
            Système autonome actif
          </span>
        </div>
        <p class="text-slate-400 text-xs mt-1">🚀 Trading intelligent multi-assets</p>
      </div>

      <nav class="space-y-2 flex-grow">
        <!-- Navigation items -->
        <a href="#" @click="currentSection = 'overview'" 
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'overview' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-brand-accent text-slate-900 flex items-center justify-center text-xs font-bold">🏠</div>
          <span>Dashboard</span>
        </a>
        
        <a href="#" @click="currentSection = 'ai_modules'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'ai_modules' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-purple-600 text-white flex items-center justify-center text-xs font-bold">🧠</div>
          <span>Modules IA</span>
        </a>
        
        <a href="#" @click="currentSection = 'paper_trading'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'paper_trading' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-yellow-600 text-white flex items-center justify-center text-xs font-bold">🧪</div>
          <span>Paper Trading</span>
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
        
        <a href="#" @click="currentSection = 'portfolio_global'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'portfolio_global' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-indigo-500 text-white flex items-center justify-center text-xs font-bold">💼</div>
          <span>Portfolio Global</span>
        </a>
        
        <a href="#" @click="currentSection = 'analytics'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'analytics' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-cyan-500 text-white flex items-center justify-center text-xs font-bold">📊</div>
          <span>Analytics</span>
        </a>
        
        <a href="#" @click="currentSection = 'historique'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'historique' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <div class="w-5 h-5 rounded bg-amber-500 text-white flex items-center justify-center text-xs font-bold">📜</div>
          <span>Historique</span>
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

      <!-- Status Orchestrateur -->
      <div class="mt-auto border-t border-slate-700 pt-6">
        <div class="text-sm text-slate-400">Status Orchestrateur :</div>
        <div class="text-xl font-semibold text-slate-100">{{ orchestratorRunning ? '🟢 Actif' : '🔴 Arrêté' }}</div>
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
          <!-- Bouton DÉMARRER/ARRÊTER -->
            <button @click="toggleOrchestrator" 
                  :class="['px-6 py-3 rounded-xl font-bold transition-all duration-300 shadow-lg',
                            orchestratorRunning 
                            ? 'bg-red-600 hover:bg-red-700 text-white' 
                            : 'bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white']">
            {{ orchestratorRunning ? 'ARRÊTER' : 'DÉMARRER' }}
          </button>
          
          <!-- Status IA compact (sans gros logo) -->
          <div class="flex items-center space-x-2 bg-slate-800 px-4 py-2 rounded-lg">
            <div class="text-sm">
              <div class="text-slate-300 font-medium">4/4 Modules IA</div>
              <div class="text-green-400 text-xs">✅ Tous Actifs</div>
            </div>
          </div>
        </div>
      </header>

      <!-- Contenu dynamique -->
      <div v-if="currentSection === 'overview'">
        <!-- Dashboard Overview -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- Cartes de métriques -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-semibold text-slate-300">Portfolio Total</h3>
                <p class="text-3xl font-bold text-green-400">{{ formatCurrency(systemMetrics.totalValue) }}</p>
                <p class="text-sm text-green-300">{{ formatPercentage(systemMetrics.change) }} aujourd'hui</p>
              </div>
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <span class="text-2xl">💰</span>
              </div>
            </div>
          </div>
          
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-semibold text-slate-300">Trades Actifs</h3>
                <p class="text-3xl font-bold text-blue-400">{{ formatNumber(systemMetrics.activeTrades) }}</p>
                <p class="text-sm text-blue-300">8 profits, 4 en cours</p>
              </div>
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <span class="text-2xl">📊</span>
              </div>
            </div>
          </div>
          
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-semibold text-slate-300">Score IA</h3>
                <p class="text-3xl font-bold text-purple-400">{{ formatNumber(systemMetrics.aiScore) }}%</p>
                <p class="text-sm text-purple-300">Performance excellente</p>
              </div>
              <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <span class="text-2xl">🧠</span>
              </div>
            </div>
          </div>
          
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg font-semibold text-slate-300">Sécurité</h3>
                <p class="text-3xl font-bold text-green-400">{{ formatNumber(systemMetrics.securityScore) }}/100</p>
                <p class="text-sm text-green-300">Système sécurisé</p>
              </div>
              <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <span class="text-2xl">🛡️</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Graphique principal -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">Performance Portfolio (30 jours)</h3>
          <div class="h-64 bg-slate-700 rounded-lg flex items-center justify-center">
            <p class="text-slate-400">Graphique de performance - À intégrer avec Chart.js</p>
          </div>
        </div>
      </div>

      <!-- Section Modules IA -->
      <div v-else-if="currentSection === 'ai_modules'" class="space-y-6">
        <!-- En-tête avec boutons de contrôle -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-2xl font-bold text-brand-accent">🧠 Modules IA Avancée (16 Endpoints)</h3>
            <div class="flex space-x-3">
              <button @click="testAllModules" 
                      :disabled="loading"
                      class="px-4 py-2 bg-brand-accent hover:bg-blue-500 disabled:bg-gray-600 rounded-lg text-white font-medium transition-colors">
                {{ loading ? '⏳ Test...' : '🚀 Tester Tous' }}
              </button>
              <button @click="loadModulesData" 
                      :disabled="loading"
                      class="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 rounded-lg text-white font-medium transition-colors">
                {{ loading ? '⏳' : '🔄 Actualiser' }}
              </button>
            </div>
          </div>
          
          <!-- Status général des modules -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-slate-700 p-4 rounded-lg border border-purple-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Feedback Loop</h4>
                  <p :class="getModuleStatus(modulesData.feedback).color" class="text-lg font-bold">
                    {{ modulesData.feedback ? '✅ Actif' : '❌ Inactif' }}
                  </p>
                </div>
                <div class="text-2xl">🔄</div>
              </div>
            </div>
            
            <div class="bg-slate-700 p-4 rounded-lg border border-blue-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Predictive</h4>
                  <p :class="getModuleStatus(modulesData.predictive).color" class="text-lg font-bold">
                    {{ modulesData.predictive ? '✅ Actif' : '❌ Inactif' }}
                  </p>
                </div>
                <div class="text-2xl">🔮</div>
              </div>
            </div>
            
            <div class="bg-slate-700 p-4 rounded-lg border border-red-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Security</h4>
                  <p :class="getModuleStatus(modulesData.security).color" class="text-lg font-bold">
                    {{ modulesData.security ? '✅ Actif' : '❌ Inactif' }}
                  </p>
                </div>
                <div class="text-2xl">🛡️</div>
              </div>
            </div>
            
            <div class="bg-slate-700 p-4 rounded-lg border border-green-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Portfolio</h4>
                  <p :class="getModuleStatus(modulesData.portfolio).color" class="text-lg font-bold">
                    {{ modulesData.portfolio ? '✅ Actif' : '❌ Inactif' }}
                  </p>
                </div>
                <div class="text-2xl">📊</div>
              </div>
            </div>
          </div>
          
          <!-- Grille des modules IA avec tous les endpoints -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- AI Feedback Loop (4 endpoints) -->
            <div class="bg-slate-700 p-4 rounded-lg border border-purple-500/30">
              <h4 class="text-lg font-semibold text-purple-400 mb-2">🔄 Feedback Loop</h4>
              <p class="text-sm text-slate-300 mb-3">Apprentissage continu</p>
              <div class="space-y-2">
                <button @click="testEndpoint('/advanced-ai/feedback/patterns')" 
                        class="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm transition-colors">
                  📋 Patterns
                </button>
                <button @click="testEndpoint('/advanced-ai/feedback/adaptations')" 
                        class="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm transition-colors">
                  🔄 Adaptations
                </button>
                <button @click="submitLearningSignal" 
                        class="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm transition-colors">
                  📤 Submit Signal
                </button>
                <button @click="analyzePerformance" 
                        class="w-full px-3 py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm transition-colors">
                  📊 Analyze Perf
                </button>
              </div>
            </div>
            
            <!-- Predictive System (4 endpoints) -->
            <div class="bg-slate-700 p-4 rounded-lg border border-blue-500/30">
              <h4 class="text-lg font-semibold text-blue-400 mb-2">🔮 Predictive</h4>
              <p class="text-sm text-slate-300 mb-3">Prédictions marché</p>
              <div class="space-y-2">
                <button @click="testEndpoint('/advanced-ai/prediction/regime')" 
                        class="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors">
                  📈 Régime
                </button>
                <button @click="testEndpoint('/advanced-ai/prediction/alerts')" 
                        class="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors">
                  🚨 Alertes
                </button>
                <button @click="generatePrediction" 
                        class="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors">
                  🔮 Prédiction
                </button>
                <button @click="getHistoricalAnalysis" 
                        class="w-full px-3 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm transition-colors">
                  📊 Analyse
                </button>
              </div>
            </div>
            
            <!-- Security Supervisor (4 endpoints) -->
            <div class="bg-slate-700 p-4 rounded-lg border border-red-500/30">
              <h4 class="text-lg font-semibold text-red-400 mb-2">🛡️ Security</h4>
              <p class="text-sm text-slate-300 mb-3">Supervision sécurité</p>
              <div class="space-y-2">
                <button @click="testEndpoint('/advanced-ai/security/dashboard')" 
                        class="w-full px-3 py-2 bg-red-600 hover:bg-red-700 rounded text-sm transition-colors">
                  📊 Dashboard
                </button>
                <button @click="testEndpoint('/advanced-ai/security/alerts')" 
                        class="w-full px-3 py-2 bg-red-600 hover:bg-red-700 rounded text-sm transition-colors">
                  🚨 Alertes
                </button>
                <button @click="runHealthCheck" 
                        class="w-full px-3 py-2 bg-red-600 hover:bg-red-700 rounded text-sm transition-colors">
                  ❤️ Health Check
                </button>
                <button @click="scanVulnerabilities" 
                        class="w-full px-3 py-2 bg-red-600 hover:bg-red-700 rounded text-sm transition-colors">
                  🔍 CVE Scan
                </button>
              </div>
            </div>
            
            <!-- Portfolio Optimizer (4 endpoints) -->
            <div class="bg-slate-700 p-4 rounded-lg border border-green-500/30">
              <h4 class="text-lg font-semibold text-green-400 mb-2">📊 Portfolio</h4>
              <p class="text-sm text-slate-300 mb-3">Optimisation</p>
              <div class="space-y-2">
                <button @click="testEndpoint('/advanced-ai/portfolio/metrics')" 
                        class="w-full px-3 py-2 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors">
                  📊 Métriques
                </button>
                <button @click="testEndpoint('/advanced-ai/portfolio/rebalance')" 
                        class="w-full px-3 py-2 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors">
                  ⚖️ Rééquilibrage
                </button>
                <button @click="optimizePortfolio" 
                        class="w-full px-3 py-2 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors">
                  🎯 Optimiser
                </button>
                <button @click="getOptimizationSummary" 
                        class="w-full px-3 py-2 bg-green-600 hover:bg-green-700 rounded text-sm transition-colors">
                  📋 Résumé
                </button>
              </div>
            </div>
          </div>
          
          <!-- Résultats des tests API améliorés -->
          <div v-if="apiTestResult" class="mt-6 p-4 bg-slate-700 rounded-lg border border-slate-600">
            <div class="flex justify-between items-center mb-3">
              <h4 class="text-lg font-semibold text-brand-accent">🔍 Résultat Test API</h4>
              <div class="flex items-center space-x-2">
                <span :class="[
                  'px-2 py-1 rounded text-xs font-medium',
                  apiTestResult.status === 'success' ? 'bg-green-600 text-white' :
                  apiTestResult.status === 'error' ? 'bg-red-600 text-white' :
                  'bg-yellow-600 text-white'
                ]">
                  {{ apiTestResult.status.toUpperCase() }}
                </span>
                <span class="text-xs text-slate-400">{{ new Date(apiTestResult.timestamp).toLocaleTimeString() }}</span>
              </div>
            </div>
            
            <div class="mb-3">
              <span class="text-sm font-medium text-slate-300">Endpoint:</span>
              <span class="text-sm text-brand-accent ml-2">{{ apiTestResult.endpoint }}</span>
            </div>
            
            <pre class="text-sm text-slate-300 bg-slate-800 p-3 rounded overflow-auto max-h-64 border border-slate-600">{{ JSON.stringify(apiTestResult.data || apiTestResult.error, null, 2) }}</pre>
          </div>
        </div>
      </div>

      <!-- Section Paper Trading -->
      <div v-else-if="currentSection === 'paper_trading'" class="space-y-6">
        <!-- En-tête Paper Trading -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <div class="flex justify-between items-center mb-6">
            <div>
              <h3 class="text-2xl font-bold text-yellow-400">🧪 Paper Trading (Dry Run)</h3>
              <p class="text-slate-300 mt-2">Test des stratégies de trading sans risque financier</p>
            </div>
            <div class="flex space-x-3">
              <button @click="startPaperTrading" 
                      :disabled="tradingLoading"
                      class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 rounded-lg text-white font-medium transition-colors">
                {{ tradingLoading ? '⏳ En cours...' : '🚀 Démarrer Paper Trading' }}
              </button>
              <button @click="executeDemoTrades" 
                      :disabled="tradingLoading"
                      class="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 rounded-lg text-white font-medium transition-colors">
                {{ tradingLoading ? '⏳' : '💼 Demo Trades' }}
              </button>
              <button @click="resetPaperTrading" 
                      :disabled="tradingLoading"
                      class="px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 rounded-lg text-white font-medium transition-colors">
                {{ tradingLoading ? '⏳' : '🔄 Reset' }}
              </button>
            </div>
          </div>
          
          <!-- Status des brokers -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-slate-700 p-4 rounded-lg border border-blue-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Brokers Configurés</h4>
                  <p class="text-2xl font-bold text-blue-400">{{ tradingStatus.brokers_configured || 0 }}</p>
                </div>
                <div class="text-2xl">🔌</div>
              </div>
            </div>
            
            <div class="bg-slate-700 p-4 rounded-lg border border-green-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Brokers Connectés</h4>
                  <p class="text-2xl font-bold text-green-400">{{ tradingStatus.brokers_connected || 0 }}</p>
                </div>
                <div class="text-2xl">✅</div>
              </div>
            </div>
            
            <div class="bg-slate-700 p-4 rounded-lg border border-purple-500/30">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-slate-300">Portfolio Paper</h4>
                  <p class="text-2xl font-bold text-purple-400">{{ formatCurrency(tradingStatus.portfolio_value || 10000) }}</p>
                </div>
                <div class="text-2xl">💰</div>
              </div>
            </div>
          </div>
          
          <!-- Liste des brokers -->
          <div v-if="brokersList.length > 0" class="mb-6">
            <h4 class="text-lg font-semibold text-slate-200 mb-3">Brokers Actifs</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div v-for="broker in brokersList" :key="broker.name" 
                   class="bg-slate-700 p-3 rounded-lg border border-slate-600">
                <div class="flex justify-between items-center">
                  <div>
                    <h5 class="font-medium text-slate-200">{{ broker.name.charAt(0).toUpperCase() + broker.name.slice(1) }}</h5>
                    <p class="text-sm text-slate-400">{{ broker.mode }} mode</p>
                  </div>
                  <div class="text-right">
                    <div :class="[
                      'px-2 py-1 rounded text-xs font-medium',
                      broker.status === 'connected' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
                    ]">
                      {{ broker.status }}
                    </div>
                    <div class="text-sm text-slate-300 mt-1">{{ formatCurrency(broker.balance || 0) }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Configuration broker rapide -->
          <div class="bg-slate-700 p-4 rounded-lg border border-slate-600">
            <h4 class="text-lg font-semibold text-slate-200 mb-3">Configuration Broker Rapide</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">Type de Broker</label>
                <select v-model="newBroker.type" class="w-full p-2 bg-slate-800 border border-slate-600 rounded-lg text-slate-200">
                  <option value="alpaca">Alpaca (Actions/ETF)</option>
                  <option value="binance">Binance (Crypto)</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">API Key</label>
                <input v-model="newBroker.apiKey" type="password" placeholder="Votre clé API" 
                       class="w-full p-2 bg-slate-800 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500">
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">API Secret</label>
                <input v-model="newBroker.apiSecret" type="password" placeholder="Votre clé secrète" 
                       class="w-full p-2 bg-slate-800 border border-slate-600 rounded-lg text-slate-200 placeholder-slate-500">
              </div>
              <div class="flex items-end">
                <button @click="addBroker" :disabled="!canAddBroker || tradingLoading"
                        class="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 rounded-lg text-white font-medium transition-colors">
                  {{ tradingLoading ? '⏳ Ajout...' : '➕ Ajouter Broker' }}
                </button>
              </div>
            </div>
          </div>
          
          <!-- Résultats des operations -->
          <div v-if="tradingResult" class="mt-6 p-4 bg-slate-700 rounded-lg border border-slate-600">
            <div class="flex justify-between items-center mb-3">
              <h4 class="text-lg font-semibold text-yellow-400">📊 Résultat Opération</h4>
              <span :class="[
                'px-2 py-1 rounded text-xs font-medium',
                tradingResult.success ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
              ]">
                {{ tradingResult.success ? 'SUCCÈS' : 'ERREUR' }}
              </span>
            </div>
            <pre class="text-sm text-slate-300 bg-slate-800 p-3 rounded overflow-auto max-h-64 border border-slate-600">{{ JSON.stringify(tradingResult.data || tradingResult.error || tradingResult.message, null, 2) }}</pre>
          </div>
        </div>
        
        <!-- Market Data en temps réel -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-slate-100 mb-4">📊 Données de Marché Temps Réel</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div v-for="(data, symbol) in marketData" :key="symbol" 
                 class="bg-slate-700 p-4 rounded-lg border border-slate-600">
              <div class="flex justify-between items-center">
                <div>
                  <h4 class="font-medium text-slate-200">{{ symbol }}</h4>
                  <p class="text-2xl font-bold text-green-400">{{ formatCurrency(data.price || 0) }}</p>
                  <p class="text-sm text-slate-400">{{ data.broker || 'Auto' }}</p>
                </div>
                <div class="text-right">
                  <div class="text-sm text-slate-400">Bid: {{ formatCurrency(data.bid || 0) }}</div>
                  <div class="text-sm text-slate-400">Ask: {{ formatCurrency(data.ask || 0) }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Contrôles surveillance -->
          <div class="mt-4 flex justify-between items-center">
            <div class="flex space-x-2">
              <button @click="startMarketWatch" :disabled="isWatching"
                      class="px-3 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 rounded-lg text-white text-sm transition-colors">
                {{ isWatching ? '▶️ En cours...' : '▶️ Surveiller' }}
              </button>
              <button @click="stopMarketWatch" :disabled="!isWatching"
                      class="px-3 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 rounded-lg text-white text-sm transition-colors">
                ⏹️ Arrêter
              </button>
            </div>
            <div class="text-sm text-slate-400">
              Dernière MAJ: {{ lastUpdate ? new Date(lastUpdate).toLocaleTimeString() : 'Jamais' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Autres sections existantes -->
      <div v-else-if="currentSection === 'meme_coins'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-purple-400 mb-4">🪙 Meme Coins Trading</h3>
          <p class="text-slate-300">Module de trading haute fréquence sur tokens volatils...</p>
        </div>
      </div>

      <div v-else-if="currentSection === 'crypto_lt'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-orange-400 mb-4">₿ Crypto Long Terme</h3>
          <p class="text-slate-300">Stratégie DCA et holding long terme...</p>
        </div>
      </div>

      <div v-else-if="currentSection === 'forex'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-blue-400 mb-4">💱 Forex Trading</h3>
          <p class="text-slate-300">Trading algorithmique sur devises...</p>
        </div>
      </div>

      <div v-else-if="currentSection === 'etf'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-green-400 mb-4">📈 ETF Portfolio</h3>
          <p class="text-slate-300">Allocation portfolio diversifié...</p>
        </div>
      </div>

      <div v-else-if="currentSection === 'portfolio_global'">
        <!-- Portfolio Global détaillé -->
        <div class="space-y-6">
          <!-- Métriques principales du portfolio -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-semibold text-slate-300">Valeur Totale</h3>
                  <p class="text-3xl font-bold text-green-400">{{ formatCurrency(systemMetrics.totalValue) }}</p>
                  <p class="text-sm text-green-300">+{{ formatPercentage(systemMetrics.change) }} aujourd'hui</p>
                </div>
                <div class="text-3xl">💼</div>
              </div>
            </div>
            
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-semibold text-slate-300">Profits Réalisés</h3>
                  <p class="text-3xl font-bold text-blue-400">$2,847</p>
                  <p class="text-sm text-blue-300">Ce mois</p>
                </div>
                <div class="text-3xl">💰</div>
              </div>
            </div>
            
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-semibold text-slate-300">Diversification</h3>
                  <p class="text-3xl font-bold text-purple-400">87%</p>
                  <p class="text-sm text-purple-300">Score optimal</p>
                </div>
                <div class="text-3xl">🎯</div>
              </div>
            </div>
          </div>
          
          <!-- Allocation par stratégie -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <h3 class="text-xl font-semibold text-slate-100 mb-4">💼 Allocation par Stratégie</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div class="bg-slate-700 p-4 rounded-lg border border-purple-500/30">
                <div class="flex justify-between items-center mb-2">
                  <h4 class="font-medium text-purple-400">🪙 Meme Coins</h4>
                  <span class="text-sm text-slate-400">20%</span>
                </div>
                <div class="text-2xl font-bold text-slate-200">$5,068</div>
                <div class="text-sm text-purple-300">+15.2% cette semaine</div>
              </div>
              
              <div class="bg-slate-700 p-4 rounded-lg border border-orange-500/30">
                <div class="flex justify-between items-center mb-2">
                  <h4 class="font-medium text-orange-400">₿ Crypto LT</h4>
                  <span class="text-sm text-slate-400">40%</span>
                </div>
                <div class="text-2xl font-bold text-slate-200">$10,136</div>
                <div class="text-sm text-orange-300">+8.7% ce mois</div>
              </div>
              
              <div class="bg-slate-700 p-4 rounded-lg border border-blue-500/30">
                <div class="flex justify-between items-center mb-2">
                  <h4 class="font-medium text-blue-400">💱 Forex</h4>
                  <span class="text-sm text-slate-400">25%</span>
                </div>
                <div class="text-2xl font-bold text-slate-200">$6,335</div>
                <div class="text-sm text-blue-300">+3.1% ce mois</div>
              </div>
              
              <div class="bg-slate-700 p-4 rounded-lg border border-green-500/30">
                <div class="flex justify-between items-center mb-2">
                  <h4 class="font-medium text-green-400">📈 ETF</h4>
                  <span class="text-sm text-slate-400">15%</span>
                </div>
                <div class="text-2xl font-bold text-slate-200">$3,801</div>
                <div class="text-sm text-green-300">+5.4% ce mois</div>
              </div>
            </div>
          </div>
          
          <!-- Positions principales -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <h3 class="text-xl font-semibold text-slate-100 mb-4">📊 Top Positions</h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center p-3 bg-slate-700 rounded-lg">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm">₿</div>
                  <div>
                    <div class="font-medium text-slate-200">Bitcoin (BTC)</div>
                    <div class="text-sm text-slate-400">0.1523 BTC</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">$6,847</div>
                  <div class="text-sm text-green-300">+12.3%</div>
                </div>
              </div>
              
              <div class="flex justify-between items-center p-3 bg-slate-700 rounded-lg">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm">E</div>
                  <div>
                    <div class="font-medium text-slate-200">Ethereum (ETH)</div>
                    <div class="text-sm text-slate-400">1.247 ETH</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">$3,289</div>
                  <div class="text-sm text-green-300">+8.1%</div>
                </div>
              </div>
              
              <div class="flex justify-between items-center p-3 bg-slate-700 rounded-lg">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white font-bold text-sm">S</div>
                  <div>
                    <div class="font-medium text-slate-200">SPY ETF</div>
                    <div class="text-sm text-slate-400">8 parts</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">$3,801</div>
                  <div class="text-sm text-green-300">+5.4%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="currentSection === 'analytics'">
        <!-- Analytics détaillées -->
        <div class="space-y-6">
          <!-- Métriques de performance -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-medium text-slate-400">Sharpe Ratio</h3>
                  <p class="text-2xl font-bold text-green-400">2.34</p>
                  <p class="text-xs text-green-300">Excellent</p>
                </div>
                <div class="text-2xl">📊</div>
              </div>
            </div>
            
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-medium text-slate-400">Max Drawdown</h3>
                  <p class="text-2xl font-bold text-yellow-400">-8.2%</p>
                  <p class="text-xs text-yellow-300">Contrôlé</p>
                </div>
                <div class="text-2xl">📉</div>
              </div>
            </div>
            
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-medium text-slate-400">Win Rate</h3>
                  <p class="text-2xl font-bold text-purple-400">73%</p>
                  <p class="text-xs text-purple-300">Élevé</p>
                </div>
                <div class="text-2xl">🎯</div>
              </div>
            </div>
            
            <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-sm font-medium text-slate-400">Alpha</h3>
                  <p class="text-2xl font-bold text-cyan-400">0.18</p>
                  <p class="text-xs text-cyan-300">Surperformance</p>
                </div>
                <div class="text-2xl">🚀</div>
              </div>
            </div>
          </div>
          
          <!-- Performance par période -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <h3 class="text-xl font-semibold text-slate-100 mb-4">📈 Performance par Période</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-slate-700 p-4 rounded-lg">
                <div class="text-center">
                  <h4 class="text-sm font-medium text-slate-400 mb-2">7 Jours</h4>
                  <div class="text-2xl font-bold text-green-400">+5.2%</div>
                  <div class="text-sm text-green-300 mt-1">vs S&P500: +2.1%</div>
                </div>
              </div>
              
              <div class="bg-slate-700 p-4 rounded-lg">
                <div class="text-center">
                  <h4 class="text-sm font-medium text-slate-400 mb-2">30 Jours</h4>
                  <div class="text-2xl font-bold text-green-400">+12.8%</div>
                  <div class="text-sm text-green-300 mt-1">vs S&P500: +4.3%</div>
                </div>
              </div>
              
              <div class="bg-slate-700 p-4 rounded-lg">
                <div class="text-center">
                  <h4 class="text-sm font-medium text-slate-400 mb-2">YTD</h4>
                  <div class="text-2xl font-bold text-green-400">+28.5%</div>
                  <div class="text-sm text-green-300 mt-1">vs S&P500: +11.2%</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Analyse des stratégies -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <h3 class="text-xl font-semibold text-slate-100 mb-4">🔍 Performance par Stratégie</h3>
            <div class="space-y-4">
              <div class="flex justify-between items-center p-4 bg-slate-700 rounded-lg border border-purple-500/30">
                <div class="flex items-center space-x-3">
                  <div class="w-3 h-3 bg-purple-500 rounded-full"></div>
                  <div>
                    <div class="font-medium text-purple-400">Meme Coins (Scalping)</div>
                    <div class="text-sm text-slate-400">145 trades cette semaine</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">+15.2%</div>
                  <div class="text-sm text-purple-300">Win Rate: 68%</div>
                </div>
              </div>
              
              <div class="flex justify-between items-center p-4 bg-slate-700 rounded-lg border border-orange-500/30">
                <div class="flex items-center space-x-3">
                  <div class="w-3 h-3 bg-orange-500 rounded-full"></div>
                  <div>
                    <div class="font-medium text-orange-400">Crypto Long Terme (DCA)</div>
                    <div class="text-sm text-slate-400">12 achats automatiques</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">+8.7%</div>
                  <div class="text-sm text-orange-300">Win Rate: 91%</div>
                </div>
              </div>
              
              <div class="flex justify-between items-center p-4 bg-slate-700 rounded-lg border border-blue-500/30">
                <div class="flex items-center space-x-3">
                  <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <div>
                    <div class="font-medium text-blue-400">Forex (Grid Trading)</div>
                    <div class="text-sm text-slate-400">89 trades ce mois</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">+3.1%</div>
                  <div class="text-sm text-blue-300">Win Rate: 77%</div>
                </div>
              </div>
              
              <div class="flex justify-between items-center p-4 bg-slate-700 rounded-lg border border-green-500/30">
                <div class="flex items-center space-x-3">
                  <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                  <div>
                    <div class="font-medium text-green-400">ETF (Allocation)</div>
                    <div class="text-sm text-slate-400">3 rééquilibrages</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-400">+5.4%</div>
                  <div class="text-sm text-green-300">Win Rate: 100%</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Graphique placeholder -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
            <h3 class="text-xl font-semibold text-slate-100 mb-4">📊 Évolution Performance (YTD)</h3>
            <div class="h-64 bg-slate-700 rounded-lg flex items-center justify-center">
              <p class="text-slate-400">Graphique de performance avancé - À intégrer avec Chart.js</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="currentSection === 'historique'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-amber-400 mb-4">📜 Historique</h3>
          <p class="text-slate-300">Historique des transactions et des événements...</p>
        </div>
      </div>

      <div v-else-if="currentSection === 'health'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-red-400 mb-4">❤️ Health Monitor</h3>
          <p class="text-slate-300">Monitoring système et performances...</p>
        </div>
      </div>

      <div v-else-if="currentSection === 'settings'">
        <div class="bg-slate-800 p-6 rounded-xl shadow-lg">
          <h3 class="text-xl font-semibold text-slate-400 mb-4">⚙️ Configuration</h3>
          <p class="text-slate-300">Configuration des paramètres IA...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import aiService from '../services/aiService.js'
import tradingService from '../services/tradingService.js'

// Variables réactives
const currentSection = ref('overview')
const orchestratorRunning = ref(false)
const orchestratorStats = ref({
  success_rate: 94.2
})
const apiTestResult = ref(null)

// Données des modules IA
const modulesData = ref({
  feedback: null,
  predictive: null,
  security: null,
  portfolio: null
})

const systemMetrics = ref({
  totalValue: 25340,
  change: 12.5,
  activeTrades: 12,
  aiScore: 94.2,
  securityScore: 98
})

const loading = ref(false)
const error = ref(null)

// Variables pour le Paper Trading
const tradingLoading = ref(false)
const tradingResult = ref(null)
const tradingStatus = ref({
  brokers_configured: 0,
  brokers_connected: 0,
  portfolio_value: 10000
})
const brokersList = ref([])
const newBroker = ref({
  type: 'alpaca',
  apiKey: '',
  apiSecret: ''
})
const marketData = ref({})
const isWatching = ref(false)
const lastUpdate = ref(null)
let marketWatchInterval = null

// Lifecycle
onMounted(async () => {
  await loadModulesData()
  await loadTradingStatus()  // Charger aussi le statut trading
  
  // Actualisation périodique toutes les 30 secondes
  const interval = setInterval(async () => {
    await loadModulesData()
    if (currentSection.value === 'paper_trading') {
      await loadTradingStatus()
    }
  }, 30000)
  
  onUnmounted(() => {
    clearInterval(interval)
    stopMarketWatch()  // Arrêter la surveillance si active
  })
})

// Methods
const getSectionTitle = () => {
  const titles = {
    overview: 'Dashboard Multi-Assets',
    ai_modules: 'Modules IA Avancée',
    paper_trading: 'Paper Trading',
    meme_coins: 'Meme Coins Trading',
    crypto_lt: 'Crypto Long Terme', 
    forex: 'Forex Trading',
    etf: 'ETF Portfolio',
    portfolio_global: 'Portfolio Global',
    analytics: 'Analytics',
    historique: 'Historique',
    health: 'Health Monitor',
    settings: 'Configuration'
  }
  return titles[currentSection.value] || 'Dashboard'
}

const getSectionSubtitle = () => {
  const subtitles = {
    overview: 'Supervision intelligente de tous vos workflows de trading',
    ai_modules: 'Interface de contrôle des 16 endpoints IA avancée',
    paper_trading: 'Test des stratégies sans risque financier (dry run)',
    meme_coins: 'Trading haute fréquence sur tokens volatils',
    crypto_lt: 'Stratégie DCA et holding long terme',
    forex: 'Trading algorithmique sur devises',
    etf: 'Allocation portfolio diversifié',
    portfolio_global: 'Portfolio global de l\'investisseur',
    analytics: 'Analyse des performances et des tendances',
    historique: 'Historique des transactions et des événements',
    health: 'Monitoring système et performances',
    settings: 'Configuration des paramètres IA'
  }
  return subtitles[currentSection.value] || ''
}

const toggleOrchestrator = () => {
  orchestratorRunning.value = !orchestratorRunning.value
}

// Chargement des données des modules IA
const loadModulesData = async () => {
  if (loading.value) return
  
  loading.value = true
  error.value = null
  
  try {
    console.log('🔄 Chargement des données des modules IA...')
    
    // Charger toutes les données en parallèle
    const [
      feedbackPatterns,
      marketRegime,
      securityDashboard,
      portfolioMetrics,
      systemStatus
    ] = await Promise.allSettled([
      aiService.getFeedbackPatterns(),
      aiService.getMarketRegime(),
      aiService.getSecurityDashboard(),
      aiService.getPortfolioMetrics(),
      aiService.getCompleteSystemStatus()
    ])
    
    // Traitement des résultats
    modulesData.value = {
      feedback: feedbackPatterns.status === 'fulfilled' ? feedbackPatterns.value : null,
      predictive: marketRegime.status === 'fulfilled' ? marketRegime.value : null,
      security: securityDashboard.status === 'fulfilled' ? securityDashboard.value : null,
      portfolio: portfolioMetrics.status === 'fulfilled' ? portfolioMetrics.value : null,
      system: systemStatus.status === 'fulfilled' ? systemStatus.value : null
    }
    
    // Mise à jour des métriques système
    updateSystemMetrics()
    
    console.log('✅ Données des modules IA chargées:', modulesData.value)
    
  } catch (err) {
    console.error('❌ Erreur lors du chargement des modules:', err)
    error.value = err.message
  } finally {
    loading.value = false
  }
}

// Mise à jour des métriques système basées sur les données réelles
const updateSystemMetrics = () => {
  const { security, portfolio, feedback, system } = modulesData.value
  
  // Score de sécurité
  if (security?.security_score) {
    systemMetrics.value.securityScore = security.security_score
  }
  
  // Score IA basé sur le feedback loop
  if (feedback?.total_patterns || system?.modules_status) {
    const feedbackScore = feedback?.adaptation_score || 90
    const systemScore = system?.overall_health_score || 95
    systemMetrics.value.aiScore = Math.round((feedbackScore + systemScore) / 2)
  }
  
  // Métriques portfolio
  if (portfolio?.portfolio_value) {
    systemMetrics.value.totalValue = portfolio.portfolio_value
  }
  
  if (portfolio?.daily_return) {
    systemMetrics.value.change = portfolio.daily_return * 100
  }
  
  // Nombre de trades actifs (simulé)
  if (system?.active_tasks) {
    systemMetrics.value.activeTrades = system.active_tasks.length || 12
  }
}

// Test des endpoints IA
const testEndpoint = async (endpoint) => {
  try {
    console.log(`🧪 Test de l'endpoint: ${endpoint}`)
    loading.value = true
    
    let result
    switch (endpoint) {
      case '/advanced-ai/feedback/patterns':
        result = await aiService.getFeedbackPatterns()
        break
      case '/advanced-ai/feedback/adaptations':
        result = await aiService.getFeedbackAdaptations()
        break
      case '/advanced-ai/prediction/regime':
        result = await aiService.getMarketRegime()
        break
      case '/advanced-ai/prediction/alerts':
        result = await aiService.getPredictiveAlerts()
        break
      case '/advanced-ai/security/dashboard':
        result = await aiService.getSecurityDashboard()
        break
      case '/advanced-ai/security/alerts':
        result = await aiService.getSecurityAlerts()
        break
      case '/advanced-ai/portfolio/metrics':
        result = await aiService.getPortfolioMetrics()
        break
      case '/advanced-ai/portfolio/rebalance':
        result = await aiService.getRebalanceRecommendations()
        break
      default:
        result = { error: 'Endpoint non reconnu' }
    }
    
    apiTestResult.value = {
      endpoint,
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Test réussi:', result)
    
  } catch (error) {
    console.error('❌ Test échoué:', error)
    apiTestResult.value = {
      endpoint,
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

// Test de tous les modules
const testAllModules = async () => {
  try {
    loading.value = true
    console.log('🚀 Test de tous les modules IA...')
    
    const results = await aiService.testAllModules()
    
    apiTestResult.value = {
      endpoint: 'ALL_MODULES',
      timestamp: new Date().toISOString(),
      status: 'complete',
      data: results
    }
    
    console.log('✅ Test complet terminé:', results)
    
  } catch (error) {
    console.error('❌ Test complet échoué:', error)
    apiTestResult.value = {
      endpoint: 'ALL_MODULES',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

// Formatage des données
const formatNumber = (value) => {
  if (typeof value !== 'number') return value
  return new Intl.NumberFormat('fr-FR').format(value)
}

const formatCurrency = (value) => {
  if (typeof value !== 'number') return value
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'USD'
  }).format(value)
}

const formatPercentage = (value) => {
  if (typeof value !== 'number') return value
  return `${value > 0 ? '+' : ''}${value.toFixed(2)}%`
}

// Statut des modules
const getModuleStatus = (moduleData) => {
  if (!moduleData) return { status: 'unknown', color: 'text-gray-400' }
  
  if (moduleData.status === 'success' || moduleData.health_score > 90) {
    return { status: 'healthy', color: 'text-green-400' }
  } else if (moduleData.health_score > 70) {
    return { status: 'warning', color: 'text-yellow-400' }
  } else {
    return { status: 'error', color: 'text-red-400' }
  }
}

// Méthodes spécifiques pour les modules IA
const submitLearningSignal = async () => {
  try {
    loading.value = true
    console.log('📤 Soumission d\'un signal d\'apprentissage...')
    
    const signalData = {
      signal_type: 'SUCCESS',
      component: 'demo_test',
      context: {
        market_conditions: { volatility: 'medium', trend: 'bull' },
        system_state: { performance: 'good', load: 'normal' }
      },
      performance_metrics: {
        accuracy: 0.95,
        response_time: 150,
        success_rate: 0.88
      }
    }
    
    const result = await aiService.submitLearningSignal(signalData)
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/feedback/learn',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Signal soumis avec succès:', result)
    
  } catch (error) {
    console.error('❌ Erreur soumission signal:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/feedback/learn',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const analyzePerformance = async () => {
  try {
    loading.value = true
    console.log('📊 Analyse des performances...')
    
    const performanceData = {
      trading_metrics: {
        total_trades: 150,
        successful_trades: 132,
        avg_return: 0.025,
        max_drawdown: 0.08
      },
      system_metrics: {
        response_time: 120,
        uptime: 0.999,
        error_rate: 0.002
      },
      timeframe: '7d'
    }
    
    const result = await aiService.analyzePerformance(performanceData)
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/feedback/analyze-performance',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Analyse terminée:', result)
    
  } catch (error) {
    console.error('❌ Erreur analyse performance:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/feedback/analyze-performance',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const generatePrediction = async () => {
  try {
    loading.value = true
    console.log('🔮 Génération de prédiction...')
    
    const predictionData = {
      asset_type: 'crypto',
      horizon: '1hour',
      market_data: {
        price: 45000,
        volume: 1200000,
        volatility: 0.15
      }
    }
    
    const result = await aiService.generatePrediction(predictionData)
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/prediction/forecast',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Prédiction générée:', result)
    
  } catch (error) {
    console.error('❌ Erreur génération prédiction:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/prediction/forecast',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const getHistoricalAnalysis = async () => {
  try {
    loading.value = true
    console.log('📊 Récupération analyse historique...')
    
    const result = await aiService.getHistoricalAnalysis('crypto')
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/prediction/analysis/crypto',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Analyse historique récupérée:', result)
    
  } catch (error) {
    console.error('❌ Erreur analyse historique:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/prediction/analysis/crypto',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const runHealthCheck = async () => {
  try {
    loading.value = true
    console.log('❤️ Lancement health check...')
    
    const result = await aiService.runHealthCheck()
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/security/health-check',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Health check terminé:', result)
    
  } catch (error) {
    console.error('❌ Erreur health check:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/security/health-check',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const scanVulnerabilities = async () => {
  try {
    loading.value = true
    console.log('🔍 Lancement scan CVE...')
    
    const scanOptions = {
      scan_type: 'comprehensive',
      deep_scan: false
    }
    
    const result = await aiService.scanVulnerabilities(scanOptions)
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/security/cve-scan',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Scan CVE terminé:', result)
    
  } catch (error) {
    console.error('❌ Erreur scan CVE:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/security/cve-scan',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const optimizePortfolio = async () => {
  try {
    loading.value = true
    console.log('🎯 Optimisation portfolio...')
    
    const optimizationData = {
      strategy: 'balanced',
      risk_level: 'medium',
      market_conditions: {
        regime: 'bull',
        volatility: 'medium'
      }
    }
    
    const result = await aiService.optimizePortfolio(optimizationData)
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/portfolio/optimize',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Portfolio optimisé:', result)
    
  } catch (error) {
    console.error('❌ Erreur optimisation portfolio:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/portfolio/optimize',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

const getOptimizationSummary = async () => {
  try {
    loading.value = true
    console.log('📋 Récupération résumé optimisation...')
    
    const result = await aiService.getOptimizationSummary()
    
    apiTestResult.value = {
      endpoint: '/advanced-ai/portfolio/summary',
      timestamp: new Date().toISOString(),
      status: 'success',
      data: result
    }
    
    console.log('✅ Résumé récupéré:', result)
    
  } catch (error) {
    console.error('❌ Erreur résumé optimisation:', error)
    apiTestResult.value = {
      endpoint: '/advanced-ai/portfolio/summary',
      timestamp: new Date().toISOString(),
      status: 'error',
      error: error.message
    }
  } finally {
    loading.value = false
  }
}

// ================================================================================
// PAPER TRADING METHODS
// ================================================================================

// Charger le statut du trading
const loadTradingStatus = async () => {
  try {
    const [status, brokers] = await Promise.all([
      tradingService.testConnectivity(),
      tradingService.listBrokers()
    ])
    
    tradingStatus.value = status
    brokersList.value = brokers.brokers || []
    
    console.log('✅ Statut trading chargé:', { status, brokers })
    
  } catch (error) {
    console.error('❌ Erreur chargement statut trading:', error)
    tradingStatus.value = {
      brokers_configured: 0,
      brokers_connected: 0,
      portfolio_value: 10000,
      connectivity: 'error'
    }
  }
}

// Démarrer le paper trading
const startPaperTrading = async () => {
  try {
    tradingLoading.value = true
    tradingResult.value = null
    
    console.log('🚀 Démarrage du paper trading...')
    const result = await tradingService.startPaperTrading()
    
    tradingResult.value = { success: true, data: result }
    await loadTradingStatus()
    
    console.log('✅ Paper trading démarré:', result)
    
  } catch (error) {
    console.error('❌ Erreur démarrage paper trading:', error)
    tradingResult.value = { success: false, error: error.message }
  } finally {
    tradingLoading.value = false
  }
}

// Exécuter des trades de démonstration
const executeDemoTrades = async () => {
  try {
    tradingLoading.value = true
    tradingResult.value = null
    
    console.log('💼 Exécution des trades de démonstration...')
    const result = await tradingService.executeDemoTrades()
    
    tradingResult.value = { success: true, data: result }
    await loadTradingStatus()
    
    console.log('✅ Trades de démo exécutés:', result)
    
  } catch (error) {
    console.error('❌ Erreur trades de démo:', error)
    tradingResult.value = { success: false, error: error.message }
  } finally {
    tradingLoading.value = false
  }
}

// Reset du paper trading
const resetPaperTrading = async () => {
  try {
    tradingLoading.value = true
    tradingResult.value = null
    
    console.log('🔄 Reset du paper trading...')
    const result = await tradingService.resetPaperTrading()
    
    tradingResult.value = { success: true, data: result }
    await loadTradingStatus()
    
    console.log('✅ Paper trading reset:', result)
    
  } catch (error) {
    console.error('❌ Erreur reset paper trading:', error)
    tradingResult.value = { success: false, error: error.message }
  } finally {
    tradingLoading.value = false
  }
}

// Ajouter un broker
const addBroker = async () => {
  try {
    if (!canAddBroker.value) return
    
    tradingLoading.value = true
    tradingResult.value = null
    
    console.log('🔌 Ajout du broker:', newBroker.value.type)
    
    const result = await tradingService.addBroker({
      broker_type: newBroker.value.type,
      api_key: newBroker.value.apiKey,
      api_secret: newBroker.value.apiSecret,
      mode: 'paper'
    })
    
    tradingResult.value = { success: true, data: result }
    
    // Reset du formulaire
    newBroker.value = {
      type: 'alpaca',
      apiKey: '',
      apiSecret: ''
    }
    
    await loadTradingStatus()
    
    console.log('✅ Broker ajouté:', result)
    
  } catch (error) {
    console.error('❌ Erreur ajout broker:', error)
    tradingResult.value = { success: false, error: error.message }
  } finally {
    tradingLoading.value = false
  }
}

// Démarrer la surveillance des prix
const startMarketWatch = async () => {
  try {
    isWatching.value = true
    const symbols = ['AAPL', 'TSLA', 'BTCUSDT', 'ETHUSDT']
    
    marketWatchInterval = await tradingService.watchPrices(symbols, (data) => {
      marketData.value = data
      lastUpdate.value = new Date().toISOString()
    }, 5000)
    
    console.log('👁️ Surveillance des prix démarrée')
    
  } catch (error) {
    console.error('❌ Erreur surveillance des prix:', error)
    isWatching.value = false
  }
}

// Arrêter la surveillance des prix
const stopMarketWatch = () => {
  if (marketWatchInterval) {
    tradingService.stopWatching(marketWatchInterval)
    marketWatchInterval = null
  }
  isWatching.value = false
  console.log('⏹️ Surveillance des prix arrêtée')
}

// Computed properties
const canAddBroker = computed(() => {
  return newBroker.value.apiKey.length > 0 && newBroker.value.apiSecret.length > 0
})

// CSS variables
const brandAccent = 'rgb(56, 189, 248)' // sky-400
</script>

<style scoped>
:root {
  --brand-accent: rgb(56, 189, 248);
}

.text-brand-accent {
  color: var(--brand-accent);
}

.bg-brand-accent {
  background-color: var(--brand-accent);
}

.border-brand-accent {
  border-color: var(--brand-accent);
}
</style> 