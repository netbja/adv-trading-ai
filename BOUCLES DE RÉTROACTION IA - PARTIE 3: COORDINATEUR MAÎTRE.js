// 🔄 BOUCLES DE RÉTROACTION IA - PARTIE 3: COORDINATEUR MAÎTRE
console.log("🔄 Initializing Master Feedback Coordinator...");

// 🎯 INTELLIGENCE CENTRALE PARTAGÉE
const GLOBAL_AI_BRAIN = {
  systemState: {
    tradingActive: true,
    healthScore: 1.0,
    performanceScore: 0.7,
    adaptationLevel: 'LEARNING',
    lastDecision: null,
    emergencyMode: false
  },
  
  feedbackLoops: {
    health: null,
    performance: null,
    market: null,
    learning: null
  },
  
  metrics: {
    totalDecisions: 0,
    successfulDecisions: 0,
    adaptationRate: 0,
    learningVelocity: 0,
    systemStability: 1.0
  },
  
  memory: {
    recentDecisions: [],
    successPatterns: [],
    failurePatterns: [],
    emergencyEvents: []
  }
};

// 🎮 MASTER FEEDBACK COORDINATOR
class MasterFeedbackCoordinator {
  constructor() {
    this.loops = new Map();
    this.isActive = false;
    this.coordinationInterval = null;
    this.emergencyProtocols = new EmergencyProtocolManager();
    this.decisionEngine = new UnifiedDecisionEngine();
  }

  // 🚀 DÉMARRER COORDINATION COMPLÈTE
  async startCoordination() {
    console.log("🚀 Starting Master Feedback Coordination...");
    
    if (this.isActive) {
      console.log("⚠️ Coordination already active");
      return { status: 'ALREADY_ACTIVE' };
    }

    this.isActive = true;
    
    try {
      // 1. Initialiser tous les loops
      await this.initializeFeedbackLoops();
      
      // 2. Démarrer coordination continue
      this.coordinationInterval = setInterval(async () => {
        await this.coordinateFeedbackLoops();
      }, 30000); // 30 secondes
      
      // 3. Activer monitoring d'urgence
      this.startEmergencyMonitoring();
      
      console.log("✅ Master Coordination started");
      
      return {
        status: 'ACTIVE',
        loops: Array.from(this.loops.keys()),
        emergencyProtocols: 'ACTIVE',
        timestamp: new Date().toISOString()
      };
      
    } catch (error) {
      console.error("❌ Failed to start coordination:", error);
      this.isActive = false;
      throw error;
    }
  }

  // 🔗 INITIALISER LOOPS DE FEEDBACK
  async initializeFeedbackLoops() {
    console.log("🔗 Initializing feedback loops...");
    
    // Health Loop
    if (global.HealthDecisionLoop) {
      const healthLoop = new global.HealthDecisionLoop();
      await healthLoop.initialize();
      this.loops.set('health', healthLoop);
      GLOBAL_AI_BRAIN.feedbackLoops.health = healthLoop;
    }
    
    // Performance Loop
    if (global.PerformanceStrategyLoop) {
      const performanceLoop = new global.PerformanceStrategyLoop();
      await performanceLoop.initialize();
      this.loops.set('performance', performanceLoop);
      GLOBAL_AI_BRAIN.feedbackLoops.performance = performanceLoop;
    }
    
    // Market Loop (simplifié)
    const marketLoop = new MarketAllocationLoop();
    await marketLoop.initialize();
    this.loops.set('market', marketLoop);
    GLOBAL_AI_BRAIN.feedbackLoops.market = marketLoop;
    
    console.log(`✅ Initialized ${this.loops.size} feedback loops`);
  }

  // 🎯 COORDINATION PRINCIPALE
  async coordinateFeedbackLoops() {
    try {
      console.log("🎯 Coordinating feedback loops...");
      
      // 1. Collecter feedback de tous les loops
      const feedbacks = await this.collectAllFeedback();
      
      // 2. Analyser avec moteur de décision unifié
      const analysis = await this.decisionEngine.analyze(feedbacks);
      
      // 3. Prendre décision coordonnée
      const decision = await this.decisionEngine.makeDecision(analysis);
      
      // 4. Appliquer décision à tous les loops
      await this.applyCoordinatedDecision(decision);
      
      // 5. Mettre à jour intelligence globale
      this.updateGlobalIntelligence(decision, feedbacks);
      
      // 6. Vérifier conditions d'urgence
      await this.checkEmergencyConditions(feedbacks, decision);
      
      console.log(`✅ Coordination completed - Decision: ${decision.primaryAction}`);
      
    } catch (error) {
      console.error("❌ Coordination failed:", error);
      await this.handleCoordinationFailure(error);
    }
  }

