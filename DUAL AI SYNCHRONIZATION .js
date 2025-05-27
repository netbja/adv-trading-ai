// 🔄 DUAL AI SYNCHRONIZATION - INTELLIGENCE PARTAGÉE
console.log("🔄 Initializing Dual AI Synchronization System...");

// 🧠 SHARED INTELLIGENCE STRUCTURE
const SHARED_INTELLIGENCE = {
  // Conditions de marché globales
  marketConditions: {
    trend: 'UNKNOWN',           // BULL/BEAR/CRAB
    volatility: 'UNKNOWN',      // HIGH/MEDIUM/LOW
    volume: 'UNKNOWN',          // HIGH/MEDIUM/LOW
    sentiment: 'UNKNOWN',       // BULLISH/BEARISH/NEUTRAL
    lastUpdate: null,
    confidence: 0
  },
  
  // Performance des stratégies
  strategyPerformance: {
    meme: {
      winRate: 0,
      avgROI: 0,
      avgHoldingTime: 0,
      totalTrades: 0,
      recentPerformance: [], // 10 derniers trades
      bestConditions: null,
      riskScore: 50
    },
    technical: {
      winRate: 0,
      avgROI: 0,
      avgHoldingTime: 0,
      totalTrades: 0,
      recentPerformance: [],
      bestConditions: null,
      riskScore: 50
    }
  },
  
  // Allocation dynamique
  allocation: {
    meme: 0.50,        // 50% par défaut
    technical: 0.50,   // 50% par défaut
    lastRebalance: null,
    reason: 'INITIAL_SETUP'
  },
  
  // Patterns identifiés
  learnings: {
    timePatterns: {},      // Meilleures heures pour chaque stratégie
    marketPatterns: {},    // Patterns selon conditions de marché
    crossStrategy: {},     // Insights partagés entre stratégies
    riskPatterns: {}       // Patterns de risque identifiés
  }
};

// 🔍 MARKET CONDITION DETECTOR
class MarketConditionDetector {
  constructor() {
    this.indicators = {};
    this.history = [];
  }

  // 📊 DÉTECTER CONDITIONS DE MARCHÉ
  async detectMarketConditions() {
    console.log("📊 Detecting global market conditions...");
    
    try {
      // Récupérer données de marché (simulation améliorée)
      const marketData = await this.fetchMarketData();
      
      // Analyser tendance
      const trend = this.analyzeTrend(marketData);
      
      // Analyser volatilité
      const volatility = this.analyzeVolatility(marketData);
      
      // Analyser volume
      const volume = this.analyzeVolume(marketData);
      
      // Analyser sentiment
      const sentiment = this.analyzeSentiment(marketData);
      
      // Calculer confidence
      const confidence = this.calculateConfidence(trend, volatility, volume, sentiment);
      
      const conditions = {
        trend: trend.direction,
        volatility: volatility.level,
        volume: volume.level,
        sentiment: sentiment.direction,
        confidence: confidence,
        timestamp: new Date().toISOString(),
        rawData: {
          trend: trend,
          volatility: volatility,
          volume: volume,
          sentiment: sentiment
        }
      };
      
      // Mettre à jour l'intelligence partagée
      SHARED_INTELLIGENCE.marketConditions = conditions;
      
      console.log("📊 Market conditions detected:", {
        trend: conditions.trend,
        volatility: conditions.volatility,
        confidence: conditions.confidence
      });
      
      return conditions;
      
    } catch (error) {
      console.error("❌ Market condition detection failed:", error);
      return SHARED_INTELLIGENCE.marketConditions;
    }
  }

  // 📈 ANALYSER TENDANCE
  analyzeTrend(marketData) {
    const prices = marketData.priceHistory || [];
    if (prices.length < 10) {
      return { direction: 'UNKNOWN', strength: 0, reason: 'Insufficient data' };
    }
    
    // Simple moving averages
    const short = this.calculateSMA(prices.slice(-5));
    const long = this.calculateSMA(prices.slice(-10));
    
    const trendStrength = Math.abs((short - long) / long) * 100;
    
    let direction = 'CRAB';
    if (short > long * 1.02) {
      direction = 'BULL';
    } else if (short < long * 0.98) {
      direction = 'BEAR';
    }
    
    return {
      direction: direction,
      strength: trendStrength,
      shortMA: short,
      longMA: long,
      reason: `${trendStrength.toFixed(1)}% trend strength`
    };
  }

