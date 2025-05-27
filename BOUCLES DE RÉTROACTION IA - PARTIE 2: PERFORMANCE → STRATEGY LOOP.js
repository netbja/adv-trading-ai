// 🔄 BOUCLES DE RÉTROACTION IA - PARTIE 2: PERFORMANCE → STRATEGY LOOP
console.log("🔄 Initializing Performance → Strategy Feedback Loop...");

// 📈 PERFORMANCE STRATEGY LOOP
class PerformanceStrategyLoop {
  constructor() {
    this.name = 'performance_strategy';
    this.isActive = false;
    this.performanceHistory = [];
    this.strategyAdjustments = [];
    this.learningEngine = new PerformanceLearningEngine();
  }

  async initialize() {
    console.log("📈 Initializing Performance Strategy Loop...");
    this.isActive = true;
    
    // Charger historique performance existant
    await this.loadPerformanceHistory();
    
    console.log("✅ Performance Strategy Loop initialized");
  }

  // 📊 OBTENIR FEEDBACK PERFORMANCE  
  async getFeedback() {
    try {
      // Analyser performance récente
      const recentPerformance = await this.analyzeRecentPerformance();
      
      // Calculer métriques clés
      const metrics = this.calculatePerformanceMetrics(recentPerformance);
      
      // Identifier patterns de performance
      const patterns = await this.identifyPerformancePatterns();
      
      // Générer recommandations stratégiques
      const recommendations = await this.generateStrategyRecommendations(metrics, patterns);

      const feedback = {
        source: 'performance_analyzer',
        timestamp: new Date().toISOString(),
        performanceScore: metrics.overallScore,
        winRate: metrics.winRate,
        avgROI: metrics.avgROI,
        sharpeRatio: metrics.sharpeRatio,
        maxDrawdown: metrics.maxDrawdown,
        patterns: patterns,
        recommendation: recommendations.primary,
        alternativeStrategies: recommendations.alternatives,
        confidence: recommendations.confidence,
        reasoning: recommendations.reasoning,
        urgency: this.calculateUrgencyLevel(metrics)
      };

      // Enregistrer pour apprentissage
      this.performanceHistory.push({
        metrics: metrics,
        patterns: patterns,
        timestamp: new Date().toISOString()
      });

      return feedback;

    } catch (error) {
      console.error("❌ Performance feedback error:", error);
      return {
        status: 'ERROR',
        error: error.message,
        performanceScore: 0.3,
        recommendation: { action: 'DEFENSIVE_MODE', confidence: 0.7 }
      };
    }
  }

  // 📊 ANALYSER PERFORMANCE RÉCENTE
  async analyzeRecentPerformance() {
    console.log("📊 Analyzing recent performance...");
    
    // Simuler récupération données de performance
    // Dans la réalité, récupérer depuis PostgreSQL
    const recentTrades = this.getMockRecentTrades();
    
    const analysis = {
      totalTrades: recentTrades.length,
      winningTrades: recentTrades.filter(t => t.pnl > 0).length,
      losingTrades: recentTrades.filter(t => t.pnl < 0).length,
      totalPnL: recentTrades.reduce((sum, t) => sum + t.pnl, 0),
      avgHoldingTime: recentTrades.reduce((sum, t) => sum + t.holdingTime, 0) / recentTrades.length,
      bestTrade: recentTrades.reduce((best, t) => t.pnl > best.pnl ? t : best, { pnl: -Infinity }),
      worstTrade: recentTrades.reduce((worst, t) => t.pnl < worst.pnl ? t : worst, { pnl: Infinity }),
      strategies: this.groupTradesByStrategy(recentTrades)
    };

    return analysis;
  }