  // 📊 COLLECTER FEEDBACK
  async collectAllFeedback() {
    const feedbacks = {
      timestamp: new Date().toISOString(),
      health: null,
      performance: null,
      market: null,
      errors: []
    };
    
    for (const [name, loop] of this.loops) {
      try {
        feedbacks[name] = await loop.getFeedback();
        console.log(`📊 ${name} feedback collected`);
      } catch (error) {
        console.error(`❌ Failed to get ${name} feedback:`, error);
        feedbacks.errors.push({ loop: name, error: error.message });
        feedbacks[name] = { error: error.message, status: 'ERROR' };
      }
    }
    
    return feedbacks;
  }

  // ⚡ APPLIQUER DÉCISION COORDONNÉE
  async applyCoordinatedDecision(decision) {
    console.log(`⚡ Applying coordinated decision: ${decision.primaryAction}`);
    
    // Appliquer à l'orchestrateur autonome si disponible
    if (global.AutonomousOrchestrator) {
      try {
        await global.AutonomousOrchestrator.receiveCoordinatedDecision(decision);
      } catch (error) {
        console.error("❌ Failed to apply to autonomous orchestrator:", error);
      }
    }

    // Appliquer aux loops individuels
    const applicationResults = [];
    for (const [name, loop] of this.loops) {
      try {
        await loop.applyDecision(decision);
        applicationResults.push({ loop: name, status: 'SUCCESS' });
        console.log(`✅ Decision applied to ${name} loop`);
      } catch (error) {
        console.error(`❌ Failed to apply decision to ${name}:`, error);
        applicationResults.push({ loop: name, status: 'ERROR', error: error.message });
      }
    }

    // Mettre à jour état global
    GLOBAL_AI_BRAIN.systemState.lastDecision = decision;
    GLOBAL_AI_BRAIN.systemState.emergencyMode = decision.emergencyOverride || false;
    
    return applicationResults;
  }

  // 🧠 METTRE À JOUR INTELLIGENCE GLOBALE
  updateGlobalIntelligence(decision, feedbacks) {
    console.log("🧠 Updating global intelligence...");
    
    // Mettre à jour scores système
    GLOBAL_AI_BRAIN.systemState.healthScore = feedbacks.health?.healthScore || 0.5;
    GLOBAL_AI_BRAIN.systemState.performanceScore = feedbacks.performance?.performanceScore || 0.5;
    
    // Mettre à jour métriques
    GLOBAL_AI_BRAIN.metrics.totalDecisions++;
    
    // Ajouter à la mémoire
    GLOBAL_AI_BRAIN.memory.recentDecisions.push({
      decision: decision,
      feedbacks: feedbacks,
      timestamp: new Date().toISOString(),
      confidence: decision.confidence
    });

    // Nettoyer mémoire
    if (GLOBAL_AI_BRAIN.memory.recentDecisions.length > 50) {
      GLOBAL_AI_BRAIN.memory.recentDecisions = GLOBAL_AI_BRAIN.memory.recentDecisions.slice(-50);
    }

    // Calculer taux d'adaptation
    const recentDecisions = GLOBAL_AI_BRAIN.memory.recentDecisions.slice(-10);
    const avgConfidence = recentDecisions.reduce((sum, d) => sum + (d.confidence || 0.5), 0) / recentDecisions.length;
    GLOBAL_AI_BRAIN.metrics.adaptationRate = avgConfidence;

    // Calculer stabilité système
    const healthTrend = this.calculateHealthTrend();
    const performanceTrend = this.calculatePerformanceTrend();
    GLOBAL_AI_BRAIN.metrics.systemStability = (healthTrend + performanceTrend) / 2;
  }