  // 📊 ANALYSER VOLATILITÉ
  analyzeVolatility(marketData) {
    const prices = marketData.priceHistory || [];
    if (prices.length < 5) {
      return { level: 'UNKNOWN', value: 0 };
    }
    
    // Calculer volatilité (écart-type des returns)
    const returns = [];
    for (let i = 1; i < prices.length; i++) {
      returns.push((prices[i] - prices[i-1]) / prices[i-1]);
    }
    
    const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
    const volatility = Math.sqrt(variance);
    
    let level = 'LOW';
    if (volatility > 0.05) {
      level = 'HIGH';
    } else if (volatility > 0.02) {
      level = 'MEDIUM';
    }
    
    return {
      level: level,
      value: volatility,
      annualized: volatility * Math.sqrt(365),
      reason: `${(volatility * 100).toFixed(2)}% daily volatility`
    };
  }

  // 📊 ANALYSER VOLUME
  analyzeVolume(marketData) {
    const volumes = marketData.volumeHistory || [];
    if (volumes.length < 5) {
      return { level: 'UNKNOWN', ratio: 0 };
    }
    
    const currentVolume = volumes[volumes.length - 1];
    const avgVolume = volumes.slice(0, -1).reduce((sum, v) => sum + v, 0) / (volumes.length - 1);
    const ratio = currentVolume / avgVolume;
    
    let level = 'LOW';
    if (ratio > 2) {
      level = 'HIGH';
    } else if (ratio > 1.3) {
      level = 'MEDIUM';
    }
    
    return {
      level: level,
      ratio: ratio,
      current: currentVolume,
      average: avgVolume,
      reason: `${ratio.toFixed(1)}x average volume`
    };
  }

  // 📊 ANALYSER SENTIMENT
  analyzeSentiment(marketData) {
    // Simulation basée sur price action et volume
    const priceChange = marketData.priceChange24h || 0;
    const volumeRatio = (marketData.volumeHistory || [1, 1]).slice(-1)[0] / 
                       (marketData.volumeHistory || [1, 1]).slice(-2, -1)[0];
    
    let direction = 'NEUTRAL';
    let strength = Math.abs(priceChange);
    
    if (priceChange > 5 && volumeRatio > 1.5) {
      direction = 'BULLISH';
    } else if (priceChange < -5 && volumeRatio > 1.5) {
      direction = 'BEARISH';
    } else if (Math.abs(priceChange) < 2) {
      direction = 'NEUTRAL';
    }
    
    return {
      direction: direction,
      strength: strength,
      priceChange: priceChange,
      volumeRatio: volumeRatio,
      reason: `${priceChange.toFixed(1)}% price change with ${volumeRatio.toFixed(1)}x volume`
    };
  }

  // 🎯 CALCULER CONFIDENCE
  calculateConfidence(trend, volatility, volume, sentiment) {
    let confidence = 0;
    
    // Trend confidence
    if (trend.direction !== 'UNKNOWN') confidence += 25;
    if (trend.strength > 2) confidence += 15;
    
    // Volatility confidence
    if (volatility.level !== 'UNKNOWN') confidence += 20;
    
    // Volume confidence
    if (volume.level !== 'UNKNOWN') confidence += 20;
    if (volume.ratio > 1.2) confidence += 10;
    
    // Sentiment confidence
    if (sentiment.direction !== 'NEUTRAL') confidence += 10;
    
    return Math.min(100, confidence);
  }

  // 🔄 UTILITAIRES
  calculateSMA(prices) {
    return prices.reduce((sum, price) => sum + price, 0) / prices.length;
  }

