// 🔄 BOUCLES DE RÉTROACTION IA - PARTIE 1: HEALTH → DECISION LOOP
console.log("🔄 Initializing Health → Decision Feedback Loop...");

// 🏥 HEALTH DECISION LOOP
class HealthDecisionLoop {
  constructor() {
    this.name = 'health_decision';
    this.isActive = false;
    this.lastHealthData = null;
    this.decisionHistory = [];
    this.adaptationRules = new HealthAdaptationRules();
  }

  async initialize() {
    console.log("🏥 Initializing Health Decision Loop...");
    this.isActive = true;
    
    // Connecter au Health Monitor
    this.healthMonitor = global.HealthMonitor;
    if (!this.healthMonitor) {
      throw new Error("Health Monitor not available");
    }

    console.log("✅ Health Decision Loop initialized");
  }

  // 📊 OBTENIR FEEDBACK SANTÉ
  async getFeedback() {
    try {
      // Récupérer état santé actuel
      const healthStatus = await this.healthMonitor.getStatus();
      const healthFeedback = global.HEALTH_FEEDBACK;

      if (!healthFeedback) {
        return {
          status: 'NO_DATA',
          healthScore: 0.5,
          recommendation: { action: 'CONTINUE_NORMAL', confidence: 0.3 }
        };
      }

      // Analyser impact sur décisions trading
      const tradingImpact = this.analyzeTradingImpact(healthFeedback);
      
      // Générer recommandations adaptées
      const recommendations = this.generateHealthRecommendations(healthFeedback, tradingImpact);

      const feedback = {
        source: 'health_monitor',
        timestamp: new Date().toISOString(),
        healthScore: healthFeedback.healthScore,
        systemStatus: healthFeedback.systemStatus,
        urgency: healthFeedback.urgencyLevel,
        apiAvailability: healthFeedback.apiAvailability,
        rpcAvailability: healthFeedback.rpcAvailability,
        tradingImpact: tradingImpact,
        recommendation: recommendations.primary,
        alternativeActions: recommendations.alternatives,
        confidence: recommendations.confidence,
        reasoning: recommendations.reasoning
      };

      this.lastHealthData = feedback;
      return feedback;

    } catch (error) {
      console.error("❌ Health feedback error:", error);
      return {
        status: 'ERROR',
        error: error.message,
        healthScore: 0.2,
        recommendation: { action: 'PAUSE_TRADING', confidence: 0.8 }
      };
    }
  }

  // 🎯 ANALYSER IMPACT SUR TRADING
  analyzeTradingImpact(healthFeedback) {
    const impact = {
      severity: 'LOW',
      affectedComponents: [],
      tradingCapability: 1.0,
      recommendedAdjustments: []
    };

    // Impact APIs
    if (healthFeedback.apiAvailability < 0.5) {
      impact.severity = 'HIGH';
      impact.affectedComponents.push('API_SOURCES');
      impact.tradingCapability *= 0.3;
      impact.recommendedAdjustments.push('ENABLE_FALLBACK_APIS');
    } else if (healthFeedback.apiAvailability < 0.8) {
      impact.severity = 'MEDIUM';
      impact.affectedComponents.push('API_RELIABILITY');
      impact.tradingCapability *= 0.7;
      impact.recommendedAdjustments.push('REDUCE_API_FREQUENCY');
    }

    // Impact RPCs
    if (healthFeedback.rpcAvailability < 0.7) {
      impact.severity = 'HIGH';
      impact.affectedComponents.push('BLOCKCHAIN_ACCESS');
      impact.tradingCapability *= 0.5;
      impact.recommendedAdjustments.push('SWITCH_RPC_NODES');
    }

    // Impact système global
    if (healthFeedback.healthScore < 0.5) {
      impact.severity = 'CRITICAL';
      impact.affectedComponents.push('SYSTEM_STABILITY');
      impact.tradingCapability *= 0.2;
      impact.recommendedAdjustments.push('EMERGENCY_MODE');
    }

    return impact;
  }

