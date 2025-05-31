<template>
  <div class="bg-slate-900 text-slate-100 flex min-h-screen font-sans">
    <!-- Sidebar -->
    <aside class="w-64 bg-slate-800 p-6 space-y-8 flex flex-col shadow-2xl">
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-brand-accent flex items-center">
          <SparklesIcon class="w-10 h-10 mr-3" />
          AI Trade<span class="text-slate-400">Bot</span>
        </h1>
        <p class="text-slate-400 text-sm mt-2 ml-13">Système de trading autonome</p>
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
        
        <a href="#" @click="currentSection = 'health'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'health' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" :class="currentSection === 'health' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
          </svg>
          <span>❤️ Health Monitor</span>
        </a>
        
        <a href="#" @click="currentSection = 'settings'"
           :class="['flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors group',
                   currentSection === 'settings' ? 'bg-slate-700 text-brand-accent' : 'text-slate-300 hover:bg-slate-700 hover:text-brand-accent']">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5" :class="currentSection === 'settings' ? 'text-brand-accent' : 'text-slate-400 group-hover:text-brand-accent'">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 1.255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.759 6.759 0 010-1.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>⚙️ Settings</span>
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
          <!-- Bouton Refresh avec effet halo -->
          <button @click="refreshData" 
                  class="p-3 rounded-full hover:bg-slate-700 transition-all duration-300 ring-2 ring-slate-600 hover:ring-4 hover:ring-sky-400/50 shadow-lg hover:shadow-sky-400/30 group">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-slate-400 group-hover:text-sky-400 transition-colors duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
          
          <!-- Bouton Orchestrateur avec effet aurore professionnel -->
          <div class="relative">
            <button @click="toggleOrchestrator" 
                    :class="['px-6 py-3 rounded-lg font-bold transition-all duration-300 text-lg shadow-xl relative overflow-hidden group',
                            orchestratorRunning 
                              ? 'bg-red-600 hover:bg-red-700 text-white ring-4 ring-red-300/50 hover:ring-red-300 hover:shadow-red-400/50' 
                              : 'bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 text-white ring-4 ring-sky-300/50 hover:ring-sky-300 hover:shadow-sky-400/50']">
              <!-- Effet glow en arrière-plan -->
              <div :class="['absolute inset-0 rounded-lg blur-xl opacity-30 group-hover:opacity-50 transition-opacity duration-300',
                           orchestratorRunning ? 'bg-red-400' : 'bg-sky-400']"></div>
              <span class="relative z-10">{{ orchestratorRunning ? 'ARRÊTER' : 'DÉMARRER' }}</span>
          </button>
          </div>
          
          <!-- Avatar IA avec logo neuronal AGRANDI -->
          <div class="relative w-14 h-14 rounded-full border-2 border-brand-accent bg-gradient-to-br from-brand-accent to-blue-500 
                      flex items-center justify-center text-white font-bold shadow-xl
                      hover:shadow-brand-accent/50 transition-all duration-300 cursor-pointer group">
            <span class="text-lg font-extrabold">AI</span>
            <!-- Effet réseau neuronal -->
            <div class="absolute inset-0 rounded-full border-2 border-brand-accent/30 scale-110 opacity-0 
                        group-hover:opacity-100 group-hover:scale-125 transition-all duration-500"></div>
            <!-- Effet de pulsation pour montrer l'activité -->
            <div class="absolute inset-0 rounded-full border border-brand-accent/20 animate-ping scale-105"></div>
          </div>
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

      <!-- Health Monitor Section -->
      <div v-if="currentSection === 'health'" class="space-y-8">
        <!-- System Status Overview -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <!-- CPU Usage -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-medium text-slate-400 uppercase tracking-wide">CPU Usage</h3>
              <div :class="['w-3 h-3 rounded-full', getHealthColor(systemHealth.cpu_usage)]"></div>
            </div>
            <div class="relative">
              <div class="text-3xl font-bold text-slate-100">{{ systemHealth.cpu_usage || 0 }}%</div>
              <div class="w-full bg-slate-700 rounded-full h-2 mt-4">
                <div :class="['h-2 rounded-full transition-all duration-1000', getCpuBarColor(systemHealth.cpu_usage)]" 
                     :style="{ width: (systemHealth.cpu_usage || 0) + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- Memory Usage -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-medium text-slate-400 uppercase tracking-wide">Memory</h3>
              <div :class="['w-3 h-3 rounded-full', getHealthColor(systemHealth.memory_usage)]"></div>
            </div>
            <div class="relative">
              <div class="text-3xl font-bold text-slate-100">{{ systemHealth.memory_usage || 0 }}%</div>
              <div class="w-full bg-slate-700 rounded-full h-2 mt-4">
                <div :class="['h-2 rounded-full transition-all duration-1000', getMemoryBarColor(systemHealth.memory_usage)]" 
                     :style="{ width: (systemHealth.memory_usage || 0) + '%' }"></div>
              </div>
            </div>
          </div>

          <!-- Network Status -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-medium text-slate-400 uppercase tracking-wide">Network</h3>
              <div :class="['w-3 h-3 rounded-full', systemHealth.network_ok ? 'bg-green-500 shadow-green-500/50' : 'bg-red-500 shadow-red-500/50']"></div>
            </div>
            <div class="relative">
              <div class="text-2xl font-bold text-slate-100">{{ systemHealth.network_latency || 0 }}ms</div>
              <div class="text-sm text-slate-400 mt-2">{{ systemHealth.network_ok ? '🌐 Connected' : '⚠️ Issues' }}</div>
            </div>
          </div>

          <!-- Security Score -->
          <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-medium text-slate-400 uppercase tracking-wide">Security</h3>
              <div :class="['w-3 h-3 rounded-full', getSecurityColor(systemHealth.security_score)]"></div>
            </div>
            <div class="relative">
              <div class="text-3xl font-bold text-slate-100">{{ systemHealth.security_score || 0 }}/100</div>
              <div class="w-full bg-slate-700 rounded-full h-2 mt-4">
                <div :class="['h-2 rounded-full transition-all duration-1000', getSecurityBarColor(systemHealth.security_score)]" 
                     :style="{ width: (systemHealth.security_score || 0) + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI Services Status -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-6 flex items-center">
            <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            AI Services Status
          </h3>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-4 gap-4">
            <!-- Predictive System -->
            <div class="bg-slate-700/50 p-4 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-slate-100">🔮 Predictive</h4>
                <div :class="['w-2 h-2 rounded-full', aiServices.predictive?.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400']"></div>
              </div>
              <div class="text-sm space-y-1">
                <div class="flex justify-between text-slate-300">
                  <span>Predictions:</span>
                  <span class="font-mono">{{ aiServices.predictive?.predictions_count || 0 }}</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Accuracy:</span>
                  <span class="font-mono text-green-400">{{ aiServices.predictive?.accuracy || 0 }}%</span>
                </div>
                <div class="text-xs text-slate-400">Last: {{ aiServices.predictive?.last_run || 'Never' }}</div>
              </div>
            </div>

            <!-- Portfolio Optimizer -->
            <div class="bg-slate-700/50 p-4 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-slate-100">📊 Portfolio</h4>
                <div :class="['w-2 h-2 rounded-full', aiServices.portfolio?.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400']"></div>
              </div>
              <div class="text-sm space-y-1">
                <div class="flex justify-between text-slate-300">
                  <span>Assets:</span>
                  <span class="font-mono">{{ aiServices.portfolio?.assets_count || 0 }}</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Rebalanced:</span>
                  <span class="font-mono text-blue-400">{{ aiServices.portfolio?.rebalances || 0 }}</span>
                </div>
                <div class="text-xs text-slate-400">Last: {{ aiServices.portfolio?.last_run || 'Never' }}</div>
              </div>
            </div>

            <!-- Security Supervisor -->
            <div class="bg-slate-700/50 p-4 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-slate-100">🛡️ Security</h4>
                <div :class="['w-2 h-2 rounded-full', aiServices.security?.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400']"></div>
              </div>
              <div class="text-sm space-y-1">
                <div class="flex justify-between text-slate-300">
                  <span>Threats:</span>
                  <span class="font-mono text-red-400">{{ aiServices.security?.threats_detected || 0 }}</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>CVE Scans:</span>
                  <span class="font-mono">{{ aiServices.security?.cve_scans || 0 }}</span>
                </div>
                <div class="text-xs text-slate-400">Last: {{ aiServices.security?.last_run || 'Never' }}</div>
              </div>
            </div>

            <!-- Feedback Loop -->
            <div class="bg-slate-700/50 p-4 rounded-lg">
              <div class="flex items-center justify-between mb-3">
                <h4 class="font-medium text-slate-100">🧠 Feedback</h4>
                <div :class="['w-2 h-2 rounded-full', aiServices.feedback?.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400']"></div>
              </div>
              <div class="text-sm space-y-1">
                <div class="flex justify-between text-slate-300">
                  <span>Signals:</span>
                  <span class="font-mono">{{ aiServices.feedback?.signals_processed || 0 }}</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Learning:</span>
                  <span class="font-mono text-purple-400">{{ aiServices.feedback?.learning_rate || 0 }}%</span>
                </div>
                <div class="text-xs text-slate-400">Last: {{ aiServices.feedback?.last_run || 'Never' }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Real-time Logs -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-semibold text-slate-100 flex items-center">
              <svg class="w-6 h-6 mr-3 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Live System Logs
            </h3>
            <button @click="clearLogs" 
                    class="px-3 py-1 text-xs bg-slate-700 hover:bg-slate-600 text-slate-300 rounded border border-slate-600">
              Clear
            </button>
          </div>
          
          <div class="bg-slate-900 rounded-lg p-4 h-64 overflow-y-auto font-mono text-sm">
            <div v-for="log in systemLogs.slice(-50)" :key="log.id" 
                 :class="['mb-1 flex items-start space-x-2', getLogColor(log.level)]">
              <span class="text-slate-500 text-xs shrink-0">{{ formatTime(log.timestamp) }}</span>
              <span :class="['px-1 text-xs rounded', getLogBadgeColor(log.level)]">{{ log.level }}</span>
              <span class="break-words">{{ log.message }}</span>
            </div>
            
            <!-- Empty state -->
            <div v-if="systemLogs.length === 0" class="text-center text-slate-500 py-8">
              <svg class="w-12 h-12 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <p>No logs available</p>
              <p class="text-xs">System activity will appear here</p>
            </div>
          </div>
        </div>

        <!-- Performance Metrics -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-6 flex items-center">
            <svg class="w-6 h-6 mr-3 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
            Performance Metrics
          </h3>
          
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- API Performance -->
            <div class="space-y-4">
              <h4 class="font-medium text-slate-300">API Performance</h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Response Time</span>
                  <span class="text-sm font-mono text-green-400">{{ performanceMetrics.api_response_time || 0 }}ms</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Requests/min</span>
                  <span class="text-sm font-mono text-blue-400">{{ performanceMetrics.requests_per_minute || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Error Rate</span>
                  <span class="text-sm font-mono text-red-400">{{ performanceMetrics.error_rate || 0 }}%</span>
                </div>
              </div>
            </div>

            <!-- Database Performance -->
            <div class="space-y-4">
              <h4 class="font-medium text-slate-300">Database</h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Query Time</span>
                  <span class="text-sm font-mono text-green-400">{{ performanceMetrics.db_query_time || 0 }}ms</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Connections</span>
                  <span class="text-sm font-mono text-blue-400">{{ performanceMetrics.db_connections || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Cache Hit Rate</span>
                  <span class="text-sm font-mono text-purple-400">{{ performanceMetrics.cache_hit_rate || 0 }}%</span>
                </div>
              </div>
            </div>

            <!-- Trading Performance -->
            <div class="space-y-4">
              <h4 class="font-medium text-slate-300">Trading</h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Signals/hour</span>
                  <span class="text-sm font-mono text-green-400">{{ performanceMetrics.signals_per_hour || 0 }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Success Rate</span>
                  <span class="text-sm font-mono text-blue-400">{{ performanceMetrics.success_rate || 0 }}%</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-slate-400">Execution Time</span>
                  <span class="text-sm font-mono text-purple-400">{{ performanceMetrics.execution_time || 0 }}ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Settings Section -->
      <div v-if="currentSection === 'settings'" class="space-y-8">
        <!-- Configuration du Bot IA -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-6 flex items-center">
            <Cog6ToothIcon class="w-6 h-6 mr-3 text-brand-accent" />
            Configuration du Bot IA
          </h3>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Mode Trading -->
            <div class="space-y-4">
              <h4 class="font-medium text-slate-100 mb-3">Mode de Trading</h4>
              
              <div class="space-y-3">
                <label class="flex items-center space-x-3 cursor-pointer">
                  <input type="radio" v-model="settings.tradingMode" value="demo" 
                         class="w-4 h-4 text-brand-accent border-slate-600 bg-slate-700 focus:ring-brand-accent">
                  <span class="text-slate-300">Mode Démo (Paper Trading)</span>
                  <span class="px-2 py-1 text-xs bg-green-500/20 text-green-400 rounded-full">SÉCURISÉ</span>
                </label>
                
                <label class="flex items-center space-x-3 cursor-pointer">
                  <input type="radio" v-model="settings.tradingMode" value="live" 
                         class="w-4 h-4 text-brand-accent border-slate-600 bg-slate-700 focus:ring-brand-accent">
                  <span class="text-slate-300">Mode Réel (Live Trading)</span>
                  <span class="px-2 py-1 text-xs bg-red-500/20 text-red-400 rounded-full">ARGENT RÉEL</span>
                </label>
              </div>
              
              <!-- Capital Initial -->
              <div class="mt-6">
                <label class="block text-sm font-medium text-slate-300 mb-2">Capital Initial</label>
                <div class="relative">
                  <span class="absolute left-3 top-3 text-slate-400">$</span>
                  <input v-model="settings.initialCapital" type="number" min="100" step="100"
                         class="w-full pl-8 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg 
                                text-slate-100 focus:ring-2 focus:ring-brand-accent focus:border-transparent">
                </div>
              </div>
              
              <!-- Niveau de Risque -->
              <div class="mt-6">
                <label class="block text-sm font-medium text-slate-300 mb-2">Niveau de Risque</label>
                <select v-model="settings.riskLevel" 
                        class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg 
                               text-slate-100 focus:ring-2 focus:ring-brand-accent focus:border-transparent">
                  <option value="conservative">Conservateur (Faible risque)</option>
                  <option value="moderate">Modéré (Risque équilibré)</option>
                  <option value="aggressive">Agressif (Risque élevé)</option>
                </select>
              </div>
            </div>
            
            <!-- Paramètres IA -->
            <div class="space-y-4">
              <h4 class="font-medium text-slate-100 mb-3">Intelligence Artificielle</h4>
              
              <!-- Fréquence d'analyse -->
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">Fréquence d'Analyse</label>
                <select v-model="settings.analysisFrequency" 
                        class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg 
                               text-slate-100 focus:ring-2 focus:ring-brand-accent focus:border-transparent">
                  <option value="1m">Chaque minute (Ultra réactif)</option>
                  <option value="5m">Toutes les 5 minutes (Réactif)</option>
                  <option value="15m">Toutes les 15 minutes (Standard)</option>
                  <option value="1h">Toutes les heures (Conservateur)</option>
                </select>
              </div>
              
              <!-- Seuil de confiance -->
              <div>
                <label class="block text-sm font-medium text-slate-300 mb-2">
                  Seuil de Confiance IA : {{ settings.confidenceThreshold }}%
                </label>
                <input v-model="settings.confidenceThreshold" type="range" min="50" max="95" step="5"
                       class="w-full h-2 bg-slate-600 rounded-lg appearance-none cursor-pointer slider">
                <div class="flex justify-between text-xs text-slate-400 mt-1">
                  <span>50% (Plus de signaux)</span>
                  <span>95% (Signaux très sûrs)</span>
                </div>
              </div>
              
              <!-- Auto-trading -->
              <div class="flex items-center justify-between p-4 bg-slate-700/50 rounded-lg">
                <div>
                  <h5 class="font-medium text-slate-100">Auto-Trading</h5>
                  <p class="text-sm text-slate-400">Exécution automatique des signaux IA</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="settings.autoTrading" type="checkbox" class="sr-only peer">
                  <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-accent/25 
                             rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white 
                             after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white 
                             after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-accent"></div>
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Notifications -->
        <div class="bg-slate-800 p-6 rounded-xl shadow-2xl">
          <h3 class="text-xl font-semibold text-slate-100 mb-6 flex items-center">
            <svg class="w-6 h-6 mr-3 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M15 17h5l-3.595-3.595a.56.56 0 0 1 0-.79L21 8H9l8 9z M9 8l3-5 3 5"/>
            </svg>
            Système de Notifications
          </h3>
          
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Telegram -->
            <div class="bg-slate-700/50 p-5 rounded-lg">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-medium text-slate-100 flex items-center">
                  <svg class="w-5 h-5 mr-2 text-blue-400" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0C5.374 0 0 5.373 0 12s5.374 12 12 12 12-5.373 12-12S18.626 0 12 0zm5.568 8.16c-.169 1.858-.896 6.728-.896 6.728-.296 1.588-.816 1.878-1.316 1.878-.56 0-.84-.42-.84-.924 0-.378.084-.756.252-1.092l.504-1.428c.084-.252.084-.42-.084-.588-.252-.252-.588-.168-.756.084l-.672 1.428c-.084.252-.252.378-.504.378s-.504-.126-.504-.378l.336-2.016c.084-.42.084-.756-.084-.924-.168-.168-.42-.084-.588.168l-.504 1.26c-.084.168-.252.252-.42.252-.252 0-.42-.168-.42-.42 0-.084.042-.168.084-.252l.672-1.596c.252-.588.756-.924 1.316-.924.504 0 .924.252 1.176.672l.336.756c.168.336.504.504.84.504.42 0 .756-.252.924-.588l.252-.588c.168-.42.588-.672 1.008-.672.588 0 1.092.42 1.092 1.008z"/>
                  </svg>
                  Telegram
                </h4>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="settings.notifications.telegram.enabled" type="checkbox" class="sr-only peer">
                  <div class="w-9 h-5 bg-slate-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-400/25 
                             rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white 
                             after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white 
                             after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-blue-400"></div>
                </label>
              </div>
              
              <div class="space-y-3">
                <div>
                  <label class="block text-xs text-slate-400 mb-1">Bot Token</label>
                  <input v-model="settings.notifications.telegram.botToken" type="password" placeholder="Votre bot token"
                         class="w-full px-3 py-2 text-sm bg-slate-600 border border-slate-500 rounded 
                                text-slate-100 focus:ring-1 focus:ring-blue-400 focus:border-transparent">
                </div>
                <div>
                  <label class="block text-xs text-slate-400 mb-1">Chat ID</label>
                  <input v-model="settings.notifications.telegram.chatId" type="text" placeholder="Votre chat ID"
                         class="w-full px-3 py-2 text-sm bg-slate-600 border border-slate-500 rounded 
                                text-slate-100 focus:ring-1 focus:ring-blue-400 focus:border-transparent">
                </div>
              </div>
            </div>
            
            <!-- Discord -->
            <div class="bg-slate-700/50 p-5 rounded-lg">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-medium text-slate-100 flex items-center">
                  <svg class="w-5 h-5 mr-2 text-purple-400" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.211.375-.445.865-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.042-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
                  </svg>
                  Discord
                </h4>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="settings.notifications.discord.enabled" type="checkbox" class="sr-only peer">
                  <div class="w-9 h-5 bg-slate-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-400/25 
                             rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white 
                             after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white 
                             after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-purple-400"></div>
                </label>
              </div>
              
              <div>
                <label class="block text-xs text-slate-400 mb-1">Webhook URL</label>
                <input v-model="settings.notifications.discord.webhookUrl" type="url" placeholder="Discord webhook URL"
                       class="w-full px-3 py-2 text-sm bg-slate-600 border border-slate-500 rounded 
                              text-slate-100 focus:ring-1 focus:ring-purple-400 focus:border-transparent">
              </div>
            </div>
            
            <!-- Email -->
            <div class="bg-slate-700/50 p-5 rounded-lg">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-medium text-slate-100 flex items-center">
                  <svg class="w-5 h-5 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                  </svg>
                  Email
                </h4>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input v-model="settings.notifications.email.enabled" type="checkbox" class="sr-only peer">
                  <div class="w-9 h-5 bg-slate-600 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-400/25 
                             rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white 
                             after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white 
                             after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-green-400"></div>
                </label>
              </div>
              
              <div class="space-y-3">
                <div>
                  <label class="block text-xs text-slate-400 mb-1">Adresse Email</label>
                  <input v-model="settings.notifications.email.address" type="email" placeholder="votre@email.com"
                         class="w-full px-3 py-2 text-sm bg-slate-600 border border-slate-500 rounded 
                                text-slate-100 focus:ring-1 focus:ring-green-400 focus:border-transparent">
                </div>
                <div>
                  <label class="block text-xs text-slate-400 mb-1">Fréquence Rapports</label>
                  <select v-model="settings.notifications.email.frequency" 
                          class="w-full px-3 py-2 text-sm bg-slate-600 border border-slate-500 rounded 
                                 text-slate-100 focus:ring-1 focus:ring-green-400 focus:border-transparent">
                    <option value="daily">Quotidien</option>
                    <option value="weekly">Hebdomadaire</option>
                    <option value="monthly">Mensuel</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions de Sauvegarde -->
        <div class="flex justify-end space-x-4">
          <button @click="resetSettings" 
                  class="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg 
                         transition-colors duration-200 border border-slate-600">
            Réinitialiser
          </button>
          <button @click="saveSettings" 
                  class="px-6 py-3 bg-gradient-to-r from-brand-accent to-blue-500 hover:from-brand-accent/90 hover:to-blue-500/90 
                         text-white font-medium rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg">
            Sauvegarder Configuration
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AssetDashboard from '../components/AssetDashboard.vue'
import WorkflowVisualizer from '../components/WorkflowVisualizer.vue'

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

// Nouvelles données pour Health et Settings
const systemHealth = ref({
  cpu_usage: 25,
  memory_usage: 45,
  network_ok: true,
  network_latency: 12,
  security_score: 87
})

const aiServices = ref({
  predictive: { status: 'healthy', predictions_count: 234, accuracy: 87, last_run: '2 min ago' },
  portfolio: { status: 'healthy', assets_count: 12, rebalances: 3, last_run: '5 min ago' },
  security: { status: 'healthy', threats_detected: 0, cve_scans: 45, last_run: '1 min ago' },
  feedback: { status: 'healthy', signals_processed: 1247, learning_rate: 94, last_run: '30 sec ago' }
})

const systemLogs = ref([
  { id: 1, timestamp: new Date(), level: 'INFO', message: '🚀 Orchestrator started successfully' },
  { id: 2, timestamp: new Date(Date.now() - 30000), level: 'SUCCESS', message: '✅ Predictive analysis completed - 5 new signals generated' },
  { id: 3, timestamp: new Date(Date.now() - 60000), level: 'WARNING', message: '⚠️ High volatility detected on DOGE/USDT - adjusting strategy' },
  { id: 4, timestamp: new Date(Date.now() - 90000), level: 'INFO', message: '📊 Portfolio rebalancing initiated for crypto_lt' }
])

const performanceMetrics = ref({
  api_response_time: 45,
  requests_per_minute: 127,
  error_rate: 0.2,
  db_query_time: 23,
  db_connections: 8,
  cache_hit_rate: 94,
  signals_per_hour: 23,
  success_rate: 87,
  execution_time: 156
})

const settings = ref({
  tradingMode: 'demo',
  initialCapital: 10000,
  riskLevel: 'moderate',
  analysisFrequency: '5m',
  confidenceThreshold: 75,
  autoTrading: false,
  notifications: {
    telegram: {
      enabled: false,
      botToken: '',
      chatId: ''
    },
    discord: {
      enabled: false,
      webhookUrl: ''
    },
    email: {
      enabled: false,
      address: '',
      frequency: 'daily'
    }
  }
})

// Méthodes
const getSectionTitle = () => {
  const titles = {
    overview: 'Dashboard Multi-Assets',
    meme_coins: '🪙 Meme Coins Station',
    crypto_lt: '₿ Crypto Long Terme Station',
    forex: '💱 Forex Trading Station',
    etf: '📈 ETF Investment Station',
    ai_insights: '🧠 AI Insights Hub',
    health: '❤️ Health Monitor',
    settings: '⚙️ Configuration'
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
    ai_insights: 'Analyses prédictives et recommandations de l\'orchestrateur',
    health: 'Monitoring système et services IA en temps réel',
    settings: 'Configuration complète du bot de trading autonome'
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

// Health Monitor Helper Methods
const getHealthColor = (value) => {
  if (value <= 50) return 'bg-green-500 shadow-green-500/50'
  if (value <= 80) return 'bg-yellow-500 shadow-yellow-500/50'
  return 'bg-red-500 shadow-red-500/50'
}

const getCpuBarColor = (value) => {
  if (value <= 50) return 'bg-gradient-to-r from-green-500 to-green-400'
  if (value <= 80) return 'bg-gradient-to-r from-yellow-500 to-yellow-400'
  return 'bg-gradient-to-r from-red-500 to-red-400'
}

const getMemoryBarColor = (value) => {
  if (value <= 60) return 'bg-gradient-to-r from-blue-500 to-blue-400'
  if (value <= 85) return 'bg-gradient-to-r from-yellow-500 to-yellow-400'
  return 'bg-gradient-to-r from-red-500 to-red-400'
}

const getSecurityColor = (score) => {
  if (score >= 80) return 'bg-green-500 shadow-green-500/50'
  if (score >= 60) return 'bg-yellow-500 shadow-yellow-500/50'
  return 'bg-red-500 shadow-red-500/50'
}

const getSecurityBarColor = (score) => {
  if (score >= 80) return 'bg-gradient-to-r from-green-500 to-green-400'
  if (score >= 60) return 'bg-gradient-to-r from-yellow-500 to-yellow-400'
  return 'bg-gradient-to-r from-red-500 to-red-400'
}

const getLogColor = (level) => {
  const colors = {
    INFO: 'text-blue-400',
    SUCCESS: 'text-green-400',
    WARNING: 'text-yellow-400',
    ERROR: 'text-red-400',
    CRITICAL: 'text-red-300'
  }
  return colors[level] || 'text-slate-400'
}

const getLogBadgeColor = (level) => {
  const colors = {
    INFO: 'bg-blue-500/20 text-blue-300',
    SUCCESS: 'bg-green-500/20 text-green-300',
    WARNING: 'bg-yellow-500/20 text-yellow-300',
    ERROR: 'bg-red-500/20 text-red-300',
    CRITICAL: 'bg-red-600/30 text-red-200'
  }
  return colors[level] || 'bg-slate-500/20 text-slate-300'
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const clearLogs = () => {
  systemLogs.value = []
}

// Settings Methods
const saveSettings = async () => {
  try {
    const response = await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(settings.value)
    })
    
    if (response.ok) {
      // Show success notification
      console.log('✅ Settings saved successfully')
    }
  } catch (error) {
    console.error('❌ Error saving settings:', error)
  }
}

const resetSettings = () => {
  settings.value = {
    tradingMode: 'demo',
    initialCapital: 10000,
    riskLevel: 'moderate',
    analysisFrequency: '5m',
    confidenceThreshold: 75,
    autoTrading: false,
    notifications: {
      telegram: { enabled: false, botToken: '', chatId: '' },
      discord: { enabled: false, webhookUrl: '' },
      email: { enabled: false, address: '', frequency: 'daily' }
    }
  }
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
    fetchAssetRecommendations(),
    fetchHealthData(),
    fetchSystemLogs()
  ])
}

// Health Monitoring Data Fetching
const fetchHealthData = async () => {
  try {
    // Simuler des données de santé système réalistes
    systemHealth.value = {
      cpu_usage: Math.floor(Math.random() * 40) + 20, // 20-60%
      memory_usage: Math.floor(Math.random() * 50) + 30, // 30-80%
      network_ok: Math.random() > 0.1, // 90% uptime
      network_latency: Math.floor(Math.random() * 30) + 5, // 5-35ms
      security_score: Math.floor(Math.random() * 20) + 75 // 75-95
    }
    
    // Simuler performance metrics réalistes
    performanceMetrics.value = {
      api_response_time: Math.floor(Math.random() * 50) + 20, // 20-70ms
      requests_per_minute: Math.floor(Math.random() * 100) + 50, // 50-150
      error_rate: Math.random() * 2, // 0-2%
      db_query_time: Math.floor(Math.random() * 30) + 10, // 10-40ms
      db_connections: Math.floor(Math.random() * 15) + 5, // 5-20
      cache_hit_rate: Math.floor(Math.random() * 15) + 85, // 85-100%
      signals_per_hour: Math.floor(Math.random() * 30) + 10, // 10-40
      success_rate: Math.floor(Math.random() * 20) + 75, // 75-95%
      execution_time: Math.floor(Math.random() * 200) + 100 // 100-300ms
    }
    
    // Mettre à jour statut des services IA
    const statuses = ['healthy', 'warning', 'error']
    Object.keys(aiServices.value).forEach(service => {
      aiServices.value[service].status = Math.random() > 0.2 ? 'healthy' : statuses[Math.floor(Math.random() * 3)]
    })
    
  } catch (error) {
    console.error('Erreur récupération données health:', error)
  }
}

const fetchSystemLogs = async () => {
  try {
    // En production, récupérer les vrais logs via API
    // Pour demo, ajouter parfois de nouveaux logs
    if (Math.random() > 0.7) {
      const logMessages = [
        '🔄 Market analysis cycle completed',
        '💎 New arbitrage opportunity detected',
        '⚡ Portfolio optimization triggered',
        '🎯 Signal confidence increased to 89%',
        '🔒 Security scan completed - all clear',
        '📈 Performance metrics updated',
        '🌐 Network latency optimized',
        '🧠 ML model retrained with new data'
      ]
      
      const levels = ['INFO', 'SUCCESS', 'WARNING']
      const newLog = {
        id: Date.now(),
        timestamp: new Date(),
        level: levels[Math.floor(Math.random() * levels.length)],
        message: logMessages[Math.floor(Math.random() * logMessages.length)]
      }
      
      systemLogs.value.unshift(newLog)
      
      // Garder seulement les 100 derniers logs
      if (systemLogs.value.length > 100) {
        systemLogs.value = systemLogs.value.slice(0, 100)
      }
    }
  } catch (error) {
    console.error('Erreur récupération logs:', error)
  }
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