  async fetchMarketData() {
    // Simulation de données de marché
    // À remplacer par vraies APIs (CoinGecko, etc.)
    const basePrice = 2500; // ETH price
    const priceHistory = [];
    const volumeHistory = [];
    
    for (let i = 0; i < 20; i++) {
      const change = (Math.random() - 0.5) * 0.1; // ±5% max
      const price = i === 0 ? basePrice : priceHistory[i-1] * (1 + change);
      priceHistory.push(price);
      
      const volume = 1000000000 * (0.8 + Math.random() * 0.4); // 800M-1.2B
      volumeHistory.push(volume);
    }
    
    return {
      priceHistory: priceHistory,
      volumeHistory: volumeHistory,
      priceChange24h: ((priceHistory[priceHistory.length - 1] - priceHistory[0]) / priceHistory[0]) * 100
    };
  }
}

// ⚖️ STRATEGY ALLOCATOR
class StrategyAllocator {
  constructor() {
    this.detector = new MarketConditionDetector();
    this.allocationHistory = [];
  }

  // 🎯 CALCULER ALLOCATION OPTIMALE
  async calculateOptimalAllocation() {
    console.log("⚖️ Calculating optimal strategy allocation...");
    
    // Détecter conditions actuelles
    const conditions = await this.detector.detectMarketConditions();
    
    // Analyser performance récente
    const performance = this.analyzeRecentPerformance();
    
    // Calculer nouvelle allocation
    const newAllocation = this.determineAllocation(conditions, performance);
    
    // Vérifier si rebalancing nécessaire
    const needsRebalancing = this.needsRebalancing(newAllocation);
    
    if (needsRebalancing) {
      console.log("⚖️ Rebalancing strategies:", {
        from: { meme: SHARED_INTELLIGENCE.allocation.meme, technical: SHARED_INTELLIGENCE.allocation.technical },
        to: newAllocation,
        reason: newAllocation.reason
      });
      
      SHARED_INTELLIGENCE.allocation = {
        ...newAllocation,
        lastRebalance: new Date().toISOString()
      };
      
      this.allocationHistory.push({
        allocation: newAllocation,
        conditions: conditions,
        performance: performance,
        timestamp: new Date().toISOString()
      });
    }
    
    return {
      allocation: SHARED_INTELLIGENCE.allocation,
      conditions: conditions,
      performance: performance,
      rebalanced: needsRebalancing,
      timestamp: new Date().toISOString()
    };
  }

  // 🎯 DÉTERMINER ALLOCATION
  determineAllocation(conditions, performance) {
    let memeAllocation = 0.50; // Base 50/50
    let technicalAllocation = 0.50;
    let reason = "BALANCED_DEFAULT";
    
    // Ajustements basés sur conditions de marché
    if (conditions.trend === 'BULL' && conditions.volatility === 'HIGH') {
      // Bull market + haute volatilité = favoriser meme scalping
      memeAllocation = 0.70;
      technicalAllocation = 0.30;
      reason = "BULL_HIGH_VOLATILITY";
      
    } else if (conditions.trend === 'BEAR' && conditions.volatility === 'LOW') {
      // Bear market + faible volatilité = favoriser technical
      memeAllocation = 0.30;
      technicalAllocation = 0.70;
      reason = "BEAR_LOW_VOLATILITY";
      
    } else if (conditions.trend === 'CRAB') {
      // Market sideways = équilibré
      memeAllocation = 0.50;
      technicalAllocation = 0.50;
      reason = "SIDEWAYS_BALANCED";
      
    } else if (conditions.volatility === 'HIGH') {
      // Haute volatilité générale = plus de meme
      memeAllocation = 0.65;
      technicalAllocation = 0.35;
      reason = "HIGH_VOLATILITY";
    }
    
    // Ajustements basés sur performance récente
    const memePerf = performance.meme.recentWinRate;
    const techPerf = performance.technical.recentWinRate;
    
    if (memePerf > techPerf + 0.2) {
      // Meme performe 20% mieux
      memeAllocation = Math.min(0.80, memeAllocation + 0.15);
      technicalAllocation = 1 - memeAllocation;
      reason += "_MEME_OUTPERFORMING";
      
    } else if (techPerf > memePerf + 0.2) {
      // Technical performe 20% mieux
      technicalAllocation = Math.min(0.80, technicalAllocation + 0.15);
      memeAllocation = 1 - technicalAllocation;
      reason += "_TECHNICAL_OUTPERFORMING";
    }
    
    return {
      meme: memeAllocation,
      technical: technicalAllocation,
      reason: reason,
      confidence: conditions.confidence
    };
  }

