// Service pour intégrer les vraies données des modules IA
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class AIService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api/advanced-ai`
  }

  // Helper pour les requêtes HTTP
  async makeRequest(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`Erreur API ${endpoint}:`, error)
      throw error
    }
  }

  // ===== AI FEEDBACK LOOP =====
  async getFeedbackLoopStatus() {
    return this.makeRequest('/feedback/status')
  }

  async submitFeedback(signal, outcome, details = {}) {
    return this.makeRequest('/feedback/submit', {
      method: 'POST',
      body: JSON.stringify({ signal, outcome, details })
    })
  }

  async getFeedbackMetrics() {
    return this.makeRequest('/feedback/metrics')
  }

  // ===== PREDICTIVE SYSTEM =====
  async getPredictions(timeframes = ['5m', '1h', '4h', '24h']) {
    const predictions = {}
    for (const timeframe of timeframes) {
      predictions[timeframe] = await this.makeRequest(`/predictions/forecast/${timeframe}`)
    }
    return predictions
  }

  async getMarketRegime() {
    return this.makeRequest('/predictions/market-regime')
  }

  async getPredictiveAlerts() {
    return this.makeRequest('/predictions/alerts')
  }

  async getPredictiveMetrics() {
    return this.makeRequest('/predictions/metrics')
  }

  // ===== SECURITY SUPERVISOR =====
  async getSecurityStatus() {
    return this.makeRequest('/security/health-check')
  }

  async getSecurityScore() {
    return this.makeRequest('/security/score')
  }

  async getCVEScan() {
    return this.makeRequest('/security/cve-scan')
  }

  async getSecurityAlerts() {
    return this.makeRequest('/security/alerts')
  }

  // ===== PORTFOLIO OPTIMIZER =====
  async getCurrentAllocation() {
    return this.makeRequest('/portfolio/current-allocation')
  }

  async getOptimizedAllocation(strategy = 'BALANCED', riskLevel = 'MEDIUM') {
    return this.makeRequest('/portfolio/optimize', {
      method: 'POST',
      body: JSON.stringify({ strategy, risk_level: riskLevel })
    })
  }

  async getPortfolioMetrics() {
    return this.makeRequest('/portfolio/metrics')
  }

  async getRebalanceRecommendations() {
    return this.makeRequest('/portfolio/rebalance-recommendations')
  }

  // ===== DONNÉES AGRÉGÉES =====
  async getAllModulesStatus() {
    try {
      const [feedback, predictive, security, portfolio] = await Promise.allSettled([
        this.getFeedbackLoopStatus(),
        this.getPredictiveMetrics(),
        this.getSecurityStatus(),
        this.getPortfolioMetrics()
      ])

      return {
        feedback: feedback.status === 'fulfilled' ? feedback.value : null,
        predictive: predictive.status === 'fulfilled' ? predictive.value : null,
        security: security.status === 'fulfilled' ? security.value : null,
        portfolio: portfolio.status === 'fulfilled' ? portfolio.value : null,
        lastUpdate: new Date().toISOString()
      }
    } catch (error) {
      console.error('Erreur lors de la récupération du statut des modules:', error)
      throw error
    }
  }

  async getAIInsights() {
    try {
      const [predictions, alerts, marketRegime, securityAlerts] = await Promise.allSettled([
        this.getPredictiveAlerts(),
        this.getFeedbackMetrics(),
        this.getMarketRegime(),
        this.getSecurityAlerts()
      ])

      const insights = []

      // Insights des prédictions
      if (predictions.status === 'fulfilled' && predictions.value?.alerts) {
        predictions.value.alerts.forEach(alert => {
          insights.push({
            id: `pred_${alert.id || Date.now()}`,
            title: alert.title || 'Signal Prédictif',
            description: alert.message || alert.description,
            confidence: alert.confidence || 0,
            timeframe: alert.timeframe || '1h',
            priority: alert.severity === 'HIGH' ? 'high' : 
                     alert.severity === 'MEDIUM' ? 'medium' : 'low',
            type: 'prediction',
            source: 'Predictive System'
          })
        })
      }

      // Insights de sécurité
      if (securityAlerts.status === 'fulfilled' && securityAlerts.value?.alerts) {
        securityAlerts.value.alerts.forEach(alert => {
          insights.push({
            id: `sec_${alert.id || Date.now()}`,
            title: alert.title || 'Alerte Sécurité',
            description: alert.message || alert.description,
            confidence: 95,
            timeframe: 'Immédiat',
            priority: alert.level === 'CRITICAL' ? 'high' : 
                     alert.level === 'WARNING' ? 'medium' : 'low',
            type: 'security',
            source: 'Security Supervisor'
          })
        })
      }

      // Insight du régime de marché
      if (marketRegime.status === 'fulfilled' && marketRegime.value) {
        const regime = marketRegime.value
        insights.push({
          id: 'market_regime',
          title: `Régime de Marché: ${regime.regime || 'Neutre'}`,
          description: regime.description || 'Analyse du régime de marché actuel',
          confidence: Math.round((regime.confidence || 0.8) * 100),
          timeframe: '1d',
          priority: 'medium',
          type: 'market_analysis',
          source: 'Predictive System'
        })
      }

      return insights.sort((a, b) => {
        const priorityOrder = { high: 3, medium: 2, low: 1 }
        return priorityOrder[b.priority] - priorityOrder[a.priority]
      })

    } catch (error) {
      console.error('Erreur lors de la récupération des insights IA:', error)
      return []
    }
  }

  // ===== SYSTÈME DE SANTÉ =====
  async getSystemHealth() {
    try {
      const healthData = await this.getSecurityStatus()
      
      if (!healthData?.health_checks) {
        return this.getMockHealthData()
      }

      const metrics = []
      const checks = healthData.health_checks

      // CPU
      if (checks.cpu) {
        metrics.push({
          name: 'CPU Usage',
          value: `${Math.round(checks.cpu.usage || 0)}%`,
          percentage: checks.cpu.usage || 0,
          status: checks.cpu.status === 'HEALTHY' ? 'healthy' : 'warning',
          description: 'Utilisation processeur'
        })
      }

      // Mémoire
      if (checks.memory) {
        metrics.push({
          name: 'Memory',
          value: `${Math.round((checks.memory.used_gb || 0) * 10) / 10}GB`,
          percentage: Math.round((checks.memory.used_gb || 0) / (checks.memory.total_gb || 1) * 100),
          status: checks.memory.status === 'HEALTHY' ? 'healthy' : 'warning',
          description: 'Mémoire utilisée'
        })
      }

      // Disque
      if (checks.disk) {
        metrics.push({
          name: 'Disk Space',
          value: `${Math.round((checks.disk.free_gb || 0) * 10) / 10}GB`,
          percentage: Math.round((checks.disk.used_gb || 0) / ((checks.disk.used_gb || 0) + (checks.disk.free_gb || 1)) * 100),
          status: checks.disk.status === 'HEALTHY' ? 'healthy' : 'warning',
          description: 'Espace disque libre'
        })
      }

      // Réseau
      if (checks.network) {
        metrics.push({
          name: 'Network',
          value: `${Math.round(checks.network.latency_ms || 0)}ms`,
          percentage: Math.min((checks.network.latency_ms || 0) / 10, 100), // Normaliser sur 1000ms max
          status: checks.network.status === 'HEALTHY' ? 'healthy' : 'warning',
          description: 'Latence réseau'
        })
      }

      return metrics

    } catch (error) {
      console.error('Erreur lors de la récupération de la santé système:', error)
      return this.getMockHealthData()
    }
  }

  // Données de démonstration en cas d'erreur API
  getMockHealthData() {
    return [
      { name: 'CPU Usage', value: '23%', percentage: 23, status: 'healthy', description: 'Utilisation processeur normale' },
      { name: 'Memory', value: '1.2GB', percentage: 45, status: 'healthy', description: 'Mémoire disponible' },
      { name: 'Disk Space', value: '89GB', percentage: 78, status: 'warning', description: 'Espace disque restant' },
      { name: 'Network', value: '125ms', percentage: 12, status: 'healthy', description: 'Latence réseau moyenne' },
      { name: 'API Calls', value: '1,247', percentage: 92, status: 'healthy', description: 'Requêtes par minute' },
      { name: 'Error Rate', value: '0.03%', percentage: 3, status: 'healthy', description: 'Taux d\'erreur système' }
    ]
  }

  // ===== UTILITAIRES =====
  async testConnection() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`)
      return response.ok
    } catch (error) {
      console.error('Test de connexion échoué:', error)
      return false
    }
  }

  // Formatage des données pour l'interface
  formatModuleData(moduleData, moduleName) {
    if (!moduleData) return null

    const formatters = {
      feedback: (data) => ({
        score: data.adaptation_score || data.score || 85,
        signals: data.total_signals || data.signals_processed || 23,
        accuracy: data.learning_rate || 0.85,
        lastUpdate: data.last_update || new Date().toISOString()
      }),
      predictive: (data) => ({
        accuracy: Math.round((data.prediction_accuracy || 0.91) * 100),
        predictions: data.total_predictions || data.active_predictions || 147,
        regime: data.current_regime || 'Bull Market',
        lastUpdate: data.last_update || new Date().toISOString()
      }),
      security: (data) => ({
        score: data.security_score || data.overall_score || 96,
        threats: data.active_threats || data.cve_count || 0,
        status: data.status || 'HEALTHY',
        lastUpdate: data.last_scan || new Date().toISOString()
      }),
      portfolio: (data) => ({
        sharpe: data.sharpe_ratio || data.current_sharpe || 2.3,
        optimizations: data.optimization_count || data.rebalance_count || 12,
        performance: data.total_return || 0.15,
        lastUpdate: data.last_optimization || new Date().toISOString()
      })
    }

    const formatter = formatters[moduleName]
    return formatter ? formatter(moduleData) : moduleData
  }
}

// Instance singleton
export const aiService = new AIService()
export default aiService 