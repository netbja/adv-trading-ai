console.log('Dashboard JS V2 chargé');

let currentPage = 'overview';
const pageTitles = {
    'overview': "Vue d'ensemble",
    'capital': 'Capital & Performance',
    'crypto-workflow': 'Workflow Crypto Principal',
    'meme-workflow': 'Workflow Crypto Meme',
    'forex-workflow': 'Workflow Forex Trading',
    'wallets': 'Wallets & Secrets',
    'settings': 'Paramètres',
    'logs': 'Logs Système'
};

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM entièrement chargé et analysé");

    // Charger les données utilisateur initiales
    loadUserData();

    // Configurer les liens de navigation
    const navLinks = document.querySelectorAll('.nav-link[data-page]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const pageId = this.dataset.page;
            if (pageId) {
                showPage(pageId);
            }
        });
        link.setAttribute('role', 'button');
        link.setAttribute('tabindex', '0');
        link.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });

    // Bouton de déconnexion
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    // Bouton d'actualisation
    const refreshButton = document.getElementById('refresh-data-button');
    if (refreshButton) {
        refreshButton.addEventListener('click', refreshDashboardData);
    }

    // Charger les données de la page initiale (overview)
    showPage(currentPage); // Assure le chargement de la vue d'ensemble initiale
    // startAutoRefresh(); // Activer si souhaité
});

function showPage(pageId) {
    console.log(`Affichage de la page: ${pageId}`);
    // Nettoyer les anciens workflows (si implémenté)
    // if (currentPage.includes('workflow')) {
    //     cleanupWorkflowPage(currentPage.replace('-page', '')); 
    // }

    document.querySelectorAll('.page-content').forEach(page => {
        page.classList.remove('active');
    });
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    const targetPage = document.getElementById(pageId + '-page');
    if (targetPage) {
        targetPage.classList.add('active');
    } else {
        console.warn(`Page avec ID ${pageId}-page non trouvée.`);
        // Optionnel: rediriger vers une page d'erreur ou la page d'accueil
        // document.getElementById('overview-page').classList.add('active'); 
    }

    const activeNavLink = document.querySelector(`.nav-link[data-page="${pageId}"]`);
    if (activeNavLink) {
        activeNavLink.classList.add('active');
    }

    const titleElement = document.getElementById('page-title');
    if (titleElement) {
        titleElement.textContent = pageTitles[pageId] || pageId.charAt(0).toUpperCase() + pageId.slice(1);
    }

    currentPage = pageId;
    loadPageData(pageId);
    window.scrollTo(0, 0);
}

function startAutoRefresh() {
    setInterval(() => {
        if (currentPage === 'overview') {
            loadOverviewData();
        }
        // Pourrait être étendu pour rafraîchir les pages de workflow aussi
    }, 30000); // Toutes les 30 secondes
}

async function loadUserData() {
    try {
        const response = await fetch('/api/dashboard'); // Réutilise l'endpoint existant qui contient les user_data
        if (!response.ok) {
            if (response.status === 401) {
                // Gérer non authentifié - potentiellement rediriger vers login, bien que le backend devrait déjà le faire.
                console.warn("Utilisateur non authentifié pour récupérer les données utilisateur.");
                // window.location.href = '/'; // Redirige vers la page qui gère login/dashboard
                return;
            }
            throw new Error(`Erreur API (statut ${response.status})`);
        }
        const data = await response.json();
        if (data.user && data.user.username) {
            const usernameDisplay = document.getElementById('username-display');
            if (usernameDisplay) {
                usernameDisplay.textContent = `Connecté: ${data.user.username} (${data.user.role || 'Utilisateur'})`;
            }
        } else {
            console.warn("Données utilisateur non trouvées dans la réponse de /api/dashboard");
        }
    } catch (error) {
        console.error("Erreur de chargement des données utilisateur:", error);
        const usernameDisplay = document.getElementById('username-display');
        if (usernameDisplay) {
            usernameDisplay.textContent = "Erreur chargement utilisateur";
        }
    }
}