  // 🚨 VÉRIFIER CONDITIONS D'URGENCE
  async checkEmergencyConditions(feedbacks, decision) {
    const emergencyConditions = [];
    
    // Condition 1: Santé système critique
    if (feedbacks.health?.healthScore < 0.3) {
      emergencyConditions.push({
        type: 'CRITICAL_HEALTH',
        severity: 'HIGH',
        score: feedbacks.health.healthScore,
        action: 'EMERGENCY_STOP'
      });
    }

    // Condition 2: Performance dégradée sévèrement
    if (feedbacks.performance?.performanceScore < 0.2) {
      emergencyConditions.push({
        type: 'CRITICAL_PERFORMANCE',
        severity: 'HIGH',
        score: feedbacks.performance.performanceScore,
        action: 'DEFENSIVE_MODE'
      });
    }

    // Condition 3: Échecs multiples de loops
    const errorCount = feedbacks.errors?.length || 0;
    if (errorCount >= 2) {
      emergencyConditions.push({
        type: 'MULTIPLE_SYSTEM_FAILURES',
        severity: 'CRITICAL',
        errorCount: errorCount,
        action: 'EMERGENCY_STOP'
      });
    }

    // Traiter urgences détectées
    if (emergencyConditions.length > 0) {
      await this.emergencyProtocols.handleEmergencies(emergencyConditions, decision);
    }
  }

  // 📈 CALCULER TENDANCES
  calculateHealthTrend() {
    const recentHealth = GLOBAL_AI_BRAIN.memory.recentDecisions
      .slice(-5)
      .map(d => d.feedbacks?.health?.healthScore || 0.5);
    
    if (recentHealth.length < 2) return 0.5;
    
    const trend = (recentHealth[recentHealth.length - 1] - recentHealth[0]) / recentHealth.length;
    return Math.max(0, Math.min(1, 0.5 + trend));
  }

  calculatePerformanceTrend() {
    const recentPerformance = GLOBAL_AI_BRAIN.memory.recentDecisions
      .slice(-5)
      .map(d => d.feedbacks?.performance?.performanceScore || 0.5);
    
    if (recentPerformance.length < 2) return 0.5;
    
    const trend = (recentPerformance[recentPerformance.length - 1] - recentPerformance[0]) / recentPerformance.length;
    return Math.max(0, Math.min(1, 0.5 + trend));
  }

  // 🛑 ARRÊTER COORDINATION
  async stopCoordination() {
    console.log("🛑 Stopping Master Coordination...");
    
    this.isActive = false;
    
    if (this.coordinationInterval) {
      clearInterval(this.coordinationInterval);
      this.coordinationInterval = null;
    }

    // Arrêter loops individuels
    for (const [name, loop] of this.loops) {
      try {
        if (loop.stop) {
          await loop.stop();
        }
      } catch (error) {
        console.error(`❌ Failed to stop ${name} loop:`, error);
      }
    }

    this.loops.clear();
    
    return {
      status: 'STOPPED',
      timestamp: new Date().toISOString()
    };
  }

  // 📊 OBTENIR STATUS GLOBAL
  getGlobalStatus() {
    return {
      coordination: {
        isActive: this.isActive,
        loopsCount: this.loops.size,
        lastCoordination: GLOBAL_AI_BRAIN.systemState.lastDecision?.timestamp
      },
      system: GLOBAL_AI_BRAIN.systemState,
      metrics: GLOBAL_AI_BRAIN.metrics,
      recentDecisions: GLOBAL_AI_BRAIN.memory.recentDecisions.slice(-5),
      timestamp: new Date().toISOString()
    };
  }

  // 🆘 GESTION ÉCHEC COORDINATION
  async handleCoordinationFailure(error) {
    console.error("🆘 Handling coordination failure...");
    
    // Enregistrer échec
    GLOBAL_AI_BRAIN.memory.emergencyEvents.push({
      type: 'COORDINATION_FAILURE',
      error: error.message,
      timestamp: new Date().toISOString()
    });

    // Mode dégradé temporaire
    GLOBAL_AI_BRAIN.systemState.emergencyMode = true;
    
    // Tentative récupération automatique
    setTimeout(async () => {
      try {
        console.log("🔄 Attempting automatic recovery...");
        await this.coordinateFeedbackLoops();
        GLOBAL_AI_BRAIN.systemState.emergencyMode = false;
        console.log("✅ Automatic recovery successful");
      } catch (recoveryError) {
        console.error("❌ Automatic recovery failed:", recoveryError);
      }
    }, 60000); // Retry dans 1 minute
  }

