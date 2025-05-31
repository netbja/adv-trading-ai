/**
 * 🧠 AI SERVICE - Communication avec les modules IA avancée
 * =======================================================
 * Service pour interagir avec les 16 endpoints d'IA avancée du backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class AIService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/advanced-ai`
  }

  // Utilitaire pour requêtes GET
  async get(endpoint) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`GET ${endpoint} failed:`, error)
      throw error
    }
  }

  // Utilitaire pour requêtes POST
  async post(endpoint, data = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`POST ${endpoint} failed:`, error)
      throw error
    }
  }

  // ================================================================================
  // 🧠 AI FEEDBACK LOOP ENDPOINTS
  // ================================================================================

  // Obtenir les patterns d'apprentissage
  async getFeedbackPatterns() {
    return this.get('/feedback/patterns')
  }

  // Obtenir les adaptations récentes
  async getFeedbackAdaptations() {
    return this.get('/feedback/adaptations')
  }

  // Soumettre un signal d'apprentissage
  async submitLearningSignal(signalData) {
    return this.post('/feedback/learn', signalData)
  }

  // Analyser les performances
  async analyzePerformance(performanceData) {
    return this.post('/feedback/analyze-performance', performanceData)
  }

  // ================================================================================
  // 🔮 PREDICTIVE SYSTEM ENDPOINTS
  // ================================================================================

  // Détecter le régime de marché
  async getMarketRegime() {
    return this.get('/prediction/regime')
  }

  // Obtenir les alertes prédictives
  async getPredictiveAlerts() {
    return this.get('/prediction/alerts')
  }

  // Générer des prédictions
  async generatePrediction(predictionData) {
    return this.post('/prediction/forecast', predictionData)
  }

  // Obtenir l'analyse historique
  async getHistoricalAnalysis(assetType) {
    return this.get(`/prediction/analysis/${assetType}`)
  }

  // ================================================================================
  // 🛡️ SECURITY SUPERVISOR ENDPOINTS
  // ================================================================================

  // Obtenir le dashboard de sécurité
  async getSecurityDashboard() {
    return this.get('/security/dashboard')
  }

  // Obtenir les alertes de sécurité
  async getSecurityAlerts() {
    return this.get('/security/alerts')
  }

  // Lancer un health check
  async runHealthCheck() {
    return this.post('/security/health-check')
  }

  // Scanner les vulnérabilités
  async scanVulnerabilities(scanOptions = {}) {
    return this.post('/security/cve-scan', scanOptions)
  }

  // ================================================================================
  // 📊 PORTFOLIO OPTIMIZER ENDPOINTS
  // ================================================================================

  // Obtenir les métriques du portfolio
  async getPortfolioMetrics() {
    return this.get('/portfolio/metrics')
  }

  // Obtenir les recommandations de rééquilibrage
  async getRebalanceRecommendations() {
    return this.get('/portfolio/rebalance')
  }

  // Optimiser le portfolio
  async optimizePortfolio(optimizationData) {
    return this.post('/portfolio/optimize', optimizationData)
  }

  // Obtenir le résumé d'optimisation
  async getOptimizationSummary() {
    return this.get('/portfolio/summary')
  }

  // ================================================================================
  // 🔄 SYSTEM CONTROL ENDPOINTS
  // ================================================================================

  // Obtenir le statut complet du système
  async getCompleteSystemStatus() {
    return this.get('/status/complete')
  }

  // Réinitialiser tous les modules
  async resetAllModules(confirm = false) {
    return this.post('/control/reset', { confirm })
  }

  // ================================================================================
  // 🚀 MÉTHODES UTILITAIRES ET COMBINÉES
  // ================================================================================

  // Obtenir tous les dashboards en une fois
  async getAllDashboards() {
    try {
      const [
        systemStatus,
        securityDashboard,
        portfolioMetrics,
        marketRegime,
        feedbackPatterns
      ] = await Promise.all([
        this.getCompleteSystemStatus(),
        this.getSecurityDashboard(),
        this.getPortfolioMetrics(),
        this.getMarketRegime(),
        this.getFeedbackPatterns()
      ])

      return {
        system: systemStatus,
        security: securityDashboard,
        portfolio: portfolioMetrics,
        market: marketRegime,
        feedback: feedbackPatterns
      }
    } catch (error) {
      console.error('Failed to fetch all dashboards:', error)
      throw error
    }
  }

  // Obtenir toutes les alertes
  async getAllAlerts() {
    try {
      const [securityAlerts, predictiveAlerts] = await Promise.all([
        this.getSecurityAlerts(),
        this.getPredictiveAlerts()
      ])

      return {
        security: securityAlerts,
        predictive: predictiveAlerts
      }
    } catch (error) {
      console.error('Failed to fetch all alerts:', error)
      throw error
    }
  }

  // Test de connectivité avec tous les modules
  async testAllModules() {
    const results = {}
    const endpoints = [
      { name: 'Feedback Patterns', method: () => this.getFeedbackPatterns() },
      { name: 'Market Regime', method: () => this.getMarketRegime() },
      { name: 'Security Dashboard', method: () => this.getSecurityDashboard() },
      { name: 'Portfolio Metrics', method: () => this.getPortfolioMetrics() },
      { name: 'System Status', method: () => this.getCompleteSystemStatus() }
    ]

    for (const endpoint of endpoints) {
      try {
        const result = await endpoint.method()
        results[endpoint.name] = { status: 'success', data: result }
      } catch (error) {
        results[endpoint.name] = { status: 'error', error: error.message }
      }
    }

    return results
  }
}

// Instance singleton
export const aiService = new AIService()
export default aiService 