  // 🔢 CALCULER MÉTRIQUES PERFORMANCE
  calculatePerformanceMetrics(performance) {
    const { totalTrades, winningTrades, totalPnL, strategies } = performance;
    
    if (totalTrades === 0) {
      return {
        overallScore: 0.5,
        winRate: 0,
        avgROI: 0,
        sharpeRatio: 0,
        maxDrawdown: 0
      };
    }

    // Métriques de base
    const winRate = winningTrades / totalTrades;
    const avgROI = totalPnL / totalTrades;
    
    // Sharpe Ratio simplifié
    const returns = this.performanceHistory.slice(-10).map(h => h.metrics?.avgROI || 0);
    const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const returnStdDev = Math.sqrt(
      returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length
    );
    const sharpeRatio = returnStdDev > 0 ? avgReturn / returnStdDev : 0;

    // Max Drawdown
    const maxDrawdown = this.calculateMaxDrawdown();

    // Score global pondéré
    const overallScore = (
      winRate * 0.3 +
      Math.max(0, Math.min(1, (avgROI + 50) / 100)) * 0.3 +
      Math.max(0, Math.min(1, (sharpeRatio + 2) / 4)) * 0.2 +
      Math.max(0, Math.min(1, (50 - Math.abs(maxDrawdown)) / 50)) * 0.2
    );

    return {
      overallScore: Math.max(0, Math.min(1, overallScore)),
      winRate,
      avgROI,
      sharpeRatio,
      maxDrawdown,
      totalTrades,
      strategiesPerformance: this.analyzeStrategiesPerformance(strategies)
    };
  }

  // 🔍 IDENTIFIER PATTERNS DE PERFORMANCE
  async identifyPerformancePatterns() {
    console.log("🔍 Identifying performance patterns...");
    
    const patterns = [];
    
    if (this.performanceHistory.length < 5) {
      return patterns;
    }

    // Pattern 1: Tendance performance
    const recentScores = this.performanceHistory.slice(-5).map(h => h.metrics?.overallScore || 0.5);
    const trend = this.calculateTrend(recentScores);
    
    if (trend.direction === 'DECLINING' && trend.strength > 0.3) {
      patterns.push({
        type: 'DECLINING_PERFORMANCE',
        strength: trend.strength,
        duration: '5 periods',
        impact: 'NEGATIVE',
        recommendation: 'STRATEGY_ADJUSTMENT_NEEDED'
      });
    } else if (trend.direction === 'IMPROVING' && trend.strength > 0.3) {
      patterns.push({
        type: 'IMPROVING_PERFORMANCE',
        strength: trend.strength,
        duration: '5 periods',
        impact: 'POSITIVE',
        recommendation: 'OPTIMIZE_CURRENT_STRATEGY'
      });
    }

    // Pattern 2: Volatilité win rate
    const recentWinRates = this.performanceHistory.slice(-10).map(h => h.metrics?.winRate || 0.5);
    const winRateVolatility = this.calculateVolatility(recentWinRates);
    
    if (winRateVolatility > 0.3) {
      patterns.push({
        type: 'UNSTABLE_WIN_RATE',
        volatility: winRateVolatility,
        impact: 'NEGATIVE',
        recommendation: 'STABILIZE_STRATEGY'
      });
    }

    // Pattern 3: Performance par stratégie
    const strategyPattern = await this.analyzeStrategyPatterns();
    if (strategyPattern) {
      patterns.push(strategyPattern);
    }

    return patterns;
  }