async function loadPageData(pageId) {
    console.log(`Chargement des données pour la page: ${pageId}`);
    try {
        if (pageId === 'overview') {
            await loadOverviewData();
        } else if (pageId.endsWith('-workflow')) {
            const workflowType = pageId.replace('-workflow', '');
            await loadWorkflowPage(workflowType); // Fonction à implémenter pour charger le contenu HTML des workflows
        } else {
            // Pour les autres pages comme capital, wallets, settings, logs
            // elles ont un contenu statique "En développement" pour l'instant.
            console.log(`Page ${pageId} - Contenu statique affiché.`);
        }
    } catch (error) {
        console.error(`Erreur chargement page ${pageId}:`, error);
        showNotification('Erreur de chargement des données de la page', 'error');
    }
}

async function loadOverviewData() {
    console.log("Chargement des données de l'aperçu...");
    const lastUpdateElement = document.getElementById('last-update');
    if (lastUpdateElement) lastUpdateElement.textContent = 'Chargement...';

    try {
        const dashResponse = await fetch('/api/dashboard');
        if (!dashResponse.ok) throw new Error(`Erreur API dashboard (statut ${dashResponse.status})`);
        const dashData = await dashResponse.json();

        updateMetricWithAnimation('current-capital', dashData.capital_growth.current.toFixed(2) + '€');
        updateMetricWithAnimation('total-return', 
            (dashData.capital_growth.total_return_pct > 0 ? '+' : '') + 
            dashData.capital_growth.total_return_pct.toFixed(1) + '%');
        updateMetricWithAnimation('system-efficiency', 
            dashData.capital_growth.system_efficiency_pct.toFixed(0) + '%');
        updateMetricWithAnimation('system-uptime', 
            dashData.uptime_days + (dashData.uptime_days > 1 ? ' jours' : ' jour'));
        
        // Mettre à jour "Workflows Actifs" - à affiner selon ce que l'API renvoie
        // Pour l'instant, on va supposer 3, mais ce serait mieux si l'API le donnait.
        updateMetricWithAnimation('active-workflows', '3'); 

        const workflowStatusResponse = await fetch('/api/workflows/live-status');
        if (!workflowStatusResponse.ok) throw new Error(`Erreur API workflow status (statut ${workflowStatusResponse.status})`);
        const workflowStatusData = await workflowStatusResponse.json();
        
        updateWorkflowCardData(workflowStatusData);
        updateRecentActivity(workflowStatusData); // Gardons cette fonction, même si elle est simple pour l'instant

        if (lastUpdateElement) lastUpdateElement.textContent = 'Dernière MAJ: ' + new Date().toLocaleTimeString();

    } catch (error) {
        console.error('Erreur chargement données aperçu:', error);
        showNotification('Erreur de connexion aux données de l\'aperçu', 'error');
        if (lastUpdateElement) lastUpdateElement.textContent = 'Erreur de connexion';
    }
}

function updateMetricWithAnimation(elementId, value) {
    const element = document.getElementById(elementId);
    if (element && element.textContent !== value) {
        element.style.opacity = '0';
        setTimeout(() => {
            element.textContent = value;
            element.style.opacity = '1';
        }, 150);
    }
}