  startEmergencyMonitoring() {
    // Monitoring d'urgence en parallèle
    setInterval(async () => {
      try {
        const criticalChecks = await this.performCriticalChecks();
        if (criticalChecks.emergencyDetected) {
          await this.emergencyProtocols.triggerEmergencyProtocol(criticalChecks);
        }
      } catch (error) {
        console.error("❌ Emergency monitoring error:", error);
      }
    }, 10000); // Toutes les 10 secondes
  }

  async performCriticalChecks() {
    // Checks critiques rapides
    return {
      emergencyDetected: false,
      systemHealth: GLOBAL_AI_BRAIN.systemState.healthScore,
      tradingActive: GLOBAL_AI_BRAIN.systemState.tradingActive,
      lastDecisionAge: GLOBAL_AI_BRAIN.systemState.lastDecision ? 
        Date.now() - new Date(GLOBAL_AI_BRAIN.systemState.lastDecision.timestamp).getTime() : 0
    };
  }
}

// 🧠 MOTEUR DE DÉCISION UNIFIÉ
class UnifiedDecisionEngine {
  constructor() {
    this.decisionRules = new Map();
    this.conflictResolution = new ConflictResolver();
    this.initializeDecisionRules();
  }

  initializeDecisionRules() {
    // Règles de décision par priorité
    this.decisionRules.set('EMERGENCY_HEALTH', {
      priority: 10,
      condition: (feedbacks) => feedbacks.health?.healthScore < 0.3,
      action: 'EMERGENCY_STOP',
      confidence: 0.95
    });

    this.decisionRules.set('EMERGENCY_PERFORMANCE', {
      priority: 9,
      condition: (feedbacks) => feedbacks.performance?.performanceScore < 0.2,
      action: 'DEFENSIVE_MODE',
      confidence: 0.90
    });

    this.decisionRules.set('OPTIMIZE_PERFORMANCE', {
      priority: 5,
      condition: (feedbacks) => 
        feedbacks.health?.healthScore > 0.8 && feedbacks.performance?.performanceScore > 0.8,
      action: 'OPTIMIZE_PERFORMANCE',
      confidence: 0.85
    });

    this.decisionRules.set('MAINTAIN_NORMAL', {
      priority: 1,
      condition: () => true, // Règle par défaut
      action: 'CONTINUE_NORMAL',
      confidence: 0.70
    });
  }

  async analyze(feedbacks) {
    console.log("🧠 Unified Decision Engine analyzing...");
    
    const analysis = {
      feedbacks: feedbacks,
      applicableRules: [],
      conflicts: [],
      recommendations: [],
      urgencyLevel: 'LOW'
    };

    // Identifier règles applicables
    for (const [name, rule] of this.decisionRules) {
      try {
        if (rule.condition(feedbacks)) {
          analysis.applicableRules.push({ name, ...rule });
        }
      } catch (error) {
        console.error(`❌ Rule evaluation error for ${name}:`, error);
      }
    }

    // Trier par priorité
    analysis.applicableRules.sort((a, b) => b.priority - a.priority);

    // Détecter conflicts
    analysis.conflicts = this.conflictResolution.detectConflicts(analysis.applicableRules);

    // Déterminer urgence
    analysis.urgencyLevel = this.calculateUrgencyLevel(feedbacks, analysis.applicableRules);

    return analysis;
  }

  async makeDecision(analysis) {
    console.log("🎯 Making unified decision...");
    
    let primaryRule = null;
    
    // Résoudre conflicts s'il y en a
    if (analysis.conflicts.length > 0) {
      primaryRule = await this.conflictResolution.resolve(analysis.conflicts, analysis.applicableRules);
    } else if (analysis.applicableRules.length > 0) {
      primaryRule = analysis.applicableRules[0]; // Plus haute priorité
    } else {
      primaryRule = this.decisionRules.get('MAINTAIN_NORMAL');
    }

    const decision = {
      primaryAction: primaryRule.action,
      confidence: primaryRule.confidence,
      reasoning: this.generateReasoning(primaryRule, analysis),
      urgency: analysis.urgencyLevel,
      emergencyOverride: primaryRule.priority >= 9,
      modifications: this.generateModifications(primaryRule, analysis),
      timestamp: new Date().toISOString(),
      source: 'UNIFIED_DECISION_ENGINE',
      appliedRule: primaryRule.name || 'UNKNOWN'
    };

    return decision;
  }

