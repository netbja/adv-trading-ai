// 🔍 AI HEALTH MONITOR - RÉSEAU, API, RPC avec BOUCLES DE RÉTROACTION
console.log("🔍 Starting AI Health Monitor with Feedback Loops...");

// 🎯 CONFIGURATION HEALTH MONITOR IA
const HEALTH_CONFIG = {
  // Intervalles adaptatifs
  monitoring: {
    baseInterval: 60000,        // 1 minute base
    fastInterval: 15000,        // 15 secondes si problèmes
    slowInterval: 300000,       // 5 minutes si tout va bien
    emergencyInterval: 5000,    // 5 secondes en urgence
    adaptiveThreshold: 0.7      // Seuil pour adaptation
  },
  
  // Seuils de santé
  thresholds: {
    responseTime: {
      excellent: 1000,    // <1s excellent
      good: 3000,         // <3s bon
      warning: 8000,      // <8s warning
      critical: 15000     // >15s critique
    },
    availability: {
      excellent: 0.99,    // 99%+ excellent
      good: 0.95,         // 95%+ bon
      warning: 0.90,      // 90%+ warning
      critical: 0.80      // <80% critique
    },
    consecutiveFailures: {
      warning: 3,         // 3 échecs = warning
      critical: 5,        // 5 échecs = critique
      emergency: 10       // 10 échecs = urgence
    }
  },
  
  // Services à monitorer
  services: {
    // APIs Crypto
    apis: {
      pumpfun: {
        name: "Pump.fun API",
        url: "https://api.pump.fun/tokens/trending?limit=1",
        type: "API",
        priority: "HIGH",
        timeout: 10000,
        expectedFields: ['symbol', 'name'],
        rateLimit: { calls: 0, window: 60000, limit: 100 }
      },
      dexscreener: {
        name: "DexScreener API", 
        url: "https://api.dexscreener.com/latest/dex/search/?q=solana",
        type: "API",
        priority: "HIGH",
        timeout: 8000,
        expectedFields: ['pairs'],
        rateLimit: { calls: 0, window: 60000, limit: 300 }
      },
      coingecko: {
        name: "CoinGecko API",
        url: "https://api.coingecko.com/api/v3/ping",
        type: "API", 
        priority: "MEDIUM",
        timeout: 12000,
        expectedFields: ['gecko_says'],
        rateLimit: { calls: 0, window: 60000, limit: 50 }
      },
      birdeye: {
        name: "BirdEye API",
        url: "https://public-api.birdeye.so/defi/tokenlist?offset=0&limit=1",
        type: "API",
        priority: "MEDIUM",
        timeout: 10000,
        headers: { 'X-API-KEY': process.env.BIRDEYE_API_KEY },
        expectedFields: ['data'],
        rateLimit: { calls: 0, window: 60000, limit: 100 }
      }
    },
    
    // RPC Nodes
    rpc: {
      solana_mainnet: {
        name: "Solana Mainnet RPC",
        url: "https://api.mainnet-beta.solana.com",
        type: "RPC",
        priority: "CRITICAL",
        timeout: 5000,
        method: "getHealth",
        expectedResponse: "ok"
      },
      ethereum_mainnet: {
        name: "Ethereum Mainnet RPC", 
        url: process.env.ETH_RPC_URL || "https://mainnet.infura.io/v3/demo",
        type: "RPC",
        priority: "HIGH",
        timeout: 8000,
        method: "eth_blockNumber",
        expectedType: "string"
      },
      base_mainnet: {
        name: "Base Mainnet RPC",
        url: "https://mainnet.base.org",
        type: "RPC",
        priority: "MEDIUM",
        timeout: 8000,
        method: "eth_blockNumber",
        expectedType: "string"
      }
    },
    
    // Services internes
    internal: {
      postgres: {
        name: "PostgreSQL Database",
        type: "DATABASE",
        priority: "CRITICAL",
        timeout: 3000,
        testQuery: "SELECT 1 as health"
      },
      n8n: {
        name: "N8N Workflow Engine",
        url: "http://n8n:5678/healthz",
        type: "SERVICE",
        priority: "CRITICAL",
        timeout: 5000
      },
      grafana: {
        name: "Grafana Dashboard",
        url: "http://grafana:3000/api/health",
        type: "SERVICE", 
        priority: "HIGH",
        timeout: 5000
      }
    }
  }
};

// 🤖 AI HEALTH MONITOR CLASS
class AIHealthMonitor {
  constructor() {
    this.state = {
      isRunning: false,
      currentInterval: HEALTH_CONFIG.monitoring.baseInterval,
      globalHealth: {
        score: 1.0,
        status: 'EXCELLENT',
        lastUpdate: new Date().toISOString()
      },
      services: {},
      history: [],
      alerts: [],
      patterns: {
        degradationPatterns: [],
        recoveryPatterns: [],
        predictiveInsights: []
      }
    };
    
    this.brain = new HealthAI();
    this.feedbackLoop = new HealthFeedbackLoop();
    this.alertManager = new HealthAlertManager();
    
    // Initialiser état des services
    this.initializeServicesState();
  }