function updateWorkflowCardData(data) {
    console.log("Mise à jour des cartes de workflow avec:", data);

    // Crypto Card
    if (data.crypto) {
        const cryptoSignals = document.getElementById('crypto-signals-today');
        const cryptoPerf = document.getElementById('crypto-perf-7d');
        const statusDot = document.getElementById('dot-crypto-workflow');
        const statusText = document.getElementById('text-crypto-workflow');
        const statusIndicatorSidebar = document.getElementById('status-crypto-workflow');

        if (cryptoSignals) cryptoSignals.textContent = data.crypto.performance?.total_trades || '--';
        if (cryptoPerf) cryptoPerf.textContent = (data.crypto.performance?.gain_percentage > 0 ? '+' : '') + (data.crypto.performance?.gain_percentage || 0).toFixed(1) + '%';
        
        updateStatusDisplay(data.crypto.status, statusDot, statusText, statusIndicatorSidebar);
    }
    
    // Meme Card
    if (data.meme) {
        const memeTokens = document.getElementById('meme-tokens-scanned');
        const memeRisk = document.getElementById('meme-risk-level');
        const statusDot = document.getElementById('dot-meme-workflow');
        const statusText = document.getElementById('text-meme-workflow');
        const statusIndicatorSidebar = document.getElementById('status-meme-workflow');

        // L'API actuelle pour /live-status ne fournit pas ces détails spécifiques pour les cartes.
        // Ces lignes sont des placeholders pour quand l'API sera mise à jour ou les données calculées autrement.
        if (memeTokens) memeTokens.textContent = data.meme.performance?.tokens_scanned_today || '--'; 
        if (memeRisk) memeRisk.textContent = data.meme.performance?.risk_level || 'N/A'; 

        updateStatusDisplay(data.meme.status, statusDot, statusText, statusIndicatorSidebar);
    }

    // Forex Card
    if (data.forex) {
        const forexStrength = document.getElementById('forex-usd-strength');
        const forexPerf = document.getElementById('forex-perf-24h');
        const statusDot = document.getElementById('dot-forex-workflow');
        const statusText = document.getElementById('text-forex-workflow');
        const statusIndicatorSidebar = document.getElementById('status-forex-workflow');
        
        // Mêmes remarques que pour la carte Meme concernant les données spécifiques.
        if (forexStrength) forexStrength.textContent = data.forex.performance?.usd_strength_index || '--.--';
        if (forexPerf) forexPerf.textContent = (data.forex.performance?.daily_gain_percentage > 0 ? '+' : '') + (data.forex.performance?.daily_gain_percentage || 0).toFixed(1) + '%';
        
        updateStatusDisplay(data.forex.status, statusDot, statusText, statusIndicatorSidebar);
    }
}

// Helper function to update status display for cards and sidebar indicators
function updateStatusDisplay(status, dotElement, textElement, sidebarIndicatorElement) {
    if (!dotElement || !textElement) return;

    dotElement.className = 'status-dot'; // Reset dot classes
    if (sidebarIndicatorElement) sidebarIndicatorElement.className = 'status-indicator'; // Reset sidebar indicator classes

    switch (status) {
        case 'active':
        case 'idle': // Traiter idle comme active pour l'affichage pour l'instant
            dotElement.classList.add('status-active');
            textElement.textContent = 'Actif';
            if (sidebarIndicatorElement) sidebarIndicatorElement.classList.add('status-active');
            break;
        case 'scanning':
            dotElement.classList.add('status-scanning');
            textElement.textContent = 'Scan en cours';
            if (sidebarIndicatorElement) sidebarIndicatorElement.classList.add('status-scanning', 'pulse');
            break;
        default:
            dotElement.classList.add('status-idle'); // Un gris par défaut
            textElement.textContent = status || 'Inconnu';
            if (sidebarIndicatorElement) sidebarIndicatorElement.classList.add('status-idle');
            break;
    }
}