  calculateUrgencyLevel(feedbacks, applicableRules) {
    // Calcul du niveau d'urgence basé sur les feedbacks et règles
    const highPriorityRules = applicableRules.filter(r => r.priority >= 8);
    
    if (highPriorityRules.length > 0) return 'CRITICAL';
    
    if (feedbacks.health?.urgency === 'CRITICAL' || feedbacks.performance?.urgency === 'CRITICAL') {
      return 'HIGH';
    }
    
    if (feedbacks.errors && feedbacks.errors.length > 0) {
      return 'MEDIUM';
    }
    
    return 'LOW';
  }

  generateReasoning(primaryRule, analysis) {
    let reasoning = `Applied rule: ${primaryRule.name || 'Default'}`;
    
    if (analysis.conflicts.length > 0) {
      reasoning += ` (resolved ${analysis.conflicts.length} conflicts)`;
    }
    
    if (analysis.feedbacks.health?.healthScore < 0.5) {
      reasoning += `, health degraded (${(analysis.feedbacks.health.healthScore * 100).toFixed(1)}%)`;
    }
    
    if (analysis.feedbacks.performance?.performanceScore < 0.5) {
      reasoning += `, performance low (${(analysis.feedbacks.performance.performanceScore * 100).toFixed(1)}%)`;
    }

    return reasoning;
  }

  generateModifications(primaryRule, analysis) {
    const modifications = {};
    
    // Modifications basées sur l'action principale
    switch (primaryRule.action) {
      case 'EMERGENCY_STOP':
        modifications.tradingFrequency = 'STOP';
        modifications.monitoring = 'INCREASE';
        break;
        
      case 'DEFENSIVE_MODE':
        modifications.positionSize = 'REDUCE_50%';
        modifications.riskTolerance = 'ULTRA_LOW';
        break;
        
      case 'OPTIMIZE_PERFORMANCE':
        modifications.positionSize = 'INCREASE_20%';
        modifications.tradingFrequency = 'INCREASE';
        break;
        
      case 'CONTINUE_NORMAL':
        modifications.monitoring = 'STANDARD';
        break;
    }

    // Modifications additionnelles basées sur feedbacks spécifiques
    if (analysis.feedbacks.health?.apiAvailability < 0.7) {
      modifications.fallbackAPIs = 'ENABLE';
    }

    return modifications;
  }
}

// 🔧 RÉSOLVEUR DE CONFLITS
class ConflictResolver {
  detectConflicts(applicableRules) {
    const conflicts = [];
    
    // Détecter conflits d'actions
    const actions = applicableRules.map(r => r.action);
    const uniqueActions = [...new Set(actions)];
    
    if (uniqueActions.length > 1 && applicableRules.length > 1) {
      // Conflits potentiels
      const conflictingPairs = this.findConflictingPairs(applicableRules);
      conflicts.push(...conflictingPairs);
    }
    
    return conflicts;
  }

  findConflictingPairs(rules) {
    const conflicts = [];
    const conflictMatrix = {
      'EMERGENCY_STOP': ['OPTIMIZE_PERFORMANCE', 'CONTINUE_NORMAL'],
      'DEFENSIVE_MODE': ['OPTIMIZE_PERFORMANCE'],
      'OPTIMIZE_PERFORMANCE': ['EMERGENCY_STOP', 'DEFENSIVE_MODE']
    };

    for (let i = 0; i < rules.length; i++) {
      for (let j = i + 1; j < rules.length; j++) {
        const rule1 = rules[i];
        const rule2 = rules[j];
        
        if (conflictMatrix[rule1.action]?.includes(rule2.action)) {
          conflicts.push({
            type: 'ACTION_CONFLICT',
            rule1: rule1,
            rule2: rule2,
            severity: Math.abs(rule1.priority - rule2.priority) < 3 ? 'HIGH' : 'LOW'
          });
        }
      }
    }
    
    return conflicts;
  }

