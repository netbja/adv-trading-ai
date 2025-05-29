#!/usr/bin/env python3
"""
🔄 PAGES DÉTAILLÉES DES WORKFLOWS
Vues temps réel pour crypto, meme et forex avec métriques avancées
"""

from typing import Dict, Any

def get_crypto_workflow_page() -> str:
    """Page détaillée du workflow crypto avec onglets - Version moderne"""
    return """
    <div class="workflow-container">
        <!-- En-tête du workflow -->
        <div class="workflow-header">
            <h1 class="workflow-title">₿ Workflow Crypto Principal</h1>
            <p class="workflow-subtitle">Analyse et trading automatisé des principales cryptomonnaies</p>
        </div>
        
        <!-- Navigation par onglets -->
        <div class="tabs-container">
            <nav class="tabs-nav">
                <button class="tab-btn active" onclick="showCryptoTab('overview')">
                    🏠 Vue d'ensemble
                </button>
                <button class="tab-btn" onclick="showCryptoTab('pairs')">
                    ₿ Paires Surveillées
                </button>
                <button class="tab-btn" onclick="showCryptoTab('signals')">
                    ⚡ Signaux & Analyses
                </button>
                <button class="tab-btn" onclick="showCryptoTab('config')">
                    ⚙️ Configuration
                </button>
            </nav>
            
            <!-- Contenu des onglets -->
            <div class="tabs-content">
                <!-- Onglet Vue d'ensemble -->
                <div id="crypto-tab-overview" class="tab-content active">
                    <!-- Métriques principales -->
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Paires Surveillées</div>
                            <div class="metric-value" id="crypto-pairs-monitored">5</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Signaux Aujourd'hui</div>
                            <div class="metric-value" id="crypto-signals-today">0</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Confiance Moyenne</div>
                            <div class="metric-value" id="crypto-avg-confidence">75%</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Prochain Scan</div>
                            <div class="metric-value" id="crypto-next-scan">3:00</div>
                        </div>
                    </div>
                    
                    <!-- Statut du workflow -->
                    <div class="workflow-status-section">
                        <h2 class="section-title">🔄 Statut en Temps Réel</h2>
                        
                        <div class="status-header">
                            <div class="status-info">
                                <span>Statut actuel :</span>
                                <span class="status-badge status-idle" id="crypto-current-status">Idle</span>
                            </div>
                            
                            <div class="workflow-actions">
                                <button class="action-btn action-btn-primary" onclick="forceWorkflowExecution('crypto')">
                                    ⚡ Forcer Exécution
                                </button>
                                <button class="action-btn action-btn-secondary" onclick="exportWorkflowData('crypto')">
                                    📥 Exporter Données
                                </button>
                            </div>
                        </div>
                        
                        <div class="progress-container">
                            <div class="progress-label" id="crypto-progress-label">En attente du prochain cycle...</div>
                            <div class="progress-bar">
                                <div class="progress-fill" id="crypto-progress" style="width: 0%"></div>
                            </div>
                        </div>
                        
                        <!-- Phases du workflow -->
                        <div class="phases-container">
                            <div class="phase-item" id="phase-scanning">
                                <div class="phase-status">⏳</div>
                                <div class="phase-name">Scan Marché</div>
                                <div class="phase-description">Collecte des données de prix</div>
                            </div>
                            
                            <div class="phase-item" id="phase-analyzing">
                                <div class="phase-status">⏳</div>
                                <div class="phase-name">Analyse</div>
                                <div class="phase-description">Traitement des indicateurs</div>
                            </div>
                            
                            <div class="phase-item" id="phase-executing">
                                <div class="phase-status">⏳</div>
                                <div class="phase-name">Décision</div>
                                <div class="phase-description">Génération du signal</div>
                            </div>
                            
                            <div class="phase-item" id="phase-completed">
                                <div class="phase-status">⏳</div>
                                <div class="phase-name">Terminé</div>
                                <div class="phase-description">Cycle complété</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Paires Surveillées -->
                <div id="crypto-tab-pairs" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">₿ Paires Crypto Surveillées</h3>
                        <div class="pairs-container" id="crypto-pairs-data">
                            <div class="no-data">Chargement des données...</div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Signaux & Analyses -->
                <div id="crypto-tab-signals" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">⚡ Signaux Récents</h3>
                        <div class="signals-container">
                            <div class="signals-header">
                                <div>Heure</div>
                                <div>Paire</div>
                                <div>Type</div>
                                <div>Force</div>
                                <div>Conf.</div>
                                <div>Source</div>
                                <div>Analyse</div>
                            </div>
                            <div id="crypto-signals-table">
                                <div class="no-signals">Aucun signal récent</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Configuration -->
                <div id="crypto-tab-config" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">⚙️ Paramètres du Workflow</h3>
                        <div class="config-grid">
                            <div class="config-card">
                                <h4>🔄 Fréquence de Scan</h4>
                                <p>Intervalle entre les analyses</p>
                                <div class="config-value">3 minutes</div>
                            </div>
                            
                            <div class="config-card">
                                <h4>📊 Seuil de Confiance</h4>
                                <p>Confiance minimum pour signaler</p>
                                <div class="config-value">75%</div>
                            </div>
                            
                            <div class="config-card">
                                <h4>💰 Capital par Trade</h4>
                                <p>Pourcentage maximum par position</p>
                                <div class="config-value">5%</div>
                            </div>
                            
                            <div class="config-card">
                                <h4>🎯 Stop Loss</h4>
                                <p>Protection contre les pertes</p>
                                <div class="config-value">2%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def get_meme_workflow_page() -> str:
    """Page détaillée du workflow meme avec onglets - Version moderne"""
    return """
    <div class="workflow-container">
        <!-- En-tête du workflow -->
        <div class="workflow-header">
            <h1 class="workflow-title">🐸 Workflow Crypto Meme</h1>
            <p class="workflow-subtitle">Détection et analyse des tokens meme viraux</p>
        </div>
        
        <!-- Navigation par onglets -->
        <div class="tabs-container">
            <nav class="tabs-nav">
                <button class="tab-btn active" onclick="showMemeTab('overview')">
                    🏠 Vue d'ensemble
                </button>
                <button class="tab-btn" onclick="showMemeTab('tokens')">
                    🚀 Tokens Tendance
                </button>
                <button class="tab-btn" onclick="showMemeTab('risks')">
                    ⚠️ Analyse Risques
                </button>
                <button class="tab-btn" onclick="showMemeTab('alerts')">
                    🔥 Alertes Viralité
                </button>
            </nav>
            
            <!-- Contenu des onglets -->
            <div class="tabs-content">
                <!-- Onglet Vue d'ensemble -->
                <div id="meme-tab-overview" class="tab-content active">
                    <!-- Métriques principales -->
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Tokens Scannés</div>
                            <div class="metric-value" id="meme-tokens-scanned">5</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Score Viral Max</div>
                            <div class="metric-value" id="meme-viral-score">85</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Mentions Sociales</div>
                            <div class="metric-value" id="meme-social-mentions">1.2K</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Niveau Risque</div>
                            <div class="metric-value" id="meme-risk-level">MEDIUM</div>
                        </div>
                    </div>
                    
                    <!-- Statut du workflow -->
                    <div class="workflow-status-section">
                        <h2 class="section-title">🔄 Statut en Temps Réel</h2>
                        
                        <div class="status-header">
                            <div class="status-info">
                                <span>Statut actuel :</span>
                                <span class="status-badge status-idle" id="meme-current-status">Idle</span>
                            </div>
                            
                            <div class="workflow-actions">
                                <button class="action-btn action-btn-primary" onclick="forceWorkflowExecution('meme')">
                                    ⚡ Forcer Exécution
                                </button>
                                <button class="action-btn action-btn-secondary" onclick="exportWorkflowData('meme')">
                                    📥 Exporter Données
                                </button>
                            </div>
                        </div>
                        
                        <div class="progress-container">
                            <div class="progress-label" id="meme-progress-label">En attente du prochain cycle...</div>
                            <div class="progress-bar">
                                <div class="progress-fill" id="meme-progress" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Tokens Tendance -->
                <div id="meme-tab-tokens" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">🚀 Tokens Meme Tendance</h3>
                        <div class="meme-tokens-grid" id="meme-tokens-data">
                            <div class="no-data">Chargement des tokens...</div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Analyse des Risques -->
                <div id="meme-tab-risks" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">⚠️ Analyse des Risques</h3>
                        <div class="risk-analysis-container" id="meme-risk-analysis">
                            <div class="no-data">Chargement de l'analyse...</div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Alertes Viralité -->
                <div id="meme-tab-alerts" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">🔥 Alertes Viralité en Temps Réel</h3>
                        <div class="alerts-container" id="viral-alerts">
                            <div class="no-data">Surveillance en cours...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def get_forex_workflow_page() -> str:
    """Page détaillée du workflow forex avec onglets - Version moderne"""
    return """
    <div class="workflow-container">
        <!-- En-tête du workflow -->
        <div class="workflow-header">
            <h1 class="workflow-title">💱 Workflow Forex Trading</h1>
            <p class="workflow-subtitle">Trading automatisé des devises majeures</p>
        </div>
        
        <!-- Navigation par onglets -->
        <div class="tabs-container">
            <nav class="tabs-nav">
                <button class="tab-btn active" onclick="showForexTab('overview')">
                    🏠 Vue d'ensemble
                </button>
                <button class="tab-btn" onclick="showForexTab('pairs')">
                    💱 Paires & Taux
                </button>
                <button class="tab-btn" onclick="showForexTab('indicators')">
                    📊 Indicateurs Éco
                </button>
                <button class="tab-btn" onclick="showForexTab('correlations')">
                    🔗 Corrélations
                </button>
            </nav>
            
            <!-- Contenu des onglets -->
            <div class="tabs-content">
                <!-- Onglet Vue d'ensemble -->
                <div id="forex-tab-overview" class="tab-content active">
                    <!-- Métriques principales -->
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-label">Paires Actives</div>
                            <div class="metric-value" id="forex-pairs-active">5</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Force USD</div>
                            <div class="metric-value" id="forex-usd-strength">102</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Volatilité Moy.</div>
                            <div class="metric-value" id="forex-volatility">2.1%</div>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-label">Signaux Actifs</div>
                            <div class="metric-value" id="forex-signals-count">2</div>
                        </div>
                    </div>
                    
                    <!-- Statut du workflow -->
                    <div class="workflow-status-section">
                        <h2 class="section-title">🔄 Statut en Temps Réel</h2>
                        
                        <div class="status-header">
                            <div class="status-info">
                                <span>Statut actuel :</span>
                                <span class="status-badge status-idle" id="forex-current-status">Idle</span>
                            </div>
                            
                            <div class="workflow-actions">
                                <button class="action-btn action-btn-primary" onclick="forceWorkflowExecution('forex')">
                                    ⚡ Forcer Exécution
                                </button>
                                <button class="action-btn action-btn-secondary" onclick="exportWorkflowData('forex')">
                                    📥 Exporter Données
                                </button>
                            </div>
                        </div>
                        
                        <div class="progress-container">
                            <div class="progress-label" id="forex-progress-label">En attente du prochain cycle...</div>
                            <div class="progress-bar">
                                <div class="progress-fill" id="forex-progress" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Paires & Taux -->
                <div id="forex-tab-pairs" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">💱 Paires Forex Surveillées</h3>
                        <div class="pairs-container" id="forex-pairs-data">
                            <div class="no-data">Chargement des taux...</div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Indicateurs Économiques -->
                <div id="forex-tab-indicators" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">📊 Indicateurs Économiques</h3>
                        <div class="economic-indicators" id="economic-indicators">
                            <div class="no-data">Chargement des indicateurs...</div>
                        </div>
                    </div>
                </div>
                
                <!-- Onglet Corrélations -->
                <div id="forex-tab-correlations" class="tab-content">
                    <div class="data-section">
                        <h3 class="data-section-title">🔗 Analyse des Corrélations</h3>
                        <div class="correlations-grid" id="correlations-data">
                            <div class="no-data">Calcul des corrélations...</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

def get_workflow_styles() -> str:
    """Styles CSS pour les workflows - Version corrigée"""
    return """
    /* === CONTAINERS PRINCIPAUX === */
    .workflow-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0;
    }
    
    .workflow-header {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .workflow-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    
    .workflow-subtitle {
        opacity: 0.9;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* === MÉTRIQUES === */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    
    /* === STATUT WORKFLOW === */
    .workflow-status-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 2rem;
        margin-bottom: 2rem;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: var(--text-primary);
    }
    
    .status-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .status-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 1.5rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
    }
    
    /* === BARRE DE PROGRESSION === */
    .progress-container {
        margin: 1.5rem 0;
    }
    
    .progress-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #f1f5f9;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--success));
        transition: width 0.3s ease;
        border-radius: 4px;
    }
    
    /* === PHASES WORKFLOW === */
    .phases-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .phase-item {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .phase-item.active {
        border-color: var(--primary);
        background: #dbeafe;
    }
    
    .phase-item.completed {
        border-color: var(--success);
        background: #d1fae5;
    }
    
    .phase-status {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    .phase-name {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .phase-description {
        font-size: 0.75rem;
        color: var(--text-secondary);
        line-height: 1.3;
    }
    
    /* === ACTIONS === */
    .workflow-actions {
        display: flex;
        gap: 1rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    
    .action-btn {
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .action-btn-primary {
        background: var(--primary);
        color: white;
    }
    
    .action-btn-secondary {
        background: #f1f5f9;
        color: var(--text-secondary);
        border: 1px solid var(--border);
    }
    
    .action-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* === DONNÉES DÉTAILLÉES === */
    .data-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .data-section {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .data-section-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--text-primary);
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
    }
    
    /* === PAIRES CRYPTO === */
    .pairs-container {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .pair-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .pair-item:hover {
        background: #f1f5f9;
        transform: translateX(4px);
    }
    
    .pair-info {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .pair-symbol {
        font-weight: 700;
        font-size: 1rem;
        color: var(--text-primary);
    }
    
    .pair-price {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-family: 'Courier New', monospace;
    }
    
    .pair-metrics {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.25rem;
    }
    
    .pair-change {
        font-weight: 600;
        font-size: 0.875rem;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
    }
    
    .pair-change.positive {
        background: #d1fae5;
        color: #065f46;
    }
    
    .pair-change.negative {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .pair-volume {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    /* === TOKENS MEME === */
    .meme-tokens-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .meme-token-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .meme-token-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .meme-token-symbol {
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .viral-score {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .viral-score.high {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .viral-score.medium {
        background: #fef3c7;
        color: #92400e;
    }
    
    .viral-score.low {
        background: #d1fae5;
        color: #065f46;
    }
    
    .token-metrics {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    /* === ANALYSE RISQUES === */
    .risk-analysis-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .risk-item {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .risk-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    
    .risk-token {
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .risk-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    
    .risk-badge.high {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .risk-badge.medium {
        background: #fef3c7;
        color: #92400e;
    }
    
    .risk-badge.low {
        background: #d1fae5;
        color: #065f46;
    }
    
    .risk-details {
        font-size: 0.875rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .risk-score {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    /* === SIGNAUX === */
    .signals-container {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
    }
    
    .signals-header {
        display: grid;
        grid-template-columns: 80px 100px 80px 80px 60px 80px 1fr;
        gap: 1rem;
        padding: 0.75rem;
        background: #f8fafc;
        border-bottom: 1px solid var(--border);
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .signal-row {
        display: grid;
        grid-template-columns: 80px 100px 80px 80px 60px 80px 1fr;
        gap: 1rem;
        padding: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
        font-size: 0.875rem;
        align-items: center;
        transition: background 0.2s ease;
    }
    
    .signal-row:hover {
        background: #f8fafc;
    }
    
    .signal-row:last-child {
        border-bottom: none;
    }
    
    .signal-type {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-align: center;
    }
    
    .signal-type.buy {
        background: #d1fae5;
        color: #065f46;
    }
    
    .signal-type.sell {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .signal-type.hold {
        background: #fef3c7;
        color: #92400e;
    }
    
    .signal-strength {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-align: center;
    }
    
    .signal-strength.strength-weak {
        background: #f1f5f9;
        color: var(--text-secondary);
    }
    
    .signal-strength.strength-medium {
        background: #fef3c7;
        color: #92400e;
    }
    
    .signal-strength.strength-strong {
        background: #d1fae5;
        color: #065f46;
    }
    
    .signal-reasoning {
        font-size: 0.75rem;
        color: var(--text-secondary);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    /* === ALERTES === */
    .alerts-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .alert-item {
        display: flex;
        gap: 1rem;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid;
        background: #f8fafc;
    }
    
    .alert-item.success {
        border-left-color: var(--success);
        background: #f0fdfa;
    }
    
    .alert-item.warning {
        border-left-color: var(--warning);
        background: #fffbeb;
    }
    
    .alert-item.danger {
        border-left-color: var(--danger);
        background: #fef2f2;
    }
    
    .alert-icon {
        font-size: 1.25rem;
        flex-shrink: 0;
    }
    
    .alert-content {
        flex: 1;
    }
    
    .alert-title {
        font-weight: 700;
        margin-bottom: 0.25rem;
        color: var(--text-primary);
    }
    
    .alert-description {
        font-size: 0.875rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .alert-time {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
    }
    
    /* === DONNÉES NO-DATA === */
    .no-data {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-style: italic;
    }
    
    .no-signals {
        text-align: center;
        padding: 2rem;
        color: var(--text-secondary);
        font-style: italic;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        background: #f8fafc;
    }
    
    /* === RESPONSIVE === */
    @media (max-width: 768px) {
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        
        .status-header {
            flex-direction: column;
            align-items: stretch;
        }
        
        .workflow-actions {
            flex-direction: column;
        }
        
        .data-grid {
            grid-template-columns: 1fr;
        }
        
        .phases-container {
            grid-template-columns: 1fr;
        }
        
        .meme-tokens-grid {
            grid-template-columns: 1fr;
        }
        
        .signals-header,
        .signal-row {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
        
        .signal-row > div {
            padding: 0.25rem;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .pair-item {
            flex-direction: column;
            align-items: stretch;
            gap: 0.5rem;
        }
        
        .pair-metrics {
            align-items: stretch;
        }
    }
    
    /* === FOREX SPÉCIFIQUE === */
    .economic-indicators {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
    }
    
    .economic-item {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
    }
    
    .indicator-title {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .indicator-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    .sentiment-hawkish { color: var(--danger); }
    .sentiment-dovish { color: var(--success); }
    .sentiment-neutral { color: var(--text-secondary); }
    
    .correlations-grid {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .correlation-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem;
        background: #f8fafc;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
    }
    
    .correlation-label {
        font-size: 0.875rem;
        color: var(--text-primary);
        font-weight: 500;
    }
    
    .correlation-value {
        font-weight: 700;
        font-size: 0.875rem;
    }
    
    .correlation-value.positive { color: var(--success); }
    .correlation-value.negative { color: var(--danger); }
    .correlation-value.neutral { color: var(--text-secondary); }
    
    /* === SYSTÈME D'ONGLETS === */
    .tabs-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .tabs-nav {
        display: flex;
        background: #f8fafc;
        border-bottom: 1px solid var(--border);
        overflow-x: auto;
    }
    
    .tab-btn {
        flex: 1;
        min-width: 150px;
        padding: 1rem 1.5rem;
        border: none;
        background: transparent;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-bottom: 3px solid transparent;
        white-space: nowrap;
    }
    
    .tab-btn:hover {
        background: #f1f5f9;
        color: var(--text-primary);
    }
    
    .tab-btn.active {
        background: var(--bg-card);
        color: var(--primary);
        border-bottom-color: var(--primary);
    }
    
    .tabs-content {
        padding: 2rem;
    }
    
    .tab-content {
        display: none;
        animation: fadeIn 0.3s ease;
    }
    
    .tab-content.active {
        display: block;
    }
    
    /* === CONFIGURATION === */
    .config-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
    }
    
    .config-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    
    .config-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .config-card h4 {
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .config-card p {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-bottom: 1rem;
        line-height: 1.4;
    }
    
    .config-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--primary);
        background: var(--bg-card);
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 2px solid var(--primary);
    }
    
    /* === RESPONSIVE ONGLETS === */
    @media (max-width: 768px) {
        .tabs-nav {
            flex-direction: column;
        }
        
        .tab-btn {
            min-width: auto;
            border-bottom: none;
            border-right: 3px solid transparent;
        }
        
        .tab-btn.active {
            border-bottom: none;
            border-right-color: var(--primary);
        }
        
        .tabs-content {
            padding: 1.5rem;
        }
        
        .config-grid {
            grid-template-columns: 1fr;
        }
    }
    """ 