  // 💡 GÉNÉRER RECOMMANDATIONS STRATÉGIQUES
  async generateStrategyRecommendations(metrics, patterns) {
    console.log("💡 Generating strategy recommendations...");
    
    const recommendations = {
      primary: null,
      alternatives: [],
      confidence: 0.5,
      reasoning: ''
    };

    // Recommandations basées sur score global
    if (metrics.overallScore < 0.3) {
      recommendations.primary = {
        action: 'EMERGENCY_STRATEGY_CHANGE',
        newStrategy: 'DEFENSIVE_MODE',
        adjustments: {
          positionSize: 'REDUCE_BY_50%',
          frequency: 'REDUCE_BY_60%',
          riskTolerance: 'ULTRA_CONSERVATIVE'
        }
      };
      recommendations.confidence = 0.90;
      recommendations.reasoning = 'Critical performance degradation requires immediate defensive strategy';
      
    } else if (metrics.overallScore < 0.5) {
      recommendations.primary = {
        action: 'STRATEGY_ADJUSTMENT',
        adjustments: {
          positionSize: 'REDUCE_BY_25%',
          frequency: 'REDUCE_BY_30%',
          stopLoss: 'TIGHTEN_BY_20%'
        }
      };
      recommendations.confidence = 0.80;
      recommendations.reasoning = 'Below-average performance requires risk reduction';
      
    } else if (metrics.overallScore > 0.8) {
      recommendations.primary = {
        action: 'OPTIMIZE_PERFORMANCE',
        adjustments: {
          positionSize: 'INCREASE_BY_15%',
          frequency: 'INCREASE_BY_20%',
          targets: 'EXTEND_BY_10%'
        }
      };
      recommendations.confidence = 0.85;
      recommendations.reasoning = 'Excellent performance allows for optimization';
      
    } else {
      recommendations.primary = {
        action: 'MAINTAIN_STRATEGY',
        adjustments: {
          monitoring: 'INCREASE_PRECISION',
          finetuning: 'MINOR_OPTIMIZATIONS'
        }
      };
      recommendations.confidence = 0.70;
      recommendations.reasoning = 'Stable performance suggests current strategy is working';
    }

    // Recommandations basées sur patterns
    const decliningPattern = patterns.find(p => p.type === 'DECLINING_PERFORMANCE');
    if (decliningPattern && decliningPattern.strength > 0.5) {
      recommendations.alternatives.push({
        action: 'STRATEGY_ROTATION',
        description: 'Rotate to alternative strategy temporarily',
        confidence: 0.75
      });
    }

    const unstablePattern = patterns.find(p => p.type === 'UNSTABLE_WIN_RATE');
    if (unstablePattern) {
      recommendations.alternatives.push({
        action: 'STABILITY_FOCUS',
        description: 'Focus on consistent smaller wins',
        confidence: 0.80
      });
    }

    // Recommandations par stratégie
    if (metrics.strategiesPerformance) {
      const bestStrategy = Object.entries(metrics.strategiesPerformance)
        .sort(([,a], [,b]) => b.score - a.score)[0];
      
      if (bestStrategy && bestStrategy[1].score > metrics.overallScore + 0.2) {
        recommendations.alternatives.push({
          action: 'FOCUS_ON_BEST_STRATEGY',
          strategy: bestStrategy[0],
          description: `Focus on ${bestStrategy[0]} strategy (score: ${bestStrategy[1].score.toFixed(2)})`,
          confidence: 0.85
        });
      }
    }

    return recommendations;
  }

  // ⚡ APPLIQUER DÉCISION
  async applyDecision(coordinatedDecision) {
    console.log(`⚡ Performance Loop applying decision: ${coordinatedDecision.primaryAction}`);
    
    try {
      // Ajuster stratégie selon décision coordonnée
      const strategyAdjustment = {
        timestamp: new Date().toISOString(),
        originalStrategy: this.getCurrentStrategy(),
        coordinatedDecision: coordinatedDecision,
        appliedAdjustments: {}
      };

      // Appliquer modifications de performance
      if (coordinatedDecision.modifications) {
        if (coordinatedDecision.modifications.tradingFrequency === 'INCREASE') {
          strategyAdjustment.appliedAdjustments.frequency = 'INCREASED_BY_20%';
        } else if (coordinatedDecision.modifications.tradingFrequency === 'DECREASE') {
          strategyAdjustment.appliedAdjustments.frequency = 'DECREASED_BY_30%';
        }

        if (coordinatedDecision.modifications.positionSizing === 'OPTIMIZE') {
          strategyAdjustment.appliedAdjustments.positionSize = 'OPTIMIZED';
        }
      }

      // Gérer actions spécifiques
      switch (coordinatedDecision.primaryAction) {
        case 'EMERGENCY_STOP':
          strategyAdjustment.appliedAdjustments.mode = 'EMERGENCY_DEFENSIVE';
          break;
        case 'OPTIMIZE_PERFORMANCE':
          strategyAdjustment.appliedAdjustments.mode = 'PERFORMANCE_OPTIMIZED';
          break;
        case 'PAUSE_TRADING':
          strategyAdjustment.appliedAdjustments.mode = 'PAUSED';
          break;
      }

      // Enregistrer ajustement
      this.strategyAdjustments.push(strategyAdjustment);
      
      // Nettoyer historique
      if (this.strategyAdjustments.length > 100) {
        this.strategyAdjustments = this.strategyAdjustments.slice(-100);
      }

      console.log("✅ Performance strategy adjustments applied");
      
    } catch (error) {
      console.error("❌ Failed to apply performance decision:", error);
    }
  }

