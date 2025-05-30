<template>
  <div class="logo-container" :class="{ 'small': size === 'small', 'large': size === 'large' }">
    <!-- Logo SVG AI Trade Bot -->
    <svg 
      viewBox="0 0 200 200" 
      :width="logoSize"
      :height="logoSize"
      class="ai-trade-logo"
    >
      <!-- Cercle de fond sombre -->
      <circle cx="100" cy="100" r="90" fill="#0f172a" stroke="#1e293b" stroke-width="2"/>
      
      <!-- Réseau de connexions -->
      <g class="network-connections" stroke="#38bdf8" stroke-width="1" opacity="0.6">
        <!-- Lignes de connexion -->
        <line x1="100" y1="30" x2="160" y2="60" />
        <line x1="160" y1="60" x2="170" y2="140" />
        <line x1="170" y1="140" x2="100" y2="170" />
        <line x1="100" y1="170" x2="30" y2="140" />
        <line x1="30" y1="140" x2="40" y2="60" />
        <line x1="40" y1="60" x2="100" y2="30" />
        
        <!-- Connexions internes -->
        <line x1="100" y1="100" x2="160" y2="60" />
        <line x1="100" y1="100" x2="170" y2="140" />
        <line x1="100" y1="100" x2="30" y2="140" />
        <line x1="100" y1="100" x2="40" y2="60" />
      </g>
      
      <!-- Nœuds du réseau -->
      <g class="network-nodes">
        <circle cx="100" cy="30" r="4" fill="#38bdf8" class="pulse-animation"/>
        <circle cx="160" cy="60" r="3" fill="#06b6d4" class="pulse-animation"/>
        <circle cx="170" cy="140" r="3" fill="#0891b2" class="pulse-animation"/>
        <circle cx="100" cy="170" r="4" fill="#38bdf8" class="pulse-animation"/>
        <circle cx="30" cy="140" r="3" fill="#06b6d4" class="pulse-animation"/>
        <circle cx="40" cy="60" r="3" fill="#0891b2" class="pulse-animation"/>
      </g>
      
      <!-- Cercle central avec gradient -->
      <defs>
        <radialGradient id="centralGradient" cx="50%" cy="50%" r="50%">
          <stop offset="0%" style="stop-color:#fbbf24;stop-opacity:1" />
          <stop offset="100%" style="stop-color:#f59e0b;stop-opacity:1" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="100" r="25" fill="url(#centralGradient)" class="central-glow"/>
      
      <!-- Texte AI -->
      <text x="100" y="90" text-anchor="middle" class="ai-text-large" fill="white" font-weight="bold">AI</text>
      <text x="100" y="115" text-anchor="middle" class="ai-text-small" fill="#e2e8f0" font-size="8">TRADE BOT</text>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  size: {
    type: String,
    default: 'medium', // small, medium, large
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})

// Computed
const logoSize = computed(() => {
  switch (props.size) {
    case 'small': return '32px'
    case 'large': return '120px'
    default: return '60px' // medium
  }
})
</script>

<style scoped>
.logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.ai-trade-logo {
  filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.3));
  transition: all 0.3s ease;
}

.ai-trade-logo:hover {
  filter: drop-shadow(0 0 15px rgba(56, 189, 248, 0.5));
  transform: scale(1.05);
}

/* Animations */
.pulse-animation {
  animation: pulse 2s infinite;
}

.central-glow {
  animation: glow 3s ease-in-out infinite alternate;
}

.network-connections {
  animation: networkFlow 4s ease-in-out infinite;
}

.ai-text-large {
  font-size: 18px;
  font-family: 'Inter', sans-serif;
}

.ai-text-small {
  font-family: 'Inter', sans-serif;
  letter-spacing: 0.1em;
}

/* Responsive sizing */
.small .ai-text-large { font-size: 10px; }
.small .ai-text-small { font-size: 4px; }

.large .ai-text-large { font-size: 24px; }
.large .ai-text-small { font-size: 10px; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@keyframes glow {
  0% { filter: drop-shadow(0 0 5px rgba(251, 191, 36, 0.5)); }
  100% { filter: drop-shadow(0 0 20px rgba(251, 191, 36, 0.8)); }
}

@keyframes networkFlow {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
</style> 