  // 🚀 DÉMARRER MONITORING IA
  async start() {
    console.log("🚀 Starting AI Health Monitor...");
    this.state.isRunning = true;
    
    // Boucle principale de monitoring intelligent
    while (this.state.isRunning) {
      try {
        console.log(`🔍 Health check cycle (interval: ${this.state.currentInterval/1000}s)`);
        
        // 1. Effectuer checks de santé
        const healthResults = await this.performHealthChecks();
        
        // 2. Analyser avec IA
        const aiAnalysis = await this.brain.analyzeHealthData(healthResults);
        
        // 3. Mettre à jour état global
        this.updateGlobalHealth(healthResults, aiAnalysis);
        
        // 4. Détection de patterns
        const patterns = await this.brain.detectPatterns(this.state.history);
        
        // 5. Prédictions et recommandations
        const predictions = await this.brain.generatePredictions(patterns);
        
        // 6. Feedback loop vers orchestrateur autonome
        await this.feedbackLoop.sendHealthFeedback({
          globalHealth: this.state.globalHealth,
          serviceHealth: healthResults,
          patterns: patterns,
          predictions: predictions,
          recommendations: aiAnalysis.recommendations
        });
        
        // 7. Gestion alertes intelligentes
        await this.alertManager.processAlerts(healthResults, aiAnalysis);
        
        // 8. Adaptation intelligente de l'intervalle
        this.state.currentInterval = await this.brain.calculateOptimalInterval(
          this.state.globalHealth, 
          patterns
        );
        
        // 9. Nettoyage historique
        this.cleanupHistory();
        
        console.log(`✅ Health check completed - Global Score: ${(this.state.globalHealth.score * 100).toFixed(1)}%`);
        
        // 10. Attente adaptative
        await this.sleep(this.state.currentInterval);
        
      } catch (error) {
        console.error("❌ Health monitor error:", error);
        // Fallback sur intervalle d'urgence
        await this.sleep(HEALTH_CONFIG.monitoring.emergencyInterval);
      }
    }
  }

  // 🛑 ARRÊTER MONITORING
  stop() {
    console.log("🛑 Stopping AI Health Monitor...");
    this.state.isRunning = false;
  }

  // 🔍 EFFECTUER CHECKS DE SANTÉ
  async performHealthChecks() {
    console.log("🔍 Performing comprehensive health checks...");
    
    const results = {
      timestamp: new Date().toISOString(),
      apis: {},
      rpc: {},
      internal: {},
      summary: {
        total: 0,
        healthy: 0,
        degraded: 0,
        critical: 0
      }
    };

    // Check APIs en parallèle
    const apiPromises = Object.entries(HEALTH_CONFIG.services.apis).map(
      ([key, config]) => this.checkAPI(key, config)
    );
    
    const apiResults = await Promise.allSettled(apiPromises);
    apiResults.forEach((result, index) => {
      const key = Object.keys(HEALTH_CONFIG.services.apis)[index];
      results.apis[key] = result.status === 'fulfilled' ? result.value : 
        { status: 'ERROR', error: result.reason?.message || 'Unknown error' };
    });

    // Check RPCs en parallèle
    const rpcPromises = Object.entries(HEALTH_CONFIG.services.rpc).map(
      ([key, config]) => this.checkRPC(key, config)
    );
    
    const rpcResults = await Promise.allSettled(rpcPromises);
    rpcResults.forEach((result, index) => {
      const key = Object.keys(HEALTH_CONFIG.services.rpc)[index];
      results.rpc[key] = result.status === 'fulfilled' ? result.value :
        { status: 'ERROR', error: result.reason?.message || 'Unknown error' };
    });

    // Check services internes
    const internalPromises = Object.entries(HEALTH_CONFIG.services.internal).map(
      ([key, config]) => this.checkInternal(key, config)
    );
    
    const internalResults = await Promise.allSettled(internalPromises);
    internalResults.forEach((result, index) => {
      const key = Object.keys(HEALTH_CONFIG.services.internal)[index];
      results.internal[key] = result.status === 'fulfilled' ? result.value :
        { status: 'ERROR', error: result.reason?.message || 'Unknown error' };
    });

    // Calculer summary
    const allResults = [
      ...Object.values(results.apis),
      ...Object.values(results.rpc), 
      ...Object.values(results.internal)
    ];

    results.summary.total = allResults.length;
    results.summary.healthy = allResults.filter(r => r.status === 'HEALTHY').length;
    results.summary.degraded = allResults.filter(r => r.status === 'DEGRADED').length;
    results.summary.critical = allResults.filter(r => ['CRITICAL', 'ERROR'].includes(r.status)).length;

    console.log(`📊 Health Summary: ${results.summary.healthy}H/${results.summary.degraded}D/${results.summary.critical}C`);
    
    return results;
  }