  // 📈 APPRENDRE DES RÉSULTATS
  async learnFromOutcome(outcome) {
    console.log("📈 Performance Loop learning from outcome...");
    
    // Analyser efficacité des ajustements stratégiques
    const lastAdjustment = this.strategyAdjustments[this.strategyAdjustments.length - 1];
    if (!lastAdjustment) return;

    const learningData = {
      strategyContext: lastAdjustment,
      outcome: outcome,
      effectivenessScore: this.calculateAdjustmentEffectiveness(lastAdjustment, outcome),
      timestamp: new Date().toISOString()
    };

    // Mettre à jour moteur d'apprentissage
    await this.learningEngine.updateFromOutcome(learningData);
    
    console.log(`📊 Strategy adjustment effectiveness: ${learningData.effectivenessScore.toFixed(2)}`);
  }

  // 🔧 UTILITAIRES
  calculateUrgencyLevel(metrics) {
    if (metrics.overallScore < 0.3) return 'CRITICAL';
    if (metrics.overallScore < 0.5) return 'HIGH';
    if (metrics.winRate < 0.4) return 'MEDIUM';
    return 'LOW';
  }

  getMockRecentTrades() {
    // Simulation de trades récents
    const trades = [];
    for (let i = 0; i < 20; i++) {
      trades.push({
        id: `trade_${i}`,
        symbol: `TOKEN${i % 5}`,
        strategy: i % 2 === 0 ? 'MEME' : 'TECHNICAL',
        pnl: (Math.random() - 0.4) * 100, // Bias légèrement négatif
        holdingTime: Math.random() * 240, // 0-4h
        timestamp: new Date(Date.now() - i * 3600000).toISOString()
      });
    }
    return trades;
  }

  groupTradesByStrategy(trades) {
    return trades.reduce((groups, trade) => {
      const strategy = trade.strategy;
      if (!groups[strategy]) {
        groups[strategy] = [];
      }
      groups[strategy].push(trade);
      return groups;
    }, {});
  }

  analyzeStrategiesPerformance(strategies) {
    const analysis = {};
    
    Object.entries(strategies).forEach(([strategy, trades]) => {
      const winners = trades.filter(t => t.pnl > 0).length;
      const totalPnL = trades.reduce((sum, t) => sum + t.pnl, 0);
      const avgPnL = totalPnL / trades.length;
      const winRate = winners / trades.length;
      
      analysis[strategy] = {
        trades: trades.length,
        winRate: winRate,
        avgPnL: avgPnL,
        totalPnL: totalPnL,
        score: (winRate * 0.6) + (Math.max(0, Math.min(1, (avgPnL + 20) / 40)) * 0.4)
      };
    });
    
    return analysis;
  }

  calculateTrend(values) {
    if (values.length < 2) return { direction: 'STABLE', strength: 0 };
    
    let increases = 0;
    let decreases = 0;
    
    for (let i = 1; i < values.length; i++) {
      if (values[i] > values[i-1]) increases++;
      else if (values[i] < values[i-1]) decreases++;
    }
    
    const totalChanges = increases + decreases;
    if (totalChanges === 0) return { direction: 'STABLE', strength: 0 };
    
    const strength = Math.abs(increases - decreases) / totalChanges;
    const direction = increases > decreases ? 'IMPROVING' : 'DECLINING';
    
    return { direction, strength };
  }

  calculateVolatility(values) {
    if (values.length < 2) return 0;
    
    const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
    const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length;
    
    return Math.sqrt(variance);
  }

  calculateMaxDrawdown() {
    // Simulation du calcul de drawdown maximum
    return Math.random() * 30; // 0-30% drawdown
  }