  // 💡 GÉNÉRER RECOMMANDATIONS SANTÉ
  generateHealthRecommendations(healthFeedback, tradingImpact) {
    const recommendations = {
      primary: null,
      alternatives: [],
      confidence: 0.5,
      reasoning: ''
    };

    // Décisions basées sur impact trading
    if (tradingImpact.severity === 'CRITICAL') {
      recommendations.primary = {
        action: 'EMERGENCY_STOP',
        duration: '30min',
        conditions: ['health_score > 0.6', 'api_availability > 0.7']
      };
      recommendations.confidence = 0.95;
      recommendations.reasoning = 'Critical system health requires emergency stop';
      
    } else if (tradingImpact.severity === 'HIGH') {
      recommendations.primary = {
        action: 'PAUSE_TRADING',
        duration: '15min',
        conditions: ['health_score > 0.7', 'trading_capability > 0.6']
      };
      recommendations.confidence = 0.85;
      recommendations.reasoning = 'High impact on trading capability';
      
    } else if (tradingImpact.severity === 'MEDIUM') {
      recommendations.primary = {
        action: 'REDUCE_FREQUENCY',
        intensity: 0.5,
        duration: '10min'
      };
      recommendations.confidence = 0.75;
      recommendations.reasoning = 'Moderate health degradation detected';
      
    } else {
      recommendations.primary = {
        action: 'CONTINUE_NORMAL',
        optimizations: tradingImpact.recommendedAdjustments
      };
      recommendations.confidence = 0.70;
      recommendations.reasoning = 'System health stable';
    }

    // Alternatives basées sur composants affectés
    if (tradingImpact.affectedComponents.includes('API_SOURCES')) {
      recommendations.alternatives.push({
        action: 'FALLBACK_MODE',
        description: 'Switch to backup API sources',
        confidence: 0.8
      });
    }

    if (tradingImpact.affectedComponents.includes('BLOCKCHAIN_ACCESS')) {
      recommendations.alternatives.push({
        action: 'RPC_ROTATION',
        description: 'Rotate to healthy RPC nodes',
        confidence: 0.85
      });
    }

    return recommendations;
  }

  // ⚡ APPLIQUER DÉCISION
  async applyDecision(coordinatedDecision) {
    console.log(`⚡ Health Loop applying decision: ${coordinatedDecision.primaryAction}`);
    
    try {
      // Adapter monitoring selon décision
      if (coordinatedDecision.primaryAction === 'EMERGENCY_STOP') {
        // Augmenter fréquence monitoring en urgence
        if (this.healthMonitor.monitor) {
          this.healthMonitor.monitor.state.currentInterval = 5000; // 5 secondes
        }
      } else if (coordinatedDecision.primaryAction === 'OPTIMIZE_PERFORMANCE') {
        // Réduire monitoring si tout va bien
        if (this.healthMonitor.monitor) {
          this.healthMonitor.monitor.state.currentInterval = 120000; // 2 minutes
        }
      }

      // Enregistrer décision
      this.decisionHistory.push({
        decision: coordinatedDecision,
        healthContext: this.lastHealthData,
        timestamp: new Date().toISOString()
      });

      // Nettoyer historique
      if (this.decisionHistory.length > 50) {
        this.decisionHistory = this.decisionHistory.slice(-50);
      }

      console.log("✅ Health Loop decision applied");
      
    } catch (error) {
      console.error("❌ Failed to apply health decision:", error);
    }
  }

  // 📈 APPRENDRE DES RÉSULTATS
  async learnFromOutcome(outcome) {
    console.log("📈 Health Loop learning from outcome...");
    
    // Analyser si décision santé était correcte
    const lastDecision = this.decisionHistory[this.decisionHistory.length - 1];
    if (!lastDecision) return;

    const learningData = {
      healthContext: lastDecision.healthContext,
      decision: lastDecision.decision,
      outcome: outcome,
      wasCorrect: this.evaluateDecisionCorrectness(lastDecision, outcome),
      timestamp: new Date().toISOString()
    };

    // Mettre à jour règles d'adaptation
    await this.adaptationRules.updateRules(learningData);
    
    console.log(`📊 Health decision evaluation: ${learningData.wasCorrect ? 'CORRECT' : 'INCORRECT'}`);
  }