function updateRecentActivity(data) {
    const activityContainer = document.getElementById('recent-activity');
    if (!activityContainer) return;

    // Pour l'instant, on ne génère pas d'activité détaillée. 
    // On garde le placeholder ou on met un message simple.
    // La logique de l'ancienne f-string était complexe à reproduire sans les données exactes.
    let htmlContent = `
        <div class="no-activity">
            <div class="no-activity-icon">📊</div>
            <div class="no-activity-text">Activité des workflows</div>
            <div class="no-activity-sub">Statuts live: Crypto (${data.crypto?.status || 'N/A'}), Meme (${data.meme?.status || 'N/A'}), Forex (${data.forex?.status || 'N/A'})</div>
        </div>
    `;
    // Si on veut lister des activités (nécessiterait que l'API renvoie une liste d'activités)
    // if (data.recent_logs && data.recent_logs.length > 0) {
    //     htmlContent = data.recent_logs.map(log => {
    //         // Exemple de structure d'un item d'activité (à adapter)
    //         const typeClass = log.type === 'success' ? 'activity-success' : log.type === 'error' ? 'activity-error' : 'activity-info';
    //         const icon = log.type === 'success' ? '✅' : log.type === 'error' ? '❌' : 'ℹ️';
    //         return \`
    //             <div class="activity-item ${typeClass}">
    //                 <div class="activity-icon-wrapper">
    //                     <div class="activity-icon">${icon}</div>
    //                 </div>
    //                 <div class="activity-content">
    //                     <div class="activity-header">
    //                         <span class="activity-title">${log.title || 'Événement système'}</span>
    //                         <span class="activity-time">${new Date(log.timestamp).toLocaleTimeString()}</span>
    //                     </div>
    //                     <p class="activity-description">${log.message || 'Aucune description.'}</p>
    //                 </div>
    //             </div>
    //         \`;
    //     }).join('');
    // } 
    activityContainer.innerHTML = htmlContent;
}

function buildCryptoWorkflowHTML(data) {
    let html = `<h2><span class="nav-icon">₿</span> Workflow Crypto Principal</h2>`;

    // Section Métriques Clés
    html += `
        <div class="workflow-metrics-grid">
            <div class="metric-card">
                <span class="metric-value">${data.pairs_monitored || 'N/A'}</span>
                <span class="metric-label">Paires Monitorées</span>
            </div>
            <div class="metric-card">
                <span class="metric-value">${data.signals_today || 'N/A'}</span>
                <span class="metric-label">Signaux Aujourd'hui</span>
            </div>
            <div class="metric-card">
                <span class="metric-value">${(data.avg_confidence * 100).toFixed(0) || 'N/A'}%</span>
                <span class="metric-label">Confiance Moyenne</span>
            </div>
            <div class="metric-card">
                <span class="metric-value">${data.next_scan_in_seconds ? (data.next_scan_in_seconds / 60).toFixed(1) + ' min' : 'N/A'}</span>
                <span class="metric-label">Prochain Scan</span>
            </div>
        </div>
    `;

    // Section Exécution en Cours
    html += `<h3><span class="section-icon">⚙️</span> Exécution en Cours</h3>`;
    if (data.current_execution) {
        html += `
            <div class="execution-details">
                <p><strong>Statut:</strong> ${data.current_execution.status || 'N/A'}</p>
                <p><strong>Début:</strong> ${new Date(data.current_execution.start_time).toLocaleString() || 'N/A'}</p>
                <p><strong>Détails:</strong> ${data.current_execution.details || 'Aucun'}</p>
            </div>`;
    } else {
        html += `<p>Aucune exécution en cours.</p>`;
    }

    // Section Données des Paires
    html += `<h3><span class="section-icon">📈</span> Données des Paires</h3>`;
    if (data.pairs_data && Object.keys(data.pairs_data).length > 0) {
        html += `
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Paire</th>
                            <th>Prix</th>
                            <th>Variation 24h</th>
                            <th>Volume 24h</th>
                        </tr>
                    </thead>
                    <tbody>`;
        for (const pair in data.pairs_data) {
            const pData = data.pairs_data[pair];
            html += `
                        <tr>
                            <td>${pair}</td>
                            <td>${pData.price !== undefined ? pData.price.toFixed(2) : 'N/A'}</td>
                            <td class="${pData.change_24h > 0 ? 'positive' : pData.change_24h < 0 ? 'negative' : ''}">${pData.change_24h !== undefined ? pData.change_24h.toFixed(2) + '%' : 'N/A'}</td>
                            <td>${pData.volume_24h !== undefined ? pData.volume_24h.toLocaleString() : 'N/A'}</td>
                        </tr>`;
        }
        html += `
                    </tbody>
                </table>
            </div>`;
    } else {
        html += `<p>Aucune donnée de paires disponible.</p>`;
    }

    // Section Signaux Récents
    html += `<h3><span class="section-icon">🔔</span> Signaux Récents</h3>`;
    if (data.recent_signals && data.recent_signals.length > 0) {
        html += `
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Date/Heure</th>
                            <th>Paire</th>
                            <th>Type</th>
                            <th>Prix d'entrée</th>
                            <th>Confiance</th>
                        </tr>
                    </thead>
                    <tbody>`;
        data.recent_signals.forEach(signal => {
            html += `
                        <tr>
                            <td>${new Date(signal.timestamp).toLocaleString()}</td>
                            <td>${signal.pair}</td>
                            <td>${signal.type}</td>
                            <td>${signal.entry_price !== undefined ? signal.entry_price.toFixed(2) : 'N/A'}</td>
                            <td>${signal.confidence_score !== undefined ? (signal.confidence_score * 100).toFixed(0) + '%' : 'N/A'}</td>
                        </tr>`;
        });
        html += `
                    </tbody>
                </table>
            </div>`;
    } else {
        html += `<p>Aucun signal récent.</p>`;
    }
    
    // Section Actions
    html += `
        <h3><span class="section-icon">🛠️</span> Actions</h3>
        <div class="workflow-actions">
            <button class="btn btn-primary" onclick="forceExecuteWorkflow('crypto')">Forcer Exécution</button>
            <button class="btn btn-secondary" onclick="exportWorkflowData('crypto')">Exporter Données</button>
        </div>
    `;

    return html;
}

