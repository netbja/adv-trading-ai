#!/usr/bin/env python3
"""
⚡ JAVASCRIPT POUR WORKFLOWS
Gestion des interactions et mises à jour temps réel
"""

def get_workflow_javascript() -> str:
    """JavaScript pour les workflows temps réel"""
    return """
    // Variables globales pour workflows
    let workflowUpdateIntervals = {};
    let currentWorkflowData = {};
    
    // === GESTION DES PAGES WORKFLOWS ===
    
    async function loadWorkflowPage(workflowType) {
        try {
            // Charger les données initiales
            await loadWorkflowData(workflowType);
            
            // Démarrer les mises à jour automatiques
            startWorkflowUpdates(workflowType);
            
        } catch (error) {
            console.error(`Erreur chargement workflow ${workflowType}:`, error);
            showErrorMessage(`Impossible de charger les données du workflow ${workflowType}`);
        }
    }
    
    async function loadWorkflowData(workflowType) {
        const endpoints = {
            'crypto': '/api/workflows/crypto/details',
            'meme': '/api/workflows/meme/details', 
            'forex': '/api/workflows/forex/details'
        };
        
        const response = await fetch(endpoints[workflowType]);
        const data = await response.json();
        
        if (response.ok) {
            currentWorkflowData[workflowType] = data;
            updateWorkflowUI(workflowType, data);
        } else {
            throw new Error(data.detail || 'Erreur API');
        }
    }
    
    function updateWorkflowUI(workflowType, data) {
        switch(workflowType) {
            case 'crypto':
                updateCryptoWorkflowUI(data);
                break;
            case 'meme':
                updateMemeWorkflowUI(data);
                break;
            case 'forex':
                updateForexWorkflowUI(data);
                break;
        }
    }
    
    // === CRYPTO WORKFLOW UI ===
    
    function updateCryptoWorkflowUI(data) {
        // Métriques principales
        updateElement('crypto-pairs-monitored', data.pairs_monitored || 5);
        updateElement('crypto-signals-today', data.signals_today || 0);
        updateElement('crypto-avg-confidence', (data.avg_confidence || 0.75 * 100).toFixed(0) + '%');
        updateElement('crypto-next-scan', formatNextScanTime(data.next_scan_in_seconds || 180));
        
        // Statut workflow
        updateWorkflowStatus('crypto', data.current_execution);
        
        // Paires crypto
        updateCryptoPairsList(data.pairs_data || {});
        
        // Signaux récents
        updateSignalsTable('crypto', data.recent_signals || []);
    }
    
    function updateWorkflowStatus(workflowType, execution) {
        const statusElement = document.getElementById(`${workflowType}-current-status`);
        const progressElement = document.getElementById(`${workflowType}-progress`);
        const labelElement = document.getElementById(`${workflowType}-progress-label`);
        
        // Vérifier que les éléments existent avant de les manipuler
        if (!statusElement || !progressElement || !labelElement) {
            return; // Page non compatible avec cette fonction
        }
        
        if (!execution) {
            statusElement.textContent = 'Idle';
            statusElement.className = 'status-badge status-idle';
            progressElement.style.width = '0%';
            labelElement.textContent = 'En attente du prochain cycle...';
            return;
        }
        
        const status = execution.status;
        const phases = ['scanning', 'analyzing', 'executing', 'completed'];
        const currentPhaseIndex = phases.indexOf(status);
        
        // Mettre à jour badge de statut
        statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        statusElement.className = `status-badge status-${status}`;
        
        // Mettre à jour barre de progression
        const progressPercent = currentPhaseIndex >= 0 ? ((currentPhaseIndex + 1) / phases.length) * 100 : 0;
        progressElement.style.width = progressPercent + '%';
        
        // Mettre à jour phases
        const phaseLabels = {
            'scanning': 'Scan des marchés en cours...',
            'analyzing': 'Analyse technique des signaux...',
            'executing': 'Génération de la décision finale...',
            'completed': 'Cycle terminé avec succès!'
        };
        
        labelElement.textContent = phaseLabels[status] || 'État inconnu';
        
        // Mettre à jour les icônes de phases
        phases.forEach((phase, index) => {
            const phaseElement = document.getElementById(`phase-${phase}`);
            if (phaseElement) {
                phaseElement.classList.remove('active', 'completed');
                
                if (index < currentPhaseIndex) {
                    phaseElement.classList.add('completed');
                    phaseElement.querySelector('.phase-status').textContent = '✅';
                } else if (index === currentPhaseIndex) {
                    phaseElement.classList.add('active');
                    phaseElement.querySelector('.phase-status').textContent = '🔄';
                } else {
                    phaseElement.querySelector('.phase-status').textContent = '⏳';
                }
            }
        });
    }
    
    function updateCryptoPairsList(pairsData) {
        const container = document.getElementById('crypto-pairs-data');
        if (!container) return;
        
        const pairs = Object.entries(pairsData).map(([symbol, data]) => {
            const changeClass = data.change_24h >= 0 ? 'positive' : 'negative';
            const changeSign = data.change_24h >= 0 ? '+' : '';
            
            return `
                <div class="pair-item">
                    <div class="pair-info">
                        <div class="pair-symbol">${symbol}</div>
                        <div class="pair-price">$${data.price?.toFixed(6) || '0.000000'}</div>
                    </div>
                    <div class="pair-metrics">
                        <div class="pair-change ${changeClass}">
                            ${changeSign}${data.change_24h?.toFixed(2) || '0.00'}%
                        </div>
                        <div class="pair-volume">Vol: ${formatVolume(data.volume_24h || 0)}</div>
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = pairs || '<div class="no-data">Aucune donnée disponible</div>';
    }
    
    // === MEME WORKFLOW UI ===
    
    function updateMemeWorkflowUI(data) {
        // Métriques meme
        updateElement('meme-tokens-scanned', data.tokens_scanned || 5);
        updateElement('meme-viral-score', data.max_viral_score || 0);
        updateElement('meme-social-mentions', data.total_social_mentions || 0);
        updateElement('meme-risk-level', data.overall_risk_level || 'LOW');
        
        // Tokens tendance
        updateMemeTokensGrid(data.tokens_data || {});
        
        // Analyse des risques
        updateRiskAnalysis(data.risk_analysis || {});
        
        // Alertes viralité
        updateViralAlerts(data.viral_alerts || []);
    }
    
    function updateMemeTokensGrid(tokensData) {
        const container = document.getElementById('meme-tokens-data');
        if (!container) return;
        
        const tokens = Object.entries(tokensData).map(([symbol, data]) => {
            const viralScoreClass = data.viral_score > 70 ? 'high' : 
                                   data.viral_score > 40 ? 'medium' : 'low';
            
            return `
                <div class="meme-token-card">
                    <div class="meme-token-symbol">${symbol}</div>
                    <div class="viral-score ${viralScoreClass}">
                        ${data.viral_score?.toFixed(0) || 0}/100
                    </div>
                    <div class="token-metrics">
                        <div>Mentions: ${data.social_mentions || 0}</div>
                        <div>Change: ${(data.change_24h || 0).toFixed(1)}%</div>
                        <div>Whale: ${data.whale_activity || 'low'}</div>
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = tokens || '<div class="no-data">Aucun token analysé</div>';
    }
    
    function updateRiskAnalysis(riskData) {
        const container = document.getElementById('meme-risk-analysis');
        if (!container) return;
        
        const risks = Object.entries(riskData).map(([token, risk]) => {
            const levelClass = risk.risk_level.toLowerCase();
            
            return `
                <div class="risk-item">
                    <div class="risk-header">
                        <span class="risk-token">${token}</span>
                        <span class="risk-badge ${levelClass}">${risk.risk_level}</span>
                    </div>
                    <div class="risk-details">
                        <div class="risk-score">Score: ${risk.risk_score}/100</div>
                        <div class="risk-factors">
                            Volatilité: ${risk.factors.volatility?.toFixed(1) || 0}% • 
                            Social: ${risk.factors.social_activity || 0} • 
                            Whale: ${risk.factors.whale_activity || 'low'}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = risks || '<div class="no-data">Aucune analyse disponible</div>';
    }
    
    function updateViralAlerts(alerts) {
        const container = document.getElementById('viral-alerts');
        if (!container) return;
        
        if (alerts.length === 0) {
            container.innerHTML = `
                <div class="alert-item success">
                    <div class="alert-icon">🚀</div>
                    <div class="alert-content">
                        <div class="alert-title">Aucune alerte active</div>
                        <div class="alert-description">Surveillance en cours...</div>
                    </div>
                    <div class="alert-time">En temps réel</div>
                </div>
            `;
            return;
        }
        
        const alertsHtml = alerts.map(alert => {
            const alertClass = alert.severity === 'high' ? 'danger' : 
                              alert.severity === 'medium' ? 'warning' : 'success';
            
            return `
                <div class="alert-item ${alertClass}">
                    <div class="alert-icon">${alert.icon || '⚠️'}</div>
                    <div class="alert-content">
                        <div class="alert-title">${alert.title}</div>
                        <div class="alert-description">${alert.description}</div>
                    </div>
                    <div class="alert-time">${formatTimeAgo(alert.timestamp)}</div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = alertsHtml;
    }
    
    // === FOREX WORKFLOW UI ===
    
    function updateForexWorkflowUI(data) {
        // Métriques forex
        updateElement('forex-pairs-active', data.pairs_active || 5);
        updateElement('forex-usd-strength', data.usd_strength_index?.toFixed(0) || 100);
        updateElement('forex-volatility', (data.avg_volatility * 100)?.toFixed(1) + '%' || '2.1%');
        updateElement('forex-signals-count', data.active_signals_count || 0);
        
        // Paires forex
        updateForexPairsTable(data.pairs_data || {});
        
        // Indicateurs économiques
        updateEconomicIndicators(data.economic_data || {});
        
        // Corrélations
        updateCorrelationsGrid(data.correlations || {});
    }
    
    function updateForexPairsTable(pairsData) {
        const container = document.getElementById('forex-pairs-data');
        if (!container) return;
        
        const pairs = Object.entries(pairsData).map(([symbol, data]) => {
            const changeClass = data.change_24h >= 0 ? 'positive' : 'negative';
            const changeSign = data.change_24h >= 0 ? '+' : '';
            
            return `
                <div class="pair-item">
                    <div class="pair-info">
                        <div class="pair-symbol">${symbol}</div>
                        <div class="pair-price">${data.current_rate?.toFixed(4) || '0.0000'}</div>
                    </div>
                    <div class="pair-metrics">
                        <div class="pair-change ${changeClass}">
                            ${changeSign}${data.change_24h?.toFixed(2) || '0.00'}%
                        </div>
                        <div class="pair-trend">${data.trend || 'Neutre'}</div>
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = pairs || '<div class="no-data">Aucune donnée forex</div>';
    }
    
    function updateEconomicIndicators(economicData) {
        const container = document.getElementById('economic-indicators');
        if (!container) return;
        
        const indicators = `
            <div class="economic-item">
                <div class="indicator-title">Force USD</div>
                <div class="indicator-value">${economicData.usd_strength_index?.toFixed(0) || 100}</div>
            </div>
            
            <div class="economic-item">
                <div class="indicator-title">Sentiment Global</div>
                <div class="indicator-value">${economicData.global_risk_sentiment || 'neutral'}</div>
            </div>
            
            <div class="economic-item">
                <div class="indicator-title">FED</div>
                <div class="indicator-value sentiment-${economicData.central_bank_sentiment?.fed || 'neutral'}">
                    ${economicData.central_bank_sentiment?.fed || 'neutral'}
                </div>
            </div>
            
            <div class="economic-item">
                <div class="indicator-title">ECB</div>
                <div class="indicator-value sentiment-${economicData.central_bank_sentiment?.ecb || 'neutral'}">
                    ${economicData.central_bank_sentiment?.ecb || 'neutral'}
                </div>
            </div>
            
            <div class="economic-item">
                <div class="indicator-title">Événements Aujourd'hui</div>
                <div class="indicator-value">${economicData.economic_calendar?.high_impact_events_today || 0}</div>
            </div>
        `;
        
        container.innerHTML = indicators;
    }
    
    function updateCorrelationsGrid(correlations) {
        const container = document.getElementById('correlations-data');
        if (!container) return;
        
        const correlationsHtml = Object.entries(correlations).map(([pair, value]) => {
            const correlationClass = value > 0.5 ? 'positive' : 
                                   value < -0.5 ? 'negative' : 'neutral';
            
            return `
                <div class="correlation-item">
                    <div class="correlation-label">${pair.replace('_vs_', ' vs ')}</div>
                    <div class="correlation-value ${correlationClass}">
                        ${(value * 100).toFixed(0)}%
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = correlationsHtml || '<div class="no-data">Aucune corrélation</div>';
    }
    
    // === TABLEAUX DE SIGNAUX ===
    
    function updateSignalsTable(workflowType, signals) {
        const container = document.getElementById(`${workflowType}-signals-table`);
        if (!container) return;
        
        if (signals.length === 0) {
            container.innerHTML = '<div class="no-signals">Aucun signal récent</div>';
            return;
        }
        
        const signalsHtml = signals.map(signal => {
            const strengthClass = `strength-${signal.strength.replace('_', '-')}`;
            const typeClass = signal.signal_type.toLowerCase();
            
            return `
                <div class="signal-row">
                    <div>${new Date(signal.timestamp).toLocaleTimeString()}</div>
                    <div class="pair-symbol">${signal.symbol}</div>
                    <div class="signal-type ${typeClass}">${signal.signal_type}</div>
                    <div class="signal-strength ${strengthClass}">${signal.strength}</div>
                    <div>${(signal.confidence * 100).toFixed(0)}%</div>
                    <div>${signal.source}</div>
                    <div class="signal-reasoning">${signal.reasoning}</div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = signalsHtml;
    }
    
    // === GESTION DES MISES À JOUR ===
    
    function startWorkflowUpdates(workflowType) {
        // Arrêter l'ancien interval s'il existe
        if (workflowUpdateIntervals[workflowType]) {
            clearInterval(workflowUpdateIntervals[workflowType]);
        }
        
        // Démarrer nouveau cycle de mises à jour
        workflowUpdateIntervals[workflowType] = setInterval(() => {
            loadWorkflowData(workflowType).catch(console.error);
        }, 15000); // Mise à jour toutes les 15 secondes
    }
    
    function stopWorkflowUpdates(workflowType) {
        if (workflowUpdateIntervals[workflowType]) {
            clearInterval(workflowUpdateIntervals[workflowType]);
            delete workflowUpdateIntervals[workflowType];
        }
    }
    
    // === ACTIONS UTILISATEUR ===
    
    async function forceWorkflowExecution(workflowType) {
        try {
            const response = await fetch(`/api/workflows/${workflowType}/force-execute`, {
                method: 'POST'
            });
            
            const result = await response.json();
            
            if (response.ok) {
                showSuccessMessage(`Exécution forcée du workflow ${workflowType} démarrée`);
                // Recharger les données immédiatement
                setTimeout(() => loadWorkflowData(workflowType), 1000);
            } else {
                throw new Error(result.detail || 'Erreur');
            }
        } catch (error) {
            showErrorMessage(`Erreur lors du forçage du workflow: ${error.message}`);
        }
    }
    
    async function exportWorkflowData(workflowType) {
        try {
            const response = await fetch(`/api/workflows/${workflowType}/export`);
            const blob = await response.blob();
            
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `${workflowType}_workflow_data_${new Date().toISOString().split('T')[0]}.json`;
            
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            
            showSuccessMessage(`Données du workflow ${workflowType} exportées`);
        } catch (error) {
            showErrorMessage(`Erreur lors de l'export: ${error.message}`);
        }
    }
    
    // === FONCTIONS UTILITAIRES ===
    
    function updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
    
    function formatNextScanTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    function formatVolume(volume) {
        if (volume >= 1e9) return (volume / 1e9).toFixed(1) + 'B';
        if (volume >= 1e6) return (volume / 1e6).toFixed(1) + 'M';
        if (volume >= 1e3) return (volume / 1e3).toFixed(1) + 'K';
        return volume.toString();
    }
    
    function formatTimeAgo(timestamp) {
        const now = new Date();
        const time = new Date(timestamp);
        const diffMs = now - time;
        const diffMins = Math.floor(diffMs / 60000);
        
        if (diffMins < 1) return 'maintenant';
        if (diffMins < 60) return `il y a ${diffMins} min`;
        
        const diffHours = Math.floor(diffMins / 60);
        if (diffHours < 24) return `il y a ${diffHours}h`;
        
        const diffDays = Math.floor(diffHours / 24);
        return `il y a ${diffDays}j`;
    }
    
    function showSuccessMessage(message) {
        // TODO: Implémenter système de notifications
        console.log('SUCCESS:', message);
    }
    
    function showErrorMessage(message) {
        // TODO: Implémenter système de notifications  
        console.error('ERROR:', message);
    }
    
    // === NETTOYAGE ===
    
    function cleanupWorkflowPage(workflowType) {
        stopWorkflowUpdates(workflowType);
        delete currentWorkflowData[workflowType];
    }
    
    // Nettoyage général au changement de page
    function cleanupAllWorkflows() {
        Object.keys(workflowUpdateIntervals).forEach(stopWorkflowUpdates);
        currentWorkflowData = {};
    }
    
    // === GESTION DES ONGLETS ===
    
    function showCryptoTab(tabName) {
        // Masquer tous les contenus d'onglets crypto
        document.querySelectorAll('#crypto-workflow-page .tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Désactiver tous les boutons d'onglets crypto
        document.querySelectorAll('#crypto-workflow-page .tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Afficher l'onglet sélectionné
        const targetTab = document.getElementById(`crypto-tab-${tabName}`);
        if (targetTab) {
            targetTab.classList.add('active');
        }
        
        // Activer le bouton correspondant
        const targetBtn = document.querySelector(`#crypto-workflow-page .tab-btn[onclick="showCryptoTab('${tabName}')"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
        
        // Charger les données si nécessaire
        if (tabName !== 'overview') {
            loadWorkflowData('crypto');
        }
    }
    
    function showMemeTab(tabName) {
        // Masquer tous les contenus d'onglets meme
        document.querySelectorAll('#meme-workflow-page .tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Désactiver tous les boutons d'onglets meme
        document.querySelectorAll('#meme-workflow-page .tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Afficher l'onglet sélectionné
        const targetTab = document.getElementById(`meme-tab-${tabName}`);
        if (targetTab) {
            targetTab.classList.add('active');
        }
        
        // Activer le bouton correspondant
        const targetBtn = document.querySelector(`#meme-workflow-page .tab-btn[onclick="showMemeTab('${tabName}')"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
        
        // Charger les données si nécessaire
        if (tabName !== 'overview') {
            loadWorkflowData('meme');
        }
    }
    
    function showForexTab(tabName) {
        // Masquer tous les contenus d'onglets forex
        document.querySelectorAll('#forex-workflow-page .tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Désactiver tous les boutons d'onglets forex
        document.querySelectorAll('#forex-workflow-page .tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Afficher l'onglet sélectionné
        const targetTab = document.getElementById(`forex-tab-${tabName}`);
        if (targetTab) {
            targetTab.classList.add('active');
        }
        
        // Activer le bouton correspondant
        const targetBtn = document.querySelector(`#forex-workflow-page .tab-btn[onclick="showForexTab('${tabName}')"]`);
        if (targetBtn) {
            targetBtn.classList.add('active');
        }
        
        // Charger les données si nécessaire
        if (tabName !== 'overview') {
            loadWorkflowData('forex');
        }
    }
    """ 