  evaluateDecisionCorrectness(decision, outcome) {
    // Logique d'évaluation de la justesse de la décision
    if (decision.decision.primaryAction === 'EMERGENCY_STOP') {
      // Si on a fait un emergency stop, c'était correct si le système s'est stabilisé
      return outcome.systemStabilized === true;
    } else if (decision.decision.primaryAction === 'PAUSE_TRADING') {
      // Si on a pausé, c'était correct si ça a évité des pertes
      return outcome.lossesAvoided === true || outcome.healthImproved === true;
    }
    
    // Par défaut, considérer correct si pas de dégradation majeure
    return outcome.majorDegradation !== true;
  }
}

// 🔧 RÈGLES D'ADAPTATION SANTÉ
class HealthAdaptationRules {
  constructor() {
    this.rules = new Map();
    this.learningRate = 0.1;
    this.initializeDefaultRules();
  }

  initializeDefaultRules() {
    // Règles par défaut basées sur score santé
    this.rules.set('critical_health', {
      condition: 'health_score < 0.3',
      action: 'EMERGENCY_STOP',
      confidence: 0.95,
      learned: false
    });

    this.rules.set('degraded_health', {
      condition: 'health_score < 0.6',
      action: 'PAUSE_TRADING',
      confidence: 0.80,
      learned: false
    });

    this.rules.set('api_failure', {
      condition: 'api_availability < 0.5',
      action: 'FALLBACK_MODE',
      confidence: 0.85,
      learned: false
    });
  }

  async updateRules(learningData) {
    console.log("🔧 Updating health adaptation rules...");
    
    const { healthContext, decision, outcome, wasCorrect } = learningData;
    
    // Identifier quelle règle a été utilisée
    const usedRule = this.identifyUsedRule(healthContext, decision);
    
    if (usedRule) {
      // Ajuster confiance selon résultat
      const adjustment = wasCorrect ? this.learningRate : -this.learningRate;
      usedRule.confidence = Math.max(0.1, Math.min(0.99, usedRule.confidence + adjustment));
      usedRule.learned = true;
      
      console.log(`📊 Rule '${usedRule.name}' confidence updated: ${usedRule.confidence.toFixed(2)}`);
    }

    // Créer nouvelles règles si pattern détecté
    if (wasCorrect && this.shouldCreateNewRule(learningData)) {
      await this.createNewRule(learningData);
    }
  }

  identifyUsedRule(healthContext, decision) {
    // Logique pour identifier quelle règle a été utilisée
    const healthScore = healthContext.healthScore;
    const action = decision.primaryAction;

    for (const [name, rule] of this.rules) {
      if (this.ruleMatches(rule, healthScore, action)) {
        return { name, ...rule };
      }
    }

    return null;
  }

  ruleMatches(rule, healthScore, action) {
    // Vérifier si la règle correspond au contexte et à l'action
    if (rule.condition.includes('health_score < 0.3') && healthScore < 0.3) {
      return rule.action === action;
    }
    if (rule.condition.includes('health_score < 0.6') && healthScore < 0.6) {
      return rule.action === action;
    }
    
    return false;
  }

  shouldCreateNewRule(learningData) {
    // Créer nouvelle règle si pattern récurrent détecté
    const similarCases = this.findSimilarCases(learningData);
    return similarCases.length >= 3; // Pattern détecté après 3 cas similaires
  }

  async createNewRule(learningData) {
    const { healthContext, decision } = learningData;
    
    const newRuleName = `learned_${Date.now()}`;
    const newRule = {
      condition: `health_score < ${healthContext.healthScore + 0.1}`,
      action: decision.primaryAction,
      confidence: 0.6,
      learned: true,
      createdFrom: learningData.timestamp
    };

    this.rules.set(newRuleName, newRule);
    console.log(`🆕 Created new health rule: ${newRuleName}`);
  }

  findSimilarCases(learningData) {
    // Logique pour trouver cas similaires dans l'historique
    // Simplifié pour l'exemple
    return [];
  }
}

// 🚀 EXPORT POUR UTILISATION
global.HealthDecisionLoop = HealthDecisionLoop;

console.log("✅ Health → Decision Feedback Loop ready");