  // 📊 ANALYSER PERFORMANCE RÉCENTE
  analyzeRecentPerformance() {
    const memeStats = SHARED_INTELLIGENCE.strategyPerformance.meme;
    const techStats = SHARED_INTELLIGENCE.strategyPerformance.technical;
    
    return {
      meme: {
        recentWinRate: this.calculateRecentWinRate(memeStats.recentPerformance),
        avgROI: memeStats.avgROI,
        riskScore: memeStats.riskScore,
        totalTrades: memeStats.totalTrades
      },
      technical: {
        recentWinRate: this.calculateRecentWinRate(techStats.recentPerformance),
        avgROI: techStats.avgROI,
        riskScore: techStats.riskScore,
        totalTrades: techStats.totalTrades
      }
    };
  }

  // 📈 CALCULER WIN RATE RÉCENT
  calculateRecentWinRate(recentTrades) {
    if (!recentTrades || recentTrades.length === 0) return 0.5; // Neutral par défaut
    
    const winners = recentTrades.filter(trade => trade.pnl > 0).length;
    return winners / recentTrades.length;
  }

  // 🔄 VÉRIFIER BESOIN DE REBALANCING
  needsRebalancing(newAllocation) {
    const current = SHARED_INTELLIGENCE.allocation;
    const threshold = 0.1; // 10% de différence minimum
    
    return Math.abs(newAllocation.meme - current.meme) > threshold ||
           Math.abs(newAllocation.technical - current.technical) > threshold;
  }
}

// 🧠 PERFORMANCE TRACKER
class PerformanceTracker {
  constructor() {
    this.tradeHistory = [];
  }

  // 📊 ENREGISTRER TRADE
  recordTrade(trade, strategy) {
    console.log(`📊 Recording ${strategy} trade: ${trade.symbol}`);
    
    const tradeRecord = {
      ...trade,
      strategy: strategy,
      recordedAt: new Date().toISOString()
    };
    
    // Ajouter à l'historique
    this.tradeHistory.push(tradeRecord);
    
    // Mettre à jour performance strategy
    this.updateStrategyPerformance(trade, strategy);
    
    // Identifier patterns
    this.identifyPatterns(trade, strategy);
    
    return tradeRecord;
  }

  // 📈 METTRE À JOUR PERFORMANCE STRATÉGIE
  updateStrategyPerformance(trade, strategy) {
    const stats = SHARED_INTELLIGENCE.strategyPerformance[strategy];
    
    // Mettre à jour compteurs
    stats.totalTrades++;
    
    // Ajouter aux trades récents (max 10)
    stats.recentPerformance.push({
      symbol: trade.symbol,
      pnl: trade.pnl || 0,
      roi: trade.roi || 0,
      holdingTime: trade.holdingTime || 0,
      timestamp: trade.timestamp
    });
    
    // Garder seulement les 10 derniers
    if (stats.recentPerformance.length > 10) {
      stats.recentPerformance = stats.recentPerformance.slice(-10);
    }
    
    // Recalculer statistiques globales
    this.recalculateStats(strategy);
  }

  // 🔢 RECALCULER STATISTIQUES
  recalculateStats(strategy) {
    const stats = SHARED_INTELLIGENCE.strategyPerformance[strategy];
    const recent = stats.recentPerformance;
    
    if (recent.length === 0) return;
    
    // Win rate
    const winners = recent.filter(t => t.pnl > 0).length;
    stats.winRate = winners / recent.length;
    
    // ROI moyen
    stats.avgROI = recent.reduce((sum, t) => sum + (t.roi || 0), 0) / recent.length;
    
    // Temps de détention moyen
    stats.avgHoldingTime = recent.reduce((sum, t) => sum + (t.holdingTime || 0), 0) / recent.length;
    
    // Score de risque (basé sur volatilité des returns)
    const returns = recent.map(t => t.roi || 0);
    const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length;
    const variance = returns.reduce((sum, r) => sum + Math.pow(r - avgReturn, 2), 0) / returns.length;
    stats.riskScore = Math.min(100, Math.sqrt(variance) * 100);
  }