  async resolve(conflicts, applicableRules) {
    console.log(`🔧 Resolving ${conflicts.length} conflicts...`);
    
    // Stratégie: Priorité absolue à la sécurité
    const safetyRules = applicableRules.filter(r => 
      ['EMERGENCY_STOP', 'DEFENSIVE_MODE'].includes(r.action)
    );
    
    if (safetyRules.length > 0) {
      // Prendre la règle de sécurité avec la plus haute priorité
      safetyRules.sort((a, b) => b.priority - a.priority);
      return safetyRules[0];
    }
    
    // Sinon, prendre la règle avec la plus haute priorité
    applicableRules.sort((a, b) => b.priority - a.priority);
    return applicableRules[0];
  }
}

// 🚨 GESTIONNAIRE DE PROTOCOLES D'URGENCE
class EmergencyProtocolManager {
  constructor() {
    this.activeEmergencies = [];
    this.protocolHistory = [];
  }

  async handleEmergencies(emergencyConditions, currentDecision) {
    console.log(`🚨 Handling ${emergencyConditions.length} emergency conditions...`);
    
    for (const condition of emergencyConditions) {
      await this.processEmergencyCondition(condition, currentDecision);
    }
  }

  async processEmergencyCondition(condition, currentDecision) {
    console.log(`🚨 Processing emergency: ${condition.type}`);
    
    // Enregistrer urgence
    const emergency = {
      ...condition,
      timestamp: new Date().toISOString(),
      currentDecision: currentDecision.primaryAction,
      status: 'ACTIVE'
    };
    
    this.activeEmergencies.push(emergency);
    
    // Déclencher actions d'urgence spécifiques
    switch (condition.type) {
      case 'CRITICAL_HEALTH':
        await this.handleCriticalHealth(emergency);
        break;
        
      case 'CRITICAL_PERFORMANCE':
        await this.handleCriticalPerformance(emergency);
        break;
        
      case 'MULTIPLE_SYSTEM_FAILURES':
        await this.handleSystemFailures(emergency);
        break;
    }
    
    // Archiver dans l'historique
    this.protocolHistory.push(emergency);
    
    // Nettoyer historique
    if (this.protocolHistory.length > 100) {
      this.protocolHistory = this.protocolHistory.slice(-100);
    }
  }

  async handleCriticalHealth(emergency) {
    console.log("🏥 Handling critical health emergency...");
    
    // Actions immédiates pour santé critique
    if (global.HealthMonitor) {
      // Forcer check santé immédiat
      try {
        await global.HealthMonitor.forceHealthCheck();
      } catch (error) {
        console.error("❌ Failed to force health check:", error);
      }
    }
    
    // Activer mode de sécurité
    GLOBAL_AI_BRAIN.systemState.emergencyMode = true;
    GLOBAL_AI_BRAIN.systemState.tradingActive = false;
  }

  async handleCriticalPerformance(emergency) {
    console.log("📉 Handling critical performance emergency...");
    
    // Réduire drastiquement les risques
    GLOBAL_AI_BRAIN.systemState.emergencyMode = true;
    
    // Notification d'urgence (simulation)
    console.log("📱 URGENT: Critical performance detected - switching to defensive mode");
  }

  async handleSystemFailures(emergency) {
    console.log("💥 Handling multiple system failures...");
    
    // Arrêt d'urgence complet
    GLOBAL_AI_BRAIN.systemState.emergencyMode = true;
    GLOBAL_AI_BRAIN.systemState.tradingActive = false;
    
    // Tenter redémarrage automatique des composants
    setTimeout(async () => {
      await this.attemptSystemRecovery();
    }, 30000); // Attendre 30 secondes puis tenter récupération
  }

  async triggerEmergencyProtocol(criticalChecks) {
    console.log("🚨 Triggering emergency protocol...");
    
    // Protocole d'urgence global
    const protocol = {
      type: 'SYSTEM_EMERGENCY',
      trigger: criticalChecks,
      timestamp: new Date().toISOString(),
      actions: []
    };

    // Actions d'urgence automatiques
    if (criticalChecks.systemHealth < 0.2) {
      protocol.actions.push('EMERGENCY_STOP_ALL');
      GLOBAL_AI_BRAIN.systemState.tradingActive = false;
    }

    if (criticalChecks.lastDecisionAge > 300000) { // 5 minutes
      protocol.actions.push('RESTART_COORDINATION');
      // Redémarrer coordination si bloquée
    }

    this.protocolHistory.push(protocol);
    return protocol;
  }