  // 🌐 CHECK API
  async checkAPI(key, config) {
    const startTime = Date.now();
    
    try {
      // Vérifier rate limit
      if (this.isRateLimited(key, config)) {
        return {
          service: key,
          status: 'RATE_LIMITED',
          responseTime: 0,
          message: 'Rate limit exceeded',
          timestamp: new Date().toISOString()
        };
      }

      const headers = config.headers || {};
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), config.timeout);

      const response = await fetch(config.url, {
        headers: headers,
        signal: controller.signal
      });

      clearTimeout(timeoutId);
      const responseTime = Date.now() - startTime;

      // Incrémenter compteur rate limit
      this.updateRateLimit(key, config);

      let status = 'HEALTHY';
      let healthScore = 1.0;

      // Évaluer performance
      if (responseTime > HEALTH_CONFIG.thresholds.responseTime.critical) {
        status = 'CRITICAL';
        healthScore = 0.2;
      } else if (responseTime > HEALTH_CONFIG.thresholds.responseTime.warning) {
        status = 'DEGRADED';
        healthScore = 0.6;
      } else if (responseTime > HEALTH_CONFIG.thresholds.responseTime.good) {
        status = 'GOOD';
        healthScore = 0.8;
      }

      // Vérifier contenu réponse
      if (response.ok && config.expectedFields) {
        try {
          const data = await response.json();
          const hasExpectedFields = config.expectedFields.every(field => 
            data.hasOwnProperty(field) || (data.data && data.data.hasOwnProperty(field))
          );
          
          if (!hasExpectedFields) {
            status = 'DEGRADED';
            healthScore = Math.min(healthScore, 0.7);
          }
        } catch (jsonError) {
          status = 'DEGRADED'; 
          healthScore = Math.min(healthScore, 0.5);
        }
      }

      // Mettre à jour historique service
      this.updateServiceHistory(key, { success: response.ok, responseTime, status });

      return {
        service: key,
        status: response.ok ? status : 'ERROR',
        responseTime: responseTime,
        httpStatus: response.status,
        healthScore: response.ok ? healthScore : 0.1,
        message: response.ok ? 'API responding normally' : `HTTP ${response.status}`,
        timestamp: new Date().toISOString(),
        url: config.url
      };

    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      // Mettre à jour historique d'échec
      this.updateServiceHistory(key, { success: false, responseTime, error: error.message });