  // 🔍 IDENTIFIER PATTERNS
  identifyPatterns(trade, strategy) {
    // Pattern temporel
    const hour = new Date(trade.timestamp).getUTCHours();
    const timePattern = SHARED_INTELLIGENCE.learnings.timePatterns[strategy] || {};
    
    if (!timePattern[hour]) {
      timePattern[hour] = { trades: 0, wins: 0, totalROI: 0 };
    }
    
    timePattern[hour].trades++;
    if (trade.pnl > 0) timePattern[hour].wins++;
    timePattern[hour].totalROI += (trade.roi || 0);
    
    SHARED_INTELLIGENCE.learnings.timePatterns[strategy] = timePattern;
    
    // Pattern de marché
    const marketConditions = SHARED_INTELLIGENCE.marketConditions;
    const conditionKey = `${marketConditions.trend}_${marketConditions.volatility}`;
    
    const marketPattern = SHARED_INTELLIGENCE.learnings.marketPatterns[strategy] || {};
    if (!marketPattern[conditionKey]) {
      marketPattern[conditionKey] = { trades: 0, wins: 0, avgROI: 0 };
    }
    
    marketPattern[conditionKey].trades++;
    if (trade.pnl > 0) marketPattern[conditionKey].wins++;
    marketPattern[conditionKey].avgROI = 
      ((marketPattern[conditionKey].avgROI * (marketPattern[conditionKey].trades - 1)) + (trade.roi || 0)) 
      / marketPattern[conditionKey].trades;
    
    SHARED_INTELLIGENCE.learnings.marketPatterns[strategy] = marketPattern;
  }

  // 📊 GÉNÉRER RAPPORT PERFORMANCE
  generatePerformanceReport() {
    const memeStats = SHARED_INTELLIGENCE.strategyPerformance.meme;
    const techStats = SHARED_INTELLIGENCE.strategyPerformance.technical;
    
    return {
      overview: {
        totalTrades: memeStats.totalTrades + techStats.totalTrades,
        combinedWinRate: this.calculateCombinedWinRate(),
        bestStrategy: memeStats.avgROI > techStats.avgROI ? 'MEME' : 'TECHNICAL',
        riskAdjustedReturn: this.calculateRiskAdjustedReturn()
      },
      
      strategies: {
        meme: {
          ...memeStats,
          performance: this.gradePerformance(memeStats.winRate, memeStats.avgROI)
        },
        technical: {
          ...techStats,
          performance: this.gradePerformance(techStats.winRate, techStats.avgROI)
        }
      },
      
      allocation: SHARED_INTELLIGENCE.allocation,
      
      insights: this.generateInsights(),
      
      timestamp: new Date().toISOString()
    };
  }

  // 🎯 CALCULER MÉTRIQUES COMBINÉES
  calculateCombinedWinRate() {
    const meme = SHARED_INTELLIGENCE.strategyPerformance.meme;
    const tech = SHARED_INTELLIGENCE.strategyPerformance.technical;
    
    const totalTrades = meme.totalTrades + tech.totalTrades;
    if (totalTrades === 0) return 0;
    
    const totalWins = (meme.winRate * meme.totalTrades) + (tech.winRate * tech.totalTrades);
    return totalWins / totalTrades;
  }

  calculateRiskAdjustedReturn() {
    const meme = SHARED_INTELLIGENCE.strategyPerformance.meme;
    const tech = SHARED_INTELLIGENCE.strategyPerformance.technical;
    const allocation = SHARED_INTELLIGENCE.allocation;
    
    const memeContrib = (meme.avgROI / Math.max(1, meme.riskScore)) * allocation.meme;
    const techContrib = (tech.avgROI / Math.max(1, tech.riskScore)) * allocation.technical;
    
    return memeContrib + techContrib;
  }

  // 📊 GRADE PERFORMANCE
  gradePerformance(winRate, avgROI) {
    const score = (winRate * 60) + (Math.min(avgROI, 50) * 0.8); // Max 100 points
    
    if (score >= 80) return 'A+';
    if (score >= 70) return 'A';
    if (score >= 60) return 'B+';
    if (score >= 50) return 'B';
    if (score >= 40) return 'C+';
    return 'C';
  }