  async analyzeStrategyPatterns() {
    // Analyser patterns spécifiques par stratégie
    if (this.performanceHistory.length < 3) return null;
    
    const recentHistory = this.performanceHistory.slice(-3);
    const memePerformance = recentHistory.map(h => h.metrics?.strategiesPerformance?.MEME?.score || 0.5);
    const techPerformance = recentHistory.map(h => h.metrics?.strategiesPerformance?.TECHNICAL?.score || 0.5);
    
    const memeTrend = this.calculateTrend(memePerformance);
    const techTrend = this.calculateTrend(techPerformance);
    
    if (memeTrend.direction === 'IMPROVING' && techTrend.direction === 'DECLINING') {
      return {
        type: 'STRATEGY_DIVERGENCE',
        winner: 'MEME',
        loser: 'TECHNICAL',
        strength: (memeTrend.strength + techTrend.strength) / 2,
        recommendation: 'SHIFT_TO_MEME_STRATEGY'
      };
    } else if (techTrend.direction === 'IMPROVING' && memeTrend.direction === 'DECLINING') {
      return {
        type: 'STRATEGY_DIVERGENCE',
        winner: 'TECHNICAL',
        loser: 'MEME',
        strength: (memeTrend.strength + techTrend.strength) / 2,
        recommendation: 'SHIFT_TO_TECHNICAL_STRATEGY'
      };
    }
    
    return null;
  }

  getCurrentStrategy() {
    // Retourner stratégie actuelle (simulation)
    return {
      primary: 'DUAL_AI',
      allocation: { meme: 0.6, technical: 0.4 },
      riskLevel: 'MODERATE',
      positionSize: 'STANDARD'
    };
  }

  calculateAdjustmentEffectiveness(adjustment, outcome) {
    // Calculer efficacité de l'ajustement stratégique
    let effectiveness = 0.5; // Base neutre
    
    // Si ajustement défensif et résultat protecteur
    if (adjustment.appliedAdjustments.mode === 'EMERGENCY_DEFENSIVE' && outcome.lossesAvoided) {
      effectiveness = 0.9;
    }
    
    // Si optimisation et amélioration performance
    if (adjustment.appliedAdjustments.mode === 'PERFORMANCE_OPTIMIZED' && outcome.performanceImproved) {
      effectiveness = 0.8;
    }
    
    // Pénaliser si mauvais timing
    if (outcome.majorLosses && !adjustment.appliedAdjustments.mode?.includes('DEFENSIVE')) {
      effectiveness = 0.2;
    }
    
    return effectiveness;
  }

  async loadPerformanceHistory() {
    // Charger historique depuis base de données
    // Simulation pour l'instant
    console.log("📚 Loading performance history...");
    
    // Générer historique simulé
    for (let i = 0; i < 10; i++) {
      this.performanceHistory.push({
        metrics: {
          overallScore: 0.4 + Math.random() * 0.4,
          winRate: 0.3 + Math.random() * 0.4,
          avgROI: (Math.random() - 0.4) * 50
        },
        timestamp: new Date(Date.now() - i * 3600000).toISOString()
      });
    }
  }
}

// 🧠 PERFORMANCE LEARNING ENGINE
class PerformanceLearningEngine {
  constructor() {
    this.learningDatabase = [];
    this.patterns = new Map();
    this.adjustmentRules = new Map();
    this.learningRate = 0.15;
  }

  async updateFromOutcome(learningData) {
    console.log("🧠 Performance learning engine updating...");
    
    // Ajouter à la base d'apprentissage
    this.learningDatabase.push(learningData);
    
    // Limiter taille base
    if (this.learningDatabase.length > 200) {
      this.learningDatabase = this.learningDatabase.slice(-200);
    }

    // Identifier nouveaux patterns
    await this.identifyNewPatterns();
    
    // Mettre à jour règles d'ajustement
    await this.updateAdjustmentRules(learningData);
    
    console.log(`📊 Learning database size: ${this.learningDatabase.length}`);
  }