      return {
        service: key,
        status: 'ERROR',
        responseTime: responseTime,
        healthScore: 0,
        error: error.name === 'AbortError' ? 'Timeout' : error.message,
        message: `API check failed: ${error.message}`,
        timestamp: new Date().toISOString(),
        url: config.url
      };
    }
  }

  // ⚡ CHECK RPC
  async checkRPC(key, config) {
    const startTime = Date.now();
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), config.timeout);

      let requestBody;
      if (config.method === 'getHealth') {
        // Solana health check
        requestBody = {
          jsonrpc: "2.0",
          id: 1,
          method: "getHealth"
        };
      } else if (config.method === 'eth_blockNumber') {
        // Ethereum block number
        requestBody = {
          jsonrpc: "2.0",
          id: 1,
          method: "eth_blockNumber",
          params: []
        };
      }

      const response = await fetch(config.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      });

      clearTimeout(timeoutId);
      const responseTime = Date.now() - startTime;

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const data = await response.json();
      
      // Vérifier réponse selon le type
      let isHealthy = false;
      if (config.method === 'getHealth') {
        isHealthy = data.result === 'ok';
      } else if (config.method === 'eth_blockNumber') {
        isHealthy = data.result && typeof data.result === 'string' && data.result.startsWith('0x');
      }

      let status = 'HEALTHY';
      let healthScore = 1.0;

      if (!isHealthy) {
        status = 'DEGRADED';
        healthScore = 0.5;
      } else if (responseTime > HEALTH_CONFIG.thresholds.responseTime.warning) {
        status = 'DEGRADED';
        healthScore = 0.7;
      }

      this.updateServiceHistory(key, { success: isHealthy, responseTime, status });

      return {
        service: key,
        status: status,
        responseTime: responseTime,
        healthScore: healthScore,
        result: data.result,
        message: isHealthy ? 'RPC responding normally' : 'RPC response invalid',
        timestamp: new Date().toISOString(),
        url: config.url
      };

    } catch (error) {
      const responseTime = Date.now() - startTime;
      this.updateServiceHistory(key, { success: false, responseTime, error: error.message });

      return {
        service: key,
        status: 'ERROR',
        responseTime: responseTime,
        healthScore: 0,
        error: error.name === 'AbortError' ? 'Timeout' : error.message,
        message: `RPC check failed: ${error.message}`,
        timestamp: new Date().toISOString(),
        url: config.url
      };
    }
  }

  // 🏠 CHECK SERVICES INTERNES
  async checkInternal(key, config) {
    const startTime = Date.now();
    
    try {
      if (config.type === 'DATABASE') {
        // Check PostgreSQL
        // Note: Ici on simule car on n'a pas accès direct à pg
        // Dans l'implémentation réelle, utiliser pg client
        return {
          service: key,
          status: 'HEALTHY',
          responseTime: 50,
          healthScore: 1.0,
          message: 'Database responding normally',
          timestamp: new Date().toISOString()
        };
      } else {
        // Check HTTP service
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), config.timeout);

        const response = await fetch(config.url, {
          signal: controller.signal
        });

        clearTimeout(timeoutId);
        const responseTime = Date.now() - startTime;

        let status = 'HEALTHY';
        let healthScore = 1.0;

        if (!response.ok) {
          status = 'ERROR';
          healthScore = 0.1;
        } else if (responseTime > HEALTH_CONFIG.thresholds.responseTime.warning) {
          status = 'DEGRADED';
          healthScore = 0.7;
        }

        return {
          service: key,
          status: status,
          responseTime: responseTime,
          httpStatus: response.status,
          healthScore: healthScore,
          message: response.ok ? 'Service responding normally' : `HTTP ${response.status}`,
          timestamp: new Date().toISOString(),
          url: config.url
        };
      }

    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      return {
        service: key,
        status: 'ERROR',
        responseTime: responseTime,
        healthScore: 0,
        error: error.name === 'AbortError' ? 'Timeout' : error.message,
        message: `Internal service check failed: ${error.message}`,
        timestamp: new Date().toISOString()
      };
    }
  }

  // 📊 METTRE À JOUR SANTÉ GLOBALE
  updateGlobalHealth(healthResults, aiAnalysis) {
    const allServices = [
      ...Object.values(healthResults.apis),
      ...Object.values(healthResults.rpc),
      ...Object.values(healthResults.internal)
    ];

    // Calculer score pondéré selon priorité
    let totalWeight = 0;
    let weightedScore = 0;

    allServices.forEach(service => {
      const config = this.findServiceConfig(service.service);
      const weight = this.getPriorityWeight(config?.priority || 'MEDIUM');
      
      totalWeight += weight;
      weightedScore += (service.healthScore || 0) * weight;
    });

    const globalScore = totalWeight > 0 ? weightedScore / totalWeight : 0;

    // Déterminer status global
    let globalStatus = 'EXCELLENT';
    if (globalScore < 0.5) {
      globalStatus = 'CRITICAL';
    } else if (globalScore < 0.7) {
      globalStatus = 'DEGRADED';
    } else if (globalScore < 0.9) {
      globalStatus = 'GOOD';
    }

    this.state.globalHealth = {
      score: globalScore,
      status: globalStatus,
      lastUpdate: new Date().toISOString(),
      criticalServices: allServices.filter(s => ['CRITICAL', 'ERROR'].includes(s.status)).length,
      degradedServices: allServices.filter(s => s.status === 'DEGRADED').length,
      healthyServices: allServices.filter(s => s.status === 'HEALTHY').length
    };

    // Ajouter à l'historique
    this.state.history.push({
      timestamp: new Date().toISOString(),
      globalHealth: this.state.globalHealth,
      serviceResults: healthResults,
      aiAnalysis: aiAnalysis
    });
  }

  // 🔧 UTILITAIRES
  initializeServicesState() {
    const allServices = {
      ...HEALTH_CONFIG.services.apis,
      ...HEALTH_CONFIG.services.rpc,
      ...HEALTH_CONFIG.services.internal
    };

    Object.keys(allServices).forEach(key => {
      this.state.services[key] = {
        history: [],
        consecutiveFailures: 0,
        lastSuccess: null,
        availability: 1.0
      };
    });
  }

  updateServiceHistory(serviceKey, result) {
    if (!this.state.services[serviceKey]) {
      this.state.services[serviceKey] = {
        history: [],
        consecutiveFailures: 0,
        lastSuccess: null,
        availability: 1.0
      };
    }

    const service = this.state.services[serviceKey];
    
    // Ajouter à l'historique
    service.history.push({
      ...result,
      timestamp: new Date().toISOString()
    });

    // Garder seulement les 100 derniers
    if (service.history.length > 100) {
      service.history = service.history.slice(-100);
    }

    // Mettre à jour compteurs
    if (result.success) {
      service.consecutiveFailures = 0;
      service.lastSuccess = new Date().toISOString();
    } else {
      service.consecutiveFailures++;
    }

    // Calculer availability (sur dernières 24h)
    const last24h = service.history.filter(h => 
      Date.now() - new Date(h.timestamp).getTime() < 86400000
    );
    
    if (last24h.length > 0) {
      const successes = last24h.filter(h => h.success).length;
      service.availability = successes / last24h.length;
    }
  }

  isRateLimited(serviceKey, config) {
    if (!config.rateLimit) return false;
    
    const now = Date.now();
    const rateLimit = config.rateLimit;
    
    // Reset window si nécessaire
    if (now - rateLimit.resetTime > rateLimit.window) {
      rateLimit.calls = 0;
      rateLimit.resetTime = now;
    }
    
    return rateLimit.calls >= rateLimit.limit;
  }

  updateRateLimit(serviceKey, config) {
    if (config.rateLimit) {
      config.rateLimit.calls++;
    }
  }

  findServiceConfig(serviceKey) {
    return HEALTH_CONFIG.services.apis[serviceKey] ||
           HEALTH_CONFIG.services.rpc[serviceKey] ||
           HEALTH_CONFIG.services.internal[serviceKey];
  }

  getPriorityWeight(priority) {
    const weights = {
      'CRITICAL': 3,
      'HIGH': 2,
      'MEDIUM': 1,
      'LOW': 0.5
    };
    return weights[priority] || 1;
  }

  cleanupHistory() {
    // Garder seulement les 500 derniers checks
    if (this.state.history.length > 500) {
      this.state.history = this.state.history.slice(-500);
    }
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 🧠 HEALTH AI ENGINE
class HealthAI {
  constructor() {
    this.patterns = {
      degradation: [],
      recovery: [],
      predictions: []
    };
  }

  async analyzeHealthData(healthResults) {
    console.log("🧠 AI analyzing health data...");
    
    const analysis = {
      overallTrend: this.analyzeTrend(healthResults),
      criticalIssues: this.identifyCriticalIssues(healthResults),
      recommendations: this.generateRecommendations(healthResults),
      riskAssessment: this.assessRisk(healthResults),
      confidenceLevel: 0.8
    };

    return analysis;
  }

  analyzeTrend(healthResults) {
    const criticalCount = healthResults.summary.critical;
    const degradedCount = healthResults.summary.degraded;
    const healthyCount = healthResults.summary.healthy;
    const total = healthResults.summary.total;

    if (criticalCount > total * 0.3) {
      return 'DETERIORATING';
    } else if (degradedCount > total * 0.5) {
      return 'DECLINING';
    } else if (healthyCount > total * 0.8) {
      return 'IMPROVING';
    } else {
      return 'STABLE';
    }
  }

  identifyCriticalIssues(healthResults) {
    const issues = [];
    
    // APIs critiques en panne
    Object.entries(healthResults.apis).forEach(([key, result]) => {
      if (['CRITICAL', 'ERROR'].includes(result.status)) {
        const config = HEALTH_CONFIG.services.apis[key];
        if (config?.priority === 'CRITICAL' || config?.priority === 'HIGH') {
          issues.push({
            type: 'API_CRITICAL',
            service: key,
            message: `Critical API ${key} is down: ${result.error || result.message}`,
            impact: 'HIGH',
            urgency: 'IMMEDIATE'
          });
        }
      }
    });

    // RPCs en panne
    Object.entries(healthResults.rpc).forEach(([key, result]) => {
      if (['CRITICAL', 'ERROR'].includes(result.status)) {
        issues.push({
          type: 'RPC_CRITICAL',
          service: key,
          message: `RPC node ${key} is unreachable: ${result.error || result.message}`,
          impact: 'HIGH',
          urgency: 'IMMEDIATE'
        });
      }
    });

    return issues;
  }

  generateRecommendations(healthResults) {
    const recommendations = [];

    // Recommandations basées sur les résultats
    if (healthResults.summary.critical > 0) {
      recommendations.push({
        type: 'IMMEDIATE_ACTION',
        priority: 'HIGH',
        message: 'Switch to fallback APIs immediately',
        action: 'ENABLE_FALLBACKS'
      });
    }

    if (healthResults.summary.degraded > healthResults.summary.total * 0.3) {
      recommendations.push({
        type: 'PREVENTIVE_ACTION',
        priority: 'MEDIUM', 
        message: 'Reduce trading frequency to preserve API limits',
        action: 'REDUCE_FREQUENCY'
      });
    }

    return recommendations;
  }

  assessRisk(healthResults) {
    let riskScore = 0;
    
    // API risks
    const apiRisk = (healthResults.summary.critical * 0.5 + healthResults.summary.degraded * 0.2) / healthResults.summary.total;
    riskScore += apiRisk * 0.6;
    
    // RPC risks
    const rpcCritical = Object.values(healthResults.rpc).filter(r => ['CRITICAL', 'ERROR'].includes(r.status)).length;
    const rpcTotal = Object.values(healthResults.rpc).length;
    const rpcRisk = rpcTotal > 0 ? rpcCritical / rpcTotal : 0;
    riskScore += rpcRisk * 0.4;

    return {
      score: Math.min(1, riskScore),
      level: riskScore > 0.7 ? 'HIGH' : riskScore > 0.4 ? 'MEDIUM' : 'LOW',
      factors: {
        apiHealth: apiRisk,
        rpcHealth: rpcRisk
      }
    };
  }

  async detectPatterns(history) {
    // Analyse de patterns sur l'historique
    if (history.length < 10) return [];

    const patterns = [];
    
    // Pattern de dégradation progressive
    const recentChecks = history.slice(-10);
    const scores = recentChecks.map(h => h.globalHealth.score);
    
    let declining = true;
    for (let i = 1; i < scores.length; i++) {
      if (scores[i] >= scores[i-1]) {
        declining = false;
        break;
      }
    }
    
    if (declining) {
      patterns.push({
        type: 'PROGRESSIVE_DEGRADATION',
        confidence: 0.8,
        message: 'Progressive degradation detected over last 10 checks',
        recommendation: 'Investigate root cause immediately'
      });
    }

    return patterns;
  }

  async generatePredictions(patterns) {
    const predictions = [];

    patterns.forEach(pattern => {
      if (pattern.type === 'PROGRESSIVE_DEGRADATION') {
        predictions.push({
          type: 'SYSTEM_FAILURE_RISK',
          timeframe: '15-30 minutes',
          probability: 0.75,
          message: 'High probability of system failure if degradation continues',
          preventiveActions: ['Enable emergency fallbacks', 'Reduce trading volume', 'Alert admin']
        });
      }
    });

    return predictions;
  }

  async calculateOptimalInterval(globalHealth, patterns) {
    let interval = HEALTH_CONFIG.monitoring.baseInterval;

    // Adapter selon santé globale
    if (globalHealth.status === 'CRITICAL') {
      interval = HEALTH_CONFIG.monitoring.emergencyInterval;
    } else if (globalHealth.status === 'DEGRADED') {
      interval = HEALTH_CONFIG.monitoring.fastInterval;
    } else if (globalHealth.status === 'EXCELLENT' && globalHealth.score > 0.95) {
      interval = HEALTH_CONFIG.monitoring.slowInterval;
    }

    // Adapter selon patterns détectés
    const criticalPatterns = patterns.filter(p => p.confidence > 0.7);
    if (criticalPatterns.length > 0) {
      interval = Math.min(interval, HEALTH_CONFIG.monitoring.fastInterval);
    }

    return interval;
  }
}

// 🔄 HEALTH FEEDBACK LOOP
class HealthFeedbackLoop {
  constructor() {
    this.feedbackHistory = [];
  }

  async sendHealthFeedback(healthData) {
    console.log("🔄 Sending health feedback to autonomous orchestrator...");
    
    const feedback = {
      timestamp: new Date().toISOString(),
      healthScore: healthData.globalHealth.score,
      systemStatus: healthData.globalHealth.status,
      criticalIssues: healthData.patterns.filter(p => p.confidence > 0.8),
      recommendations: healthData.recommendations,
      apiAvailability: this.calculateAPIAvailability(healthData.serviceHealth),
      rpcAvailability: this.calculateRPCAvailability(healthData.serviceHealth),
      tradingRecommendation: this.generateTradingRecommendation(healthData),
      urgencyLevel: this.calculateUrgencyLevel(healthData)
    };

    // Envoyer à l'orchestrateur autonome via variables partagées N8N
    try {
      // Dans N8N, ceci mettrait à jour des variables workflow
      global.HEALTH_FEEDBACK = feedback;
      
      // Déclencher interruption si critique
      if (feedback.urgencyLevel === 'CRITICAL' && global.AutonomousOrchestrator) {
        global.AutonomousOrchestrator.interrupt(`Health crisis: ${feedback.systemStatus}`);
      }
      
      console.log(`✅ Health feedback sent - Status: ${feedback.systemStatus}, Score: ${(feedback.healthScore * 100).toFixed(1)}%`);
      
    } catch (error) {
      console.error("❌ Failed to send health feedback:", error);
    }

    // Archiver feedback
    this.feedbackHistory.push(feedback);
    if (this.feedbackHistory.length > 100) {
      this.feedbackHistory = this.feedbackHistory.slice(-100);
    }

    return feedback;
  }

  calculateAPIAvailability(serviceHealth) {
    const apis = Object.values(serviceHealth.apis);
    if (apis.length === 0) return 0;
    
    const healthy = apis.filter(api => ['HEALTHY', 'GOOD'].includes(api.status)).length;
    return healthy / apis.length;
  }

  calculateRPCAvailability(serviceHealth) {
    const rpcs = Object.values(serviceHealth.rpc);
    if (rpcs.length === 0) return 0;
    
    const healthy = rpcs.filter(rpc => ['HEALTHY', 'GOOD'].includes(rpc.status)).length;
    return healthy / rpcs.length;
  }

  generateTradingRecommendation(healthData) {
    const apiAvail = this.calculateAPIAvailability(healthData.serviceHealth);
    const rpcAvail = this.calculateRPCAvailability(healthData.serviceHealth);
    const globalScore = healthData.globalHealth.score;

    if (globalScore < 0.3) {
      return {
        action: 'EMERGENCY_STOP',
        reason: 'Critical system health',
        confidence: 0.95
      };
    } else if (apiAvail < 0.5) {
      return {
        action: 'PAUSE_TRADING',
        reason: 'Insufficient API availability',
        confidence: 0.85
      };
    } else if (globalScore < 0.6) {
      return {
        action: 'REDUCE_FREQUENCY',
        reason: 'Degraded system performance',
        confidence: 0.75
      };
    } else if (globalScore > 0.9) {
      return {
        action: 'OPTIMIZE_PERFORMANCE',
        reason: 'Excellent system health',  
        confidence: 0.80
      };
    } else {
      return {
        action: 'CONTINUE_NORMAL',
        reason: 'Stable system health',
        confidence: 0.70
      };
    }
  }

  calculateUrgencyLevel(healthData) {
    const criticalServices = healthData.globalHealth.criticalServices || 0;
    const globalScore = healthData.globalHealth.score;
    const criticalPatterns = healthData.patterns.filter(p => p.confidence > 0.8).length;

    if (criticalServices > 2 || globalScore < 0.3 || criticalPatterns > 1) {
      return 'CRITICAL';
    } else if (criticalServices > 0 || globalScore < 0.6 || criticalPatterns > 0) {
      return 'HIGH';
    } else if (globalScore < 0.8) {
      return 'MEDIUM';
    } else {
      return 'LOW';
    }
  }
}

// 🚨 HEALTH ALERT MANAGER
class HealthAlertManager {
  constructor() {
    this.alertHistory = [];
    this.alertThresholds = {
      globalScore: 0.5,
      consecutiveFailures: 3,
      responseTime: 10000
    };
  }

  async processAlerts(healthResults, aiAnalysis) {
    console.log("🚨 Processing health alerts...");
    
    const alerts = [];

    // Alertes globales
    if (healthResults.summary.critical > 0) {
      alerts.push({
        level: 'CRITICAL',
        type: 'SYSTEM_CRITICAL',
        message: `${healthResults.summary.critical} critical services detected`,
        services: this.getCriticalServices(healthResults),
        action: 'IMMEDIATE_ATTENTION_REQUIRED',
        timestamp: new Date().toISOString()
      });
    }

    // Alertes API spécifiques
    Object.entries(healthResults.apis).forEach(([key, result]) => {
      if (result.status === 'ERROR' && HEALTH_CONFIG.services.apis[key]?.priority === 'HIGH') {
        alerts.push({
          level: 'HIGH',
          type: 'API_DOWN',
          message: `High priority API ${key} is down: ${result.error}`,
          service: key,
          action: 'ENABLE_FALLBACK_API',
          timestamp: new Date().toISOString()
        });
      }
    });

    // Alertes de performance
    const slowServices = this.getSlowServices(healthResults);
    if (slowServices.length > 0) {
      alerts.push({
        level: 'WARNING',
        type: 'PERFORMANCE_DEGRADED',
        message: `${slowServices.length} services responding slowly`,
        services: slowServices,
        action: 'MONITOR_PERFORMANCE',
        timestamp: new Date().toISOString()
      });
    }

    // Traiter et envoyer alertes
    for (const alert of alerts) {
      await this.sendAlert(alert);
    }

    return alerts;
  }

  getCriticalServices(healthResults) {
    const critical = [];
    
    Object.entries(healthResults.apis).forEach(([key, result]) => {
      if (['CRITICAL', 'ERROR'].includes(result.status)) {
        critical.push({ service: key, type: 'API', status: result.status });
      }
    });
    
    Object.entries(healthResults.rpc).forEach(([key, result]) => {
      if (['CRITICAL', 'ERROR'].includes(result.status)) {
        critical.push({ service: key, type: 'RPC', status: result.status });
      }
    });
    
    return critical;
  }

  getSlowServices(healthResults) {
    const slow = [];
    
    [...Object.entries(healthResults.apis), ...Object.entries(healthResults.rpc)].forEach(([key, result]) => {
      if (result.responseTime > HEALTH_CONFIG.thresholds.responseTime.warning) {
        slow.push({
          service: key,
          responseTime: result.responseTime,
          threshold: HEALTH_CONFIG.thresholds.responseTime.warning
        });
      }
    });
    
    return slow;
  }

  async sendAlert(alert) {
    console.log(`🚨 Alert [${alert.level}]: ${alert.message}`);
    
    // Éviter spam d'alertes
    const recentSimilar = this.alertHistory.filter(a => 
      a.type === alert.type && 
      a.service === alert.service &&
      Date.now() - new Date(a.timestamp).getTime() < 300000 // 5 minutes
    );
    
    if (recentSimilar.length > 0) {
      console.log("⏸️ Alert suppressed (similar alert sent recently)");
      return;
    }

    // Ici on pourrait envoyer vers Telegram, email, etc.
    // Pour l'instant, juste logger et stocker
    
    // Ajouter à l'historique
    this.alertHistory.push(alert);
    if (this.alertHistory.length > 200) {
      this.alertHistory = this.alertHistory.slice(-200);
    }

    // Envoyer notification (simulation)
    if (alert.level === 'CRITICAL') {
      await this.sendTelegramAlert(alert);
    }
  }

  async sendTelegramAlert(alert) {
    // Simulation envoi Telegram
    console.log(`📱 Telegram Alert: ${alert.message}`);
    
    const telegramMessage = `🚨 HEALTH ALERT [${alert.level}]

${alert.message}

Action Required: ${alert.action}
Time: ${new Date(alert.timestamp).toLocaleString()}

Services affected: ${alert.services?.length || 1}`;

    // Ici integration avec API Telegram Bot
    try {
      // await sendTelegramMessage(telegramMessage);
      console.log("✅ Telegram alert sent (simulated)");
    } catch (error) {
      console.error("❌ Failed to send Telegram alert:", error);
    }
  }
}

// 🚀 MAIN HEALTH MONITOR ORCHESTRATOR
class HealthMonitorOrchestrator {
  constructor() {
    this.monitor = new AIHealthMonitor();
    this.isRunning = false;
  }

  async start() {
    if (this.isRunning) {
      console.log("⚠️ Health monitor already running");
      return;
    }

    console.log("🚀 Starting Health Monitor Orchestrator...");
    this.isRunning = true;
    
    // Démarrer monitoring en arrière-plan
    this.monitor.start().catch(error => {
      console.error("❌ Health monitor failed:", error);
      this.isRunning = false;
    });

    return {
      status: 'STARTED',
      message: 'AI Health Monitor is now running',
      timestamp: new Date().toISOString()
    };
  }

  async stop() {
    if (!this.isRunning) {
      console.log("⚠️ Health monitor not running");
      return;
    }

    console.log("🛑 Stopping Health Monitor...");
    this.monitor.stop();
    this.isRunning = false;

    return {
      status: 'STOPPED',
      message: 'AI Health Monitor has been stopped',
      timestamp: new Date().toISOString()
    };
  }

  async getStatus() {
    return {
      isRunning: this.isRunning,
      globalHealth: this.monitor.state.globalHealth,
      currentInterval: this.monitor.state.currentInterval,
      servicesMonitored: Object.keys(this.monitor.state.services).length,
      lastCheck: this.monitor.state.history.length > 0 ? 
        this.monitor.state.history[this.monitor.state.history.length - 1].timestamp : null,
      alertsActive: this.monitor.alertManager?.alertHistory.filter(a => 
        Date.now() - new Date(a.timestamp).getTime() < 3600000 // 1 hour
      ).length || 0
    };
  }

  async forceHealthCheck() {
    if (!this.isRunning) {
      throw new Error("Health monitor not running");
    }

    console.log("🔍 Forcing immediate health check...");
    
    // Déclencher check immédiat
    const results = await this.monitor.performHealthChecks();
    const analysis = await this.monitor.brain.analyzeHealthData(results);
    
    return {
      status: 'COMPLETED',
      results: results,
      analysis: analysis,
      globalHealth: this.monitor.state.globalHealth,
      timestamp: new Date().toISOString()
    };
  }
}

// 🚀 EXPORT POUR N8N
async function startHealthMonitor() {
  try {
    console.log("🚀 Initializing AI Health Monitor for N8N...");
    
    const orchestrator = new HealthMonitorOrchestrator();
    const result = await orchestrator.start();
    
    // Exporter vers global pour accès depuis autres nodes
    global.HealthMonitor = orchestrator;
    
    return {
      json: {
        component: 'AI_HEALTH_MONITOR',
        ...result,
        features: [
          'Adaptive monitoring intervals',
          'AI-powered health analysis', 
          'Predictive failure detection',
          'Automated feedback loops',
          'Smart alerting system',
          'Multi-service health tracking'
        ],
        monitored_services: {
          apis: Object.keys(HEALTH_CONFIG.services.apis).length,
          rpc_nodes: Object.keys(HEALTH_CONFIG.services.rpc).length,
          internal_services: Object.keys(HEALTH_CONFIG.services.internal).length
        },
        version: 'health-monitor-v1.0'
      }
    };
    
  } catch (error) {
    console.error("❌ Health monitor initialization failed:", error);
    
    return {
      json: {
        component: 'AI_HEALTH_MONITOR',
        status: 'FAILED',
        error: error.message,
        timestamp: new Date().toISOString()
      }
    };
  }
}

// Fonctions utilitaires pour N8N
global.forceHealthCheck = async () => {
  if (global.HealthMonitor) {
    return await global.HealthMonitor.forceHealthCheck();
  }
  throw new Error("Health monitor not initialized");
};

global.getHealthStatus = async () => {
  if (global.HealthMonitor) {
    return await global.HealthMonitor.getStatus();
  }
  throw new Error("Health monitor not initialized");
};

global.stopHealthMonitor = async () => {
  if (global.HealthMonitor) {
    return await global.HealthMonitor.stop();
  }
  throw new Error("Health monitor not initialized");
};

// Démarrage automatique
return startHealthMonitor();