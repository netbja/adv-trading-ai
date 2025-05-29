#!/usr/bin/env python3
"""
🔄 PAGES DÉTAILLÉES DES WORKFLOWS
Vues temps réel pour crypto, meme et forex avec métriques avancées
"""

from typing import Dict, Any

def get_crypto_workflow_page() -> str:
    """Page détaillée du workflow crypto"""
    return """
    <div class="workflow-detail-page">
        <div class="page-header">
            <div class="header-content">
                <h1>₿ Workflow Crypto Principal</h1>
                <p>Analyse et trading des cryptomonnaies principales</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary" onclick="forceWorkflowExecution('crypto')">
                    ⚡ Forcer Exécution
                </button>
                <button class="btn btn-secondary" onclick="exportWorkflowData('crypto')">
                    📊 Exporter Données
                </button>
            </div>
        </div>
        
        <!-- Métriques temps réel -->
        <div class="grid grid-4" style="margin-bottom: 2rem;">
            <div class="metric-card">
                <div class="metric-icon crypto">₿</div>
                <div class="metric-content">
                    <div class="metric-value" id="crypto-pairs-monitored">5</div>
                    <div class="metric-label">Paires Surveillées</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon success">📊</div>
                <div class="metric-content">
                    <div class="metric-value" id="crypto-signals-today">0</div>
                    <div class="metric-label">Signaux Aujourd'hui</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon warning">⚡</div>
                <div class="metric-content">
                    <div class="metric-value" id="crypto-avg-confidence">75%</div>
                    <div class="metric-label">Confiance Moyenne</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon primary">🔄</div>
                <div class="metric-content">
                    <div class="metric-value" id="crypto-next-scan">2:30</div>
                    <div class="metric-label">Prochain Scan</div>
                </div>
            </div>
        </div>
        
        <div class="grid grid-2">
            <!-- Statut en temps réel -->
            <div class="card">
                <div class="card-header">
                    <div>
                        <h3>🔄 Statut Temps Réel</h3>
                        <p>État actuel du workflow</p>
                    </div>
                    <div class="status-badge status-scanning" id="crypto-current-status">Scan</div>
                </div>
                
                <div class="workflow-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" id="crypto-progress" style="width: 0%"></div>
                    </div>
                    <div class="progress-label" id="crypto-progress-label">En attente...</div>
                </div>
                
                <div class="workflow-phases">
                    <div class="phase-item" id="phase-scanning">
                        <div class="phase-icon">🔍</div>
                        <div class="phase-content">
                            <div class="phase-title">Scan des Marchés</div>
                            <div class="phase-description">Analyse des 5 principales cryptos</div>
                        </div>
                        <div class="phase-status">⏳</div>
                    </div>
                    
                    <div class="phase-item" id="phase-analysis">
                        <div class="phase-icon">📊</div>
                        <div class="phase-content">
                            <div class="phase-title">Analyse Technique</div>
                            <div class="phase-description">Patterns et indicateurs</div>
                        </div>
                        <div class="phase-status">⏳</div>
                    </div>
                    
                    <div class="phase-item" id="phase-sentiment">
                        <div class="phase-icon">💭</div>
                        <div class="phase-content">
                            <div class="phase-title">Sentiment Marché</div>
                            <div class="phase-description">Réseaux sociaux et news</div>
                        </div>
                        <div class="phase-status">⏳</div>
                    </div>
                    
                    <div class="phase-item" id="phase-decision">
                        <div class="phase-icon">⚡</div>
                        <div class="phase-content">
                            <div class="phase-title">Décision Trading</div>
                            <div class="phase-description">Signal final généré</div>
                        </div>
                        <div class="phase-status">⏳</div>
                    </div>
                </div>
            </div>
            
            <!-- Paires crypto surveillées -->
            <div class="card">
                <div class="card-header">
                    <h3>📈 Paires Surveillées</h3>
                    <p>État des cryptomonnaies</p>
                </div>
                
                <div class="crypto-pairs-list" id="crypto-pairs-data">
                    <!-- Chargé dynamiquement -->
                </div>
            </div>
        </div>
        
        <!-- Signaux récents -->
        <div class="card" style="margin-top: 2rem;">
            <div class="card-header">
                <h3>⚡ Signaux Récents</h3>
                <p>Historique des derniers signaux détectés</p>
            </div>
            
            <div class="signals-table">
                <div class="table-header">
                    <div class="col-time">Heure</div>
                    <div class="col-symbol">Symbole</div>
                    <div class="col-type">Type</div>
                    <div class="col-strength">Force</div>
                    <div class="col-confidence">Confiance</div>
                    <div class="col-source">Source</div>
                    <div class="col-reasoning">Raison</div>
                </div>
                
                <div class="table-body" id="crypto-signals-table">
                    <!-- Chargé dynamiquement -->
                </div>
            </div>
        </div>
    </div>
    """

