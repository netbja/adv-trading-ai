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

async function loadWorkflowPage(workflowType) {
    console.log(`Chargement de la page de workflow: ${workflowType}`);
    const pageContentDiv = document.getElementById(`${workflowType}-workflow-page`);
    if (!pageContentDiv) {
        console.error(`Conteneur de page pour ${workflowType}-workflow-page non trouvé.`);
        return;
    }

    try {
        // Étape 1: Essayer de récupérer le contenu HTML pré-rendu d'une API
        // Nous devrons créer ces endpoints API dans trading_ai_complete.py
        // Exemple: /api/pages/crypto-workflow-content
        // const response = await fetch(`/api/pages/${workflowType}-workflow-content`);
        // if (!response.ok) throw new Error(`Erreur chargement HTML pour ${workflowType}`);
        // const htmlContent = await response.text();
        // pageContentDiv.innerHTML = htmlContent;

        // Pour l'instant, on affiche juste un message placeholder
        const title = pageTitles[`${workflowType}-workflow`] || `Workflow ${workflowType}`;
        pageContentDiv.innerHTML = `<h2>${title}</h2><p>Le chargement dynamique du contenu de cette page est en cours de développement.</p><p>Les données spécifiques à ce workflow (venant de <code>/api/workflows/${workflowType}/details</code>) seront chargées et affichées ici.</p>`;
        
        // Étape 2 (future): Charger les données spécifiques au workflow (ex: /api/workflows/crypto/details)
        // et les utiliser pour peupler/mettre à jour le contenu HTML chargé à l'étape 1.
        // const detailsResponse = await fetch(`/api/workflows/${workflowType}/details`);
        // if (!detailsResponse.ok) throw new Error (\`Erreur chargement détails pour ${workflowType}\`);
        // const detailsData = await detailsResponse.json();
        // populateWorkflowDetails(workflowType, detailsData); // Une nouvelle fonction à créer

        // Étape 3 (future): Initialiser les graphiques ou autres éléments interactifs spécifiques à ce workflow
        // if (typeof initCryptoCharts === 'function') initCryptoCharts();

    } catch (error) {
        console.error(`Erreur chargement page workflow ${workflowType}:`, error);
        pageContentDiv.innerHTML = `<p class="error-message" style="display:block; background: #fee2e2; color: #dc2626; padding: 1rem; border-radius: 0.5rem;">Erreur de chargement du contenu pour ${workflowType}.</p>`;
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