  async identifyNewPatterns() {
    // Analyser base pour identifier patterns récurrents
    const recentData = this.learningDatabase.slice(-20);
    
    // Pattern: Ajustements défensifs efficaces
    const defensiveAdjustments = recentData.filter(d => 
      d.strategyContext.appliedAdjustments.mode?.includes('DEFENSIVE')
    );
    
    if (defensiveAdjustments.length >= 3) {
      const avgEffectiveness = defensiveAdjustments.reduce((sum, d) => 
        sum + d.effectivenessScore, 0) / defensiveAdjustments.length;
      
      this.patterns.set('DEFENSIVE_EFFECTIVENESS', {
        strength: avgEffectiveness,
        sampleSize: defensiveAdjustments.length,
        recommendation: avgEffectiveness > 0.7 ? 'TRUST_DEFENSIVE' : 'IMPROVE_DEFENSIVE'
      });
    }

    // Pattern: Timing d'optimisation
    const optimizations = recentData.filter(d => 
      d.strategyContext.appliedAdjustments.mode?.includes('OPTIMIZED')
    );
    
    if (optimizations.length >= 3) {
      const avgEffectiveness = optimizations.reduce((sum, d) => 
        sum + d.effectivenessScore, 0) / optimizations.length;
      
      this.patterns.set('OPTIMIZATION_TIMING', {
        strength: avgEffectiveness,
        sampleSize: optimizations.length,
        recommendation: avgEffectiveness > 0.6 ? 'AGGRESSIVE_OPTIMIZATION' : 'CONSERVATIVE_OPTIMIZATION'
      });
    }
  }

  async updateAdjustmentRules(learningData) {
    const { strategyContext, effectivenessScore } = learningData;
    
    // Identifier type d'ajustement
    const adjustmentType = this.categorizeAdjustment(strategyContext);
    
    // Mettre à jour règle existante ou créer nouvelle
    if (this.adjustmentRules.has(adjustmentType)) {
      const rule = this.adjustmentRules.get(adjustmentType);
      
      // Mise à jour pondérée
      rule.effectiveness = (rule.effectiveness * rule.samples + effectivenessScore) / (rule.samples + 1);
      rule.samples++;
      rule.confidence = Math.min(0.95, rule.confidence + this.learningRate);
      
    } else {
      // Nouvelle règle
      this.adjustmentRules.set(adjustmentType, {
        effectiveness: effectivenessScore,
        samples: 1,
        confidence: 0.3,
        created: new Date().toISOString()
      });
    }
  }

  categorizeAdjustment(strategyContext) {
    const adjustments = strategyContext.appliedAdjustments;
    
    if (adjustments.mode?.includes('EMERGENCY')) {
      return 'EMERGENCY_RESPONSE';
    } else if (adjustments.mode?.includes('DEFENSIVE')) {
      return 'DEFENSIVE_ADJUSTMENT';
    } else if (adjustments.mode?.includes('OPTIMIZED')) {
      return 'PERFORMANCE_OPTIMIZATION';
    } else if (adjustments.frequency) {
      return 'FREQUENCY_ADJUSTMENT';
    } else if (adjustments.positionSize) {
      return 'POSITION_SIZING';
    }
    
    return 'GENERAL_ADJUSTMENT';
  }

  getRecommendation(currentContext) {
    // Fournir recommandation basée sur apprentissage
    const relevantPatterns = Array.from(this.patterns.entries())
      .filter(([name, pattern]) => pattern.strength > 0.6);
    
    const relevantRules = Array.from(this.adjustmentRules.entries())
      .filter(([type, rule]) => rule.confidence > 0.5)
      .sort(([,a], [,b]) => b.effectiveness - a.effectiveness);

    return {
      suggestedAdjustment: relevantRules[0]?.[0] || 'MAINTAIN_CURRENT',
      confidence: relevantRules[0]?.[1]?.confidence || 0.5,
      supportingPatterns: relevantPatterns.map(([name, pattern]) => ({
        name, recommendation: pattern.recommendation
      }))
    };
  }
}

// 🚀 EXPORT POUR UTILISATION
global.PerformanceStrategyLoop = PerformanceStrategyLoop;

console.log("✅ Performance → Strategy Feedback Loop ready");