def get_meme_workflow_page() -> str:
    """Page détaillée du workflow crypto meme"""
    return """
    <div class="workflow-detail-page">
        <div class="page-header">
            <div class="header-content">
                <h1>🐸 Workflow Crypto Meme</h1>
                <p>Détection et analyse des tokens meme tendance</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary" onclick="forceWorkflowExecution('meme')">
                    🚀 Forcer Scan
                </button>
                <button class="btn btn-secondary" onclick="exportWorkflowData('meme')">
                    📊 Exporter
                </button>
            </div>
        </div>
        
        <!-- Métriques spéciales meme -->
        <div class="grid grid-4" style="margin-bottom: 2rem;">
            <div class="metric-card">
                <div class="metric-icon meme">🐸</div>
                <div class="metric-content">
                    <div class="metric-value" id="meme-tokens-scanned">5</div>
                    <div class="metric-label">Tokens Scannés</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon danger">🔥</div>
                <div class="metric-content">
                    <div class="metric-value" id="meme-viral-score">0</div>
                    <div class="metric-label">Score Viral Max</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon warning">📱</div>
                <div class="metric-content">
                    <div class="metric-value" id="meme-social-mentions">0</div>
                    <div class="metric-label">Mentions Sociales</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon success">⚠️</div>
                <div class="metric-content">
                    <div class="metric-value" id="meme-risk-level">LOW</div>
                    <div class="metric-label">Niveau Risque</div>
                </div>
            </div>
        </div>
        
        <div class="grid grid-2">
            <!-- Tokens tendance -->
            <div class="card">
                <div class="card-header">
                    <h3>🔥 Tokens Tendance</h3>
                    <p>Détection viralité en temps réel</p>
                </div>
                
                <div class="meme-tokens-grid" id="meme-tokens-data">
                    <!-- Chargé dynamiquement -->
                </div>
            </div>
            
            <!-- Analyse des risques -->
            <div class="card">
                <div class="card-header">
                    <h3>⚖️ Analyse des Risques</h3>
                    <p>Évaluation risque/reward</p>
                </div>
                
                <div class="risk-analysis" id="meme-risk-analysis">
                    <!-- Chargé dynamiquement -->
                </div>
            </div>
        </div>
        
        <!-- Alertes viralité -->
        <div class="card viral-alerts" style="margin-top: 2rem;">
            <div class="card-header">
                <h3>🚨 Alertes Viralité</h3>
                <p>Tokens avec potentiel viral élevé</p>
            </div>
            
            <div class="viral-alerts-content" id="viral-alerts">
                <div class="alert-item success">
                    <div class="alert-icon">🚀</div>
                    <div class="alert-content">
                        <div class="alert-title">Aucune alerte active</div>
                        <div class="alert-description">Surveillance en cours...</div>
                    </div>
                    <div class="alert-time">En temps réel</div>
                </div>
            </div>
        </div>
    </div>
    """