  // 💡 GÉNÉRER INSIGHTS
  generateInsights() {
    const insights = [];
    
    // Insight temporel
    const timePatterns = SHARED_INTELLIGENCE.learnings.timePatterns;
    const bestHours = this.findBestTradingHours(timePatterns);
    if (bestHours.length > 0) {
      insights.push({
        type: 'TIME_PATTERN',
        message: `Best trading hours: ${bestHours.join(', ')} UTC`,
        impact: 'HIGH'
      });
    }
    
    // Insight de marché
    const marketPatterns = SHARED_INTELLIGENCE.learnings.marketPatterns;
    const bestConditions = this.findBestMarketConditions(marketPatterns);
    if (bestConditions) {
      insights.push({
        type: 'MARKET_PATTERN',
        message: `Best market conditions: ${bestConditions}`,
        impact: 'HIGH'
      });
    }
    
    // Insight d'allocation
    const allocation = SHARED_INTELLIGENCE.allocation;
    if (allocation.meme > 0.7) {
      insights.push({
        type: 'ALLOCATION',
        message: 'Heavy focus on meme scalping due to market conditions',
        impact: 'MEDIUM'
      });
    } else if (allocation.technical > 0.7) {
      insights.push({
        type: 'ALLOCATION',
        message: 'Heavy focus on technical trading for stability',
        impact: 'MEDIUM'
      });
    }
    
    return insights;
  }

  // 🕐 TROUVER MEILLEURES HEURES
  findBestTradingHours(timePatterns) {
    const bestHours = [];
    
    Object.keys(timePatterns).forEach(strategy => {
      const patterns = timePatterns[strategy];
      Object.keys(patterns).forEach(hour => {
        const pattern = patterns[hour];
        if (pattern.trades >= 3 && pattern.wins / pattern.trades > 0.6) {
          bestHours.push(parseInt(hour));
        }
      });
    });
    
    return [...new Set(bestHours)].sort((a, b) => a - b);
  }

  // 📊 TROUVER MEILLEURES CONDITIONS
  findBestMarketConditions(marketPatterns) {
    let bestCondition = null;
    let bestScore = 0;
    
    Object.keys(marketPatterns).forEach(strategy => {
      const patterns = marketPatterns[strategy];
      Object.keys(patterns).forEach(condition => {
        const pattern = patterns[condition];
        if (pattern.trades >= 2) {
          const score = (pattern.wins / pattern.trades) * pattern.avgROI;
          if (score > bestScore) {
            bestScore = score;
            bestCondition = condition.replace('_', ' + ');
          }
        }
      });
    });
    
    return bestCondition;
  }
}

// 🎯 DUAL AI ORCHESTRATOR
class DualAIOrchestrator {
  constructor() {
    this.allocator = new StrategyAllocator();
    this.tracker = new PerformanceTracker();
    this.lastSync = null;
  }

  // 🔄 SYNCHRONISATION PRINCIPALE
  async synchronize() {
    console.log("🔄 Synchronizing Dual AI System...");
    
    try {
      // 1. Calculer allocation optimale
      const allocationResult = await this.allocator.calculateOptimalAllocation();
      
      // 2. Générer rapport de performance
      const performanceReport = this.tracker.generatePerformanceReport();
      
      // 3. Mettre à jour intelligence partagée
      this.updateSharedIntelligence(allocationResult, performanceReport);
      
      // 4. Générer recommandations
      const recommendations = this.generateRecommendations(allocationResult, performanceReport);
      
      const syncResult = {
        success: true,
        allocation: allocationResult.allocation,
        performance: performanceReport,
        marketConditions: allocationResult.conditions,
        recommendations: recommendations,
        sharedIntelligence: SHARED_INTELLIGENCE,
        lastSync: new Date().toISOString()
      };
      
      this.lastSync = new Date().toISOString();
      
      console.log("✅ Dual AI synchronization completed:", {
        memeAllocation: `${(allocationResult.allocation.meme * 100).toFixed(0)}%`,
        technicalAllocation: `${(allocationResult.allocation.technical * 100).toFixed(0)}%`,
        combinedWinRate: `${(performanceReport.overview.combinedWinRate * 100).toFixed(1)}%`,
        bestStrategy: performanceReport.overview.bestStrategy
      });
      
      return syncResult;
      
    } catch (error) {
      console.error("❌ Dual AI synchronization failed:", error);
      
      return {
        success: false,
        error: error.message,
        lastSync: this.lastSync,
        timestamp: new Date().toISOString()
      };
    }
  }