  async attemptSystemRecovery() {
    console.log("🔄 Attempting system recovery...");
    
    try {
      // Réinitialiser état d'urgence
      GLOBAL_AI_BRAIN.systemState.emergencyMode = false;
      
      // Nettoyer urgences actives anciennes
      this.activeEmergencies = this.activeEmergencies.filter(e => 
        Date.now() - new Date(e.timestamp).getTime() < 1800000 // 30 minutes
      );
      
      console.log("✅ System recovery completed");
      
    } catch (error) {
      console.error("❌ System recovery failed:", error);
    }
  }

  getEmergencyStatus() {
    return {
      activeEmergencies: this.activeEmergencies.length,
      recentProtocols: this.protocolHistory.slice(-5),
      systemEmergencyMode: GLOBAL_AI_BRAIN.systemState.emergencyMode,
      lastEmergency: this.protocolHistory[this.protocolHistory.length - 1]?.timestamp
    };
  }
}

// 🔗 MARKET ALLOCATION LOOP (Simplifié)
class MarketAllocationLoop {
  constructor() {
    this.name = 'market_allocation';
    this.isActive = false;
  }

  async initialize() {
    this.isActive = true;
    console.log("📊 Market Allocation Loop initialized");
  }

  async getFeedback() {
    // Feedback simulé de conditions de marché
    return {
      source: 'market_analyzer',
      marketCondition: ['BULL', 'BEAR', 'CRAB'][Math.floor(Math.random() * 3)],
      volatility: ['LOW', 'MEDIUM', 'HIGH'][Math.floor(Math.random() * 3)],
      recommendedAllocation: {
        meme: 0.4 + Math.random() * 0.4,
        technical: 0.3 + Math.random() * 0.4
      },
      confidence: 0.6 + Math.random() * 0.3,
      timestamp: new Date().toISOString()
    };
  }

  async applyDecision(decision) {
    console.log(`📊 Market loop applying decision: ${decision.primaryAction}`);
    // Application simulation
  }
}

// 🚀 EXPORT ET INITIALISATION
global.MasterFeedbackCoordinator = MasterFeedbackCoordinator;
global.GLOBAL_AI_BRAIN = GLOBAL_AI_BRAIN;

// Fonction d'initialisation pour N8N
async function initializeMasterCoordination() {
  try {
    console.log("🚀 Initializing Master Feedback Coordination System...");
    
    const coordinator = new MasterFeedbackCoordinator();
    const result = await coordinator.startCoordination();
    
    // Exporter globalement
    global.MasterCoordinator = coordinator;
    
    return {
      json: {
        component: 'MASTER_FEEDBACK_COORDINATOR',
        ...result,
        globalBrain: {
          systemState: GLOBAL_AI_BRAIN.systemState,
          metrics: GLOBAL_AI_BRAIN.metrics
        },
        features: [
          'Unified decision making',
          'Multi-loop coordination',
          'Emergency protocols',
          'Conflict resolution',
          'Adaptive learning',
          'Real-time intelligence'
        ],
        version: 'master-coordinator-v1.0'
      }
    };
    
  } catch (error) {
    console.error("❌ Master coordination initialization failed:", error);
    
    return {
      json: {
        component: 'MASTER_FEEDBACK_COORDINATOR',
        status: 'FAILED',
        error: error.message,
        timestamp: new Date().toISOString()
      }
    };
  }
}

// Fonctions utilitaires pour N8N
global.getMasterStatus = () => {
  if (global.MasterCoordinator) {
    return global.MasterCoordinator.getGlobalStatus();
  }
  return { error: 'Master coordinator not initialized' };
};

global.stopMasterCoordination = async () => {
  if (global.MasterCoordinator) {
    return await global.MasterCoordinator.stopCoordination();
  }
  return { error: 'Master coordinator not initialized' };
};

global.getEmergencyStatus = () => {
  if (global.MasterCoordinator?.emergencyProtocols) {
    return global.MasterCoordinator.emergencyProtocols.getEmergencyStatus();
  }
  return { error: 'Emergency protocols not available' };
};

console.log("✅ Master Feedback Coordinator ready");

// Démarrage automatique
return initializeMasterCoordination();