def get_forex_workflow_page() -> str:
    """Page détaillée du workflow forex"""
    return """
    <div class="workflow-detail-page">
        <div class="page-header">
            <div class="header-content">
                <h1>💱 Workflow Forex Trading</h1>
                <p>Analyse des devises et indicateurs économiques</p>
            </div>
            <div class="header-actions">
                <button class="btn btn-primary" onclick="forceWorkflowExecution('forex')">
                    💹 Analyser Maintenant
                </button>
                <button class="btn btn-secondary" onclick="exportWorkflowData('forex')">
                    📈 Exporter
                </button>
            </div>
        </div>
        
        <!-- Métriques forex -->
        <div class="grid grid-4" style="margin-bottom: 2rem;">
            <div class="metric-card">
                <div class="metric-icon forex">💱</div>
                <div class="metric-content">
                    <div class="metric-value" id="forex-pairs-active">5</div>
                    <div class="metric-label">Paires Forex</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon primary">🏦</div>
                <div class="metric-content">
                    <div class="metric-value" id="forex-usd-strength">100</div>
                    <div class="metric-label">Force USD</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon warning">📊</div>
                <div class="metric-content">
                    <div class="metric-value" id="forex-volatility">2.1%</div>
                    <div class="metric-label">Volatilité Moy.</div>
                </div>
            </div>
            
            <div class="metric-card">
                <div class="metric-icon success">🎯</div>
                <div class="metric-content">
                    <div class="metric-value" id="forex-signals-count">0</div>
                    <div class="metric-label">Signaux Actifs</div>
                </div>
            </div>
        </div>
        
        <div class="grid grid-2">
            <!-- Paires principales -->
            <div class="card">
                <div class="card-header">
                    <h3>💹 Paires Principales</h3>
                    <p>Majors et indicateurs techniques</p>
                </div>
                
                <div class="forex-pairs-table" id="forex-pairs-data">
                    <!-- Chargé dynamiquement -->
                </div>
            </div>
            
            <!-- Indicateurs économiques -->
            <div class="card">
                <div class="card-header">
                    <h3>🏦 Indicateurs Économiques</h3>
                    <p>Sentiment des banques centrales</p>
                </div>
                
                <div class="economic-indicators" id="economic-indicators">
                    <!-- Chargé dynamiquement -->
                </div>
            </div>
        </div>
        
        <!-- Analyse des corrélations -->
        <div class="card correlations-card" style="margin-top: 2rem;">
            <div class="card-header">
                <h3>🔗 Analyse des Corrélations</h3>
                <p>Relations entre devises et actifs</p>
            </div>
            
            <div class="correlations-grid" id="correlations-data">
                <!-- Chargé dynamiquement -->
            </div>
        </div>
    </div>
    """