  // 🧠 METTRE À JOUR INTELLIGENCE PARTAGÉE
  updateSharedIntelligence(allocationResult, performanceReport) {
    // Mettre à jour conditions de marché
    SHARED_INTELLIGENCE.marketConditions = allocationResult.conditions;
    
    // Mettre à jour allocation
    SHARED_INTELLIGENCE.allocation = allocationResult.allocation;
    
    // Mettre à jour performance (déjà fait par le tracker)
  }

  // 💡 GÉNÉRER RECOMMANDATIONS
  generateRecommendations(allocationResult, performanceReport) {
    const recommendations = [];
    
    // Recommandation d'allocation
    if (allocationResult.rebalanced) {
      recommendations.push({
        type: 'ALLOCATION_CHANGE',
        priority: 'HIGH',
        message: `Strategy allocation rebalanced: ${(allocationResult.allocation.meme * 100).toFixed(0)}% meme, ${(allocationResult.allocation.technical * 100).toFixed(0)}% technical`,
        reason: allocationResult.allocation.reason,
        action: 'UPDATE_PORTFOLIO_WEIGHTS'
      });
    }
    
    // Recommandation de performance
    const combinedWinRate = performanceReport.overview.combinedWinRate;
    if (combinedWinRate < 0.4) {
      recommendations.push({
        type: 'PERFORMANCE_WARNING',
        priority: 'HIGH',
        message: `Low combined win rate: ${(combinedWinRate * 100).toFixed(1)}%`,
        reason: 'Risk management required',
        action: 'REDUCE_POSITION_SIZES'
      });
    } else if (combinedWinRate > 0.7) {
      recommendations.push({
        type: 'PERFORMANCE_EXCELLENT',
        priority: 'MEDIUM',
        message: `Excellent combined win rate: ${(combinedWinRate * 100).toFixed(1)}%`,
        reason: 'System performing well',
        action: 'CONSIDER_SCALING_UP'
      });
    }
    
    // Recommandation de timing
    const insights = performanceReport.insights;
    const timeInsight = insights.find(i => i.type === 'TIME_PATTERN');
    if (timeInsight) {
      recommendations.push({
        type: 'TIMING_OPTIMIZATION',
        priority: 'MEDIUM',
        message: timeInsight.message,
        reason: 'Pattern identified in trading hours',
        action: 'OPTIMIZE_SCHEDULE'
      });
    }
    
    return recommendations;
  }

  // 📊 ENREGISTRER TRADE DANS LE SYSTÈME
  recordTrade(trade, strategy) {
    return this.tracker.recordTrade(trade, strategy);
  }

  // 📈 OBTENIR STATUS ACTUEL
  getCurrentStatus() {
    return {
      allocation: SHARED_INTELLIGENCE.allocation,
      marketConditions: SHARED_INTELLIGENCE.marketConditions,
      performance: SHARED_INTELLIGENCE.strategyPerformance,
      lastSync: this.lastSync,
      uptime: this.lastSync ? Date.now() - new Date(this.lastSync).getTime() : 0
    };
  }
}

// 🚀 EXPORT POUR N8N
async function executeDualAISync() {
  try {
    console.log("🚀 Starting Dual AI Synchronization...");
    
    const orchestrator = new DualAIOrchestrator();
    const result = await orchestrator.synchronize();
    
    return {
      json: {
        systemType: 'DUAL_AI_SYNC',
        ...result,
        version: 'dual-ai-v1.0'
      }
    };
    
  } catch (error) {
    console.error("❌ Dual AI sync failed:", error);
    
    return {
      json: {
        systemType: 'DUAL_AI_SYNC',
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      }
    };
  }
}

// Exporter l'orchestrator pour utilisation dans d'autres nodes
global.DualAIOrchestrator = DualAIOrchestrator;

return executeDualAISync();