async function forceExecuteWorkflow(workflowType) {
    if (!confirm(`Êtes-vous sûr de vouloir forcer l'exécution du workflow ${workflowType} ?`)) return;
    try {
        const response = await fetch(`/api/workflows/${workflowType}/force-execute`, { method: 'POST' });
        const result = await response.json();
        if (!response.ok) throw new Error(result.detail || 'Erreur serveur');
        showNotification(result.message || `Exécution forcée de ${workflowType} démarrée.`, 'success');
        loadWorkflowPage(workflowType); 
    } catch (error) {
        console.error(`Erreur lors de la forçage d'exécution pour ${workflowType}:`, error);
        showNotification(`Erreur: ${error.message}`, 'error');
    }
}

async function exportWorkflowData(workflowType) {
    try {
        const response = await fetch(`/api/workflows/${workflowType}/export`);
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Erreur lors de l\'exportation');
        }
        const blob = await response.blob();
        const filename = response.headers.get('content-disposition')?.split('filename=')[1]?.replace(/"/g, '') || `${workflowType}_export.json`;
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
        showNotification('Exportation des données terminée.', 'success');
    } catch (error) {
        console.error(`Erreur lors de l'exportation pour ${workflowType}:`, error);
        showNotification(`Erreur d'exportation: ${error.message}`, 'error');
    }
}

