/**
 * 🚀 TRADING SERVICE - Communication avec l'API de trading
 * =========================================================
 * Service pour gérer les brokers, ordres, et paper trading
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class TradingService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/trading`
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
        const error = await response.json()
        throw new Error(error.detail || `HTTP error! status: ${response.status}`)
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
        const error = await response.json()
        throw new Error(error.detail || `HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error(`POST ${endpoint} failed:`, error)
      throw error
    }
  }

  // ================================================================================
  // GESTION DES BROKERS
  // ================================================================================

  // Ajouter un broker
  async addBroker(brokerConfig) {
    return this.post('/brokers/add', brokerConfig)
  }

  // Lister les brokers
  async listBrokers() {
    return this.get('/brokers/list')
  }

  // ================================================================================
  // DONNÉES DE MARCHÉ
  // ================================================================================

  // Récupérer les données d'un asset
  async getMarketData(symbol, broker = null) {
    const endpoint = broker ? `/market-data/${symbol}?broker=${broker}` : `/market-data/${symbol}`
    return this.get(endpoint)
  }

  // Récupérer les données de plusieurs assets
  async getBatchMarketData(symbols) {
    const symbolsStr = Array.isArray(symbols) ? symbols.join(',') : symbols
    return this.get(`/market-data/batch?symbols=${symbolsStr}`)
  }

  // ================================================================================
  // ORDRES DE TRADING
  // ================================================================================

  // Placer un ordre
  async placeOrder(orderData) {
    return this.post('/orders/place', orderData)
  }

  // Historique des ordres
  async getOrdersHistory(broker = null, limit = 50) {
    const params = new URLSearchParams()
    if (broker) params.append('broker', broker)
    if (limit) params.append('limit', limit.toString())
    
    const endpoint = `/orders/history${params.toString() ? '?' + params.toString() : ''}`
    return this.get(endpoint)
  }

  // ================================================================================
  // PORTFOLIO
  // ================================================================================

  // Résumé du portfolio
  async getPortfolioSummary() {
    return this.get('/portfolio/summary')
  }

  // Positions du portfolio
  async getPositions(broker = null) {
    const endpoint = broker ? `/portfolio/positions?broker=${broker}` : '/portfolio/positions'
    return this.get(endpoint)
  }

  // ================================================================================
  // STRATÉGIES DE TRADING
  // ================================================================================

  // Démarrer une stratégie
  async startStrategy(strategyData) {
    return this.post('/strategies/start', strategyData)
  }

  // Statut des stratégies
  async getStrategiesStatus() {
    return this.get('/strategies/status')
  }

  // ================================================================================
  // PAPER TRADING
  // ================================================================================

  // Démarrer le paper trading
  async startPaperTrading() {
    return this.post('/paper-trading/start')
  }

  // Exécuter des trades de démonstration
  async executeDemoTrades() {
    return this.post('/paper-trading/demo-trades')
  }

  // Reset du paper trading
  async resetPaperTrading() {
    return this.get('/paper-trading/reset')
  }

  // ================================================================================
  // STATUT SYSTÈME
  // ================================================================================

  // Statut complet du système de trading
  async getTradingSystemStatus() {
    return this.get('/status')
  }

  // ================================================================================
  // MÉTHODES UTILITAIRES
  // ================================================================================

  // Configuration rapide d'un broker Alpaca
  async setupAlpacaBroker(apiKey, apiSecret, paperMode = true) {
    return this.addBroker({
      broker_type: 'alpaca',
      api_key: apiKey,
      api_secret: apiSecret,
      mode: paperMode ? 'paper' : 'live'
    })
  }

  // Configuration rapide d'un broker Binance
  async setupBinanceBroker(apiKey, apiSecret, paperMode = true) {
    return this.addBroker({
      broker_type: 'binance',
      api_key: apiKey,
      api_secret: apiSecret,
      mode: paperMode ? 'paper' : 'live'
    })
  }

  // Test de connectivité complet
  async testConnectivity() {
    try {
      const [brokers, status] = await Promise.all([
        this.listBrokers(),
        this.getTradingSystemStatus()
      ])

      return {
        brokers_configured: brokers.total_brokers || 0,
        brokers_connected: brokers.brokers?.filter(b => b.status === 'connected').length || 0,
        system_status: status.data?.trading_system?.status || 'unknown',
        portfolio_value: status.data?.portfolio?.total_value || 0,
        connectivity: 'ok'
      }
    } catch (error) {
      return {
        brokers_configured: 0,
        brokers_connected: 0,
        system_status: 'error',
        portfolio_value: 0,
        connectivity: 'error',
        error: error.message
      }
    }
  }

  // Ordre d'achat rapide
  async quickBuy(broker, symbol, quantity, orderType = 'market', price = null) {
    return this.placeOrder({
      broker,
      symbol,
      side: 'buy',
      quantity,
      order_type: orderType,
      price
    })
  }

  // Ordre de vente rapide
  async quickSell(broker, symbol, quantity, orderType = 'market', price = null) {
    return this.placeOrder({
      broker,
      symbol,
      side: 'sell',
      quantity,
      order_type: orderType,
      price
    })
  }

  // Surveillance temps réel des prix
  async watchPrices(symbols, callback, interval = 5000) {
    const updatePrices = async () => {
      try {
        const data = await this.getBatchMarketData(symbols)
        callback(data.data || {})
      } catch (error) {
        console.error('Erreur surveillance prix:', error)
        callback({})
      }
    }

    // Première mise à jour immédiate
    await updatePrices()

    // Puis mise à jour périodique
    return setInterval(updatePrices, interval)
  }

  // Arrêter la surveillance
  stopWatching(intervalId) {
    if (intervalId) {
      clearInterval(intervalId)
    }
  }

  // ================================================================================
  // DEMO TRADING COMPLET
  // ================================================================================

  // Configuration complète pour démo
  async setupDemo() {
    try {
      console.log('🚀 Configuration de la démo de trading...')

      // 1. Démarrer le paper trading
      console.log('📊 Démarrage paper trading...')
      await this.startPaperTrading()

      // 2. Exécuter des trades de démo
      console.log('💼 Exécution trades de démo...')
      await this.executeDemoTrades()

      // 3. Récupérer le statut
      console.log('📈 Récupération du statut...')
      const status = await this.getTradingSystemStatus()
      const portfolio = await this.getPortfolioSummary()

      console.log('✅ Démo configurée avec succès!')
      
      return {
        success: true,
        status,
        portfolio,
        message: 'Démo de trading configurée avec succès'
      }

    } catch (error) {
      console.error('❌ Erreur configuration démo:', error)
      return {
        success: false,
        error: error.message,
        message: 'Erreur lors de la configuration de la démo'
      }
    }
  }

  // Démonstration de stratégies
  async demoStrategies() {
    const strategies = [
      {
        strategy: 'meme_coins',
        capital_allocation: 0.2,
        risk_level: 'high',
        active: true
      },
      {
        strategy: 'crypto_lt',
        capital_allocation: 0.4,
        risk_level: 'medium',
        active: true
      },
      {
        strategy: 'forex',
        capital_allocation: 0.25,
        risk_level: 'medium',
        active: true
      },
      {
        strategy: 'etf',
        capital_allocation: 0.15,
        risk_level: 'low',
        active: true
      }
    ]

    const results = []
    for (const strategy of strategies) {
      try {
        const result = await this.startStrategy(strategy)
        results.push({ ...strategy, result, success: true })
      } catch (error) {
        results.push({ ...strategy, error: error.message, success: false })
      }
    }

    return results
  }
}

// Instance singleton
export const tradingService = new TradingService()
export default tradingService 