def get_workflow_styles() -> str:
    """Styles CSS pour les pages de workflows"""
    return """
    /* Styles pour pages de workflows */
    .workflow-detail-page {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .page-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border);
    }
    
    .header-content h1 {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .header-content p {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }
    
    .header-actions {
        display: flex;
        gap: 1rem;
    }
    
    /* Cartes métriques */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 0.75rem;
        padding: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.2s;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .metric-icon {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .metric-icon.crypto { background: #fef3c7; color: #92400e; }
    .metric-icon.meme { background: #f3e8ff; color: #7c3aed; }
    .metric-icon.forex { background: #dbeafe; color: #1e40af; }
    .metric-icon.success { background: #d1fae5; color: #065f46; }
    .metric-icon.warning { background: #fef3c7; color: #92400e; }
    .metric-icon.danger { background: #fee2e2; color: #991b1b; }
    .metric-icon.primary { background: #dbeafe; color: #1e40af; }
    
    .metric-content {
        flex: 1;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-weight: 500;
        margin-top: 0.25rem;
    }
    
    /* Barre de progression workflow */
    .workflow-progress {
        margin: 1.5rem 0;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #f1f5f9;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--success));
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    .progress-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-align: center;
    }
    
    /* Phases du workflow */
    .workflow-phases {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .phase-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        transition: all 0.2s;
    }
    
    .phase-item.active {
        border-color: var(--primary);
        background: #f0f9ff;
    }
    
    .phase-item.completed {
        border-color: var(--success);
        background: #f0fdf4;
    }
    
    .phase-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #f1f5f9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.125rem;
    }
    
    .phase-content {
        flex: 1;
    }
    
    .phase-title {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .phase-description {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }
    
    .phase-status {
        font-size: 1.25rem;
    }
    
    /* Listes de données crypto/forex */
    .crypto-pairs-list, .forex-pairs-table {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .pair-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        transition: all 0.2s;
    }
    
    .pair-item:hover {
        border-color: var(--primary);
        background: #f8fafc;
    }
    
    .pair-info {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .pair-symbol {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .pair-price {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .pair-change {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.875rem;
    }
    
    .pair-change.positive {
        background: #d1fae5;
        color: #065f46;
    }
    
    .pair-change.negative {
        background: #fee2e2;
        color: #991b1b;
    }
    
    /* Tokens meme grid */
    .meme-tokens-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
    }
    
    .meme-token-card {
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        padding: 1rem;
        text-align: center;
        transition: all 0.2s;
    }
    
    .meme-token-card:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
    }
    
    .meme-token-symbol {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .viral-score {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .viral-score.high { color: var(--danger); }
    .viral-score.medium { color: var(--warning); }
    .viral-score.low { color: var(--success); }
    
    /* Tableaux de signaux */
    .signals-table {
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    .table-header {
        display: grid;
        grid-template-columns: 80px 100px 80px 80px 80px 100px 1fr;
        gap: 1rem;
        padding: 1rem;
        background: #f8fafc;
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    .table-body {
        max-height: 400px;
        overflow-y: auto;
    }
    
    .signal-row {
        display: grid;
        grid-template-columns: 80px 100px 80px 80px 80px 100px 1fr;
        gap: 1rem;
        padding: 1rem;
        border-bottom: 1px solid var(--border);
        align-items: center;
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
    
    .signal-type.buy { background: #d1fae5; color: #065f46; }
    .signal-type.sell { background: #fee2e2; color: #991b1b; }
    .signal-type.hold { background: #f1f5f9; color: var(--text-secondary); }
    
    .signal-strength {
        text-align: center;
        font-weight: 600;
    }
    
    .strength-very-strong { color: #dc2626; }
    .strength-strong { color: #ea580c; }
    .strength-moderate { color: #ca8a04; }
    .strength-weak { color: #65a30d; }
    
    /* Alertes viralité */
    .viral-alerts-content {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .alert-item {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid;
    }
    
    .alert-item.success {
        background: #f0fdf4;
        border-left-color: var(--success);
    }
    
    .alert-item.warning {
        background: #fffbeb;
        border-left-color: var(--warning);
    }
    
    .alert-item.danger {
        background: #fef2f2;
        border-left-color: var(--danger);
    }
    
    .alert-icon {
        font-size: 1.5rem;
    }
    
    .alert-content {
        flex: 1;
    }
    
    .alert-title {
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    
    .alert-description {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .alert-time {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    /* Corrélations */
    .correlations-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
    }
    
    .correlation-item {
        padding: 1rem;
        border: 1px solid var(--border);
        border-radius: 0.5rem;
        text-align: center;
    }
    
    .correlation-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .correlation-positive { color: var(--success); }
    .correlation-negative { color: var(--danger); }
    .correlation-neutral { color: var(--text-secondary); }
    
    /* Responsive */
    @media (max-width: 768px) {
        .grid-4 {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .grid-2 {
            grid-template-columns: 1fr;
        }
        
        .page-header {
            flex-direction: column;
            gap: 1rem;
        }
        
        .header-actions {
            align-self: stretch;
        }
        
        .table-header, .signal-row {
            grid-template-columns: 60px 80px 60px 60px 80px 1fr;
            font-size: 0.75rem;
        }
    }
    """ 