async function loadWorkflowPage(workflowType) {
    console.log(`Chargement de la page de workflow: ${workflowType}`);
    const pageContentDiv = document.getElementById(`${workflowType}-workflow-page`);
    if (!pageContentDiv) {
        console.error(`Conteneur de page pour ${workflowType}-workflow-page non trouvé.`);
        return;
    }

    // Affiche un spinner ou un message de chargement
    pageContentDiv.innerHTML = `<h2>${pageTitles[workflowType + '-workflow'] || workflowType}</h2><div class="loading-spinner">Chargement des données du workflow...</div>`;

    try {
        if (workflowType === 'crypto') {
            const response = await fetch(`/api/workflows/crypto/details`);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ detail: 'Erreur inconnue lors de la récupération des détails.' }));
                throw new Error(`Erreur ${response.status}: ${errorData.detail}`);
            }
            const data = await response.json();
            pageContentDiv.innerHTML = buildCryptoWorkflowHTML(data);
        } else if (workflowType === 'meme') {
            // TODO: Implémenter pour Meme workflow
            pageContentDiv.innerHTML = `<h2>${pageTitles['meme-workflow']}</h2><p>Le chargement dynamique pour le workflow Meme est en cours de développement.</p><p>Données attendues de <code>/api/workflows/meme/details</code>.</p>`;
             // Exemple d'appel (quand prêt):
            // const response = await fetch(`/api/workflows/meme/details`);
            // if (!response.ok) throw new Error('Erreur chargement détails Meme');
            // const data = await response.json();
            // pageContentDiv.innerHTML = buildMemeWorkflowHTML(data); // buildMemeWorkflowHTML à créer
        } else if (workflowType === 'forex') {
            // TODO: Implémenter pour Forex workflow
            pageContentDiv.innerHTML = `<h2>${pageTitles['forex-workflow']}</h2><p>Le chargement dynamique pour le workflow Forex est en cours de développement.</p><p>Données attendues de <code>/api/workflows/forex/details</code>.</p>`;
            // Exemple d'appel (quand prêt):
            // const response = await fetch(`/api/workflows/forex/details`);
            // if (!response.ok) throw new Error('Erreur chargement détails Forex');
            // const data = await response.json();
            // pageContentDiv.innerHTML = buildForexWorkflowHTML(data); // buildForexWorkflowHTML à créer
        } else {
            pageContentDiv.innerHTML = `<h2>Workflow Inconnu</h2><p>Ce type de workflow n'est pas géré.</p>`;
        }

        // Optionnel: Initialiser des graphiques ou autres éléments interactifs spécifiques à ce workflow
        // if (workflowType === 'crypto' && typeof initCryptoCharts === 'function') initCryptoCharts(data);

    } catch (error) {
        console.error(`Erreur chargement page workflow ${workflowType}:`, error);
        let titleForError = "Erreur";
        if (pageTitles[workflowType + '-workflow']) {
            titleForError = pageTitles[workflowType + '-workflow'];
        } else {
            titleForError = workflowType;
        }
        
        let msgText = "Erreur de chargement du contenu.";
        if (error && error.message) {
            msgText = error.message;
        }

        pageContentDiv.innerHTML = "<h2>" + titleForError + "</h2>" +
                                 "<p class=\"error-message\" style=\"display:block; background: #fee2e2; color: #dc2626; padding: 1rem; border-radius: 0.5rem;\">" +
                                 "Erreur pour " + workflowType + ": " + msgText + "</p>";
    }
}

async function refreshDashboardData() {
    if (currentPage === 'overview') {
        await loadOverviewData();
    } else if (currentPage.endsWith('-workflow')) {
        const workflowType = currentPage.replace('-workflow', '');
        await loadWorkflowPage(workflowType); // Recharge la page workflow actuelle
    }
    // Ajouter d'autres logiques de refresh si nécessaire pour d'autres pages
    showNotification('Données actualisées', 'success');
}

function logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        // Supprimer le cookie de session
        document.cookie = 'session_token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT; SameSite=Lax';
        // Recharger la page, le backend devrait rediriger vers la page de connexion
        window.location.reload();
    }
}

// Système de notifications amélioré
function showNotification(message, type = 'info') {
    const notificationArea = document.body; // Ou un conteneur dédié si vous en avez un
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Les styles sont dans style.css, mais on ajoute la classe pour l'animation
    notificationArea.appendChild(notification);
    
    // Forcer le reflow pour que la transition s'applique
    void notification.offsetWidth;

    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300); // Attendre la fin de la transition de sortie
    }, 3000); // Durée d'affichage
}
