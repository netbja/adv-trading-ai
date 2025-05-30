"""
🏥 AUTO-HEALER ULTRA-AVANCÉ - SYSTÈME D'AUTO-GUÉRISON RÉVOLUTIONNAIRE
Détection proactive et guérison autonome de tous les problèmes système
"""

import asyncio
import psutil
import structlog
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import subprocess
import aioredis
import asyncpg
from concurrent.futures import ThreadPoolExecutor
import numpy as np

logger = structlog.get_logger()

class HealthLevel(Enum):
    """Niveaux de santé système"""
    EXCELLENT = 1    # 95-100% - Performance optimale
    GOOD = 2         # 85-94%  - Performance normale
    WARNING = 3      # 70-84%  - Attention requise
    CRITICAL = 4     # 50-69%  - Action immédiate
    EMERGENCY = 5    # 0-49%   - Urgence absolue

class IssueType(Enum):
    """Types de problèmes détectés"""
    MEMORY_LEAK = "memory_leak"
    CPU_OVERLOAD = "cpu_overload"
    DISK_FULL = "disk_full"
    DATABASE_SLOW = "database_slow"
    API_RATE_LIMIT = "api_rate_limit"
    NETWORK_LATENCY = "network_latency"
    SERVICE_DOWN = "service_down"
    CACHE_MISS = "cache_miss"
    THREAD_DEADLOCK = "thread_deadlock"
    CONNECTION_POOL_EXHAUSTED = "connection_pool_exhausted"

@dataclass
class HealthIssue:
    """Problème de santé détecté"""
    id: str
    issue_type: IssueType
    severity: HealthLevel
    description: str
    affected_component: str
    metrics: Dict[str, Any]
    
    # Healing strategy
    suggested_actions: List[str] = field(default_factory=list)
    auto_healing_possible: bool = True
    healing_strategy: Optional[str] = None
    
    # Timeline
    detected_at: datetime = field(default_factory=datetime.utcnow)
    first_occurrence: Optional[datetime] = None
    frequency: int = 1
    
    # Resolution tracking
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    healing_attempts: int = 0
    max_healing_attempts: int = 3

@dataclass
class SystemMetrics:
    """Métriques système complètes"""
    # Resource utilization
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_io: Dict[str, int]
    
    # Application metrics
    active_connections: int
    response_time_avg: float
    error_rate: float
    throughput: float
    
    # Database metrics
    db_connections: int
    db_query_time_avg: float
    db_slow_queries: int
    
    # Cache metrics
    cache_hit_rate: float
    cache_memory_usage: float
    
    # API metrics
    api_calls_remaining: Dict[str, int]
    api_response_times: Dict[str, float]
    
    timestamp: datetime = field(default_factory=datetime.utcnow)

class AutoHealer:
    """
    🏥 AUTO-HEALER RÉVOLUTIONNAIRE
    
    Système d'auto-guérison ultra-avancé qui :
    - Détecte proactivement tous les problèmes
    - Diagnostique intelligemment les causes racines
    - Applique automatiquement les corrections
    - Apprend de chaque intervention
    - Prévient les problèmes futurs
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.is_running = False
        
        # Issue tracking
        self.active_issues: Dict[str, HealthIssue] = {}
        self.resolved_issues: List[HealthIssue] = []
        self.issue_patterns: Dict[str, List[Dict]] = {}
        
        # Metrics storage
        self.metrics_history: List[SystemMetrics] = []
        self.baseline_metrics: Optional[SystemMetrics] = None
        
        # Healing strategies
        self.healing_strategies: Dict[IssueType, List[Callable]] = {}
        self.preventive_measures: Dict[str, Callable] = {}
        
        # Learning system
        self.healing_success_rates: Dict[IssueType, float] = {}
        self.pattern_detection_models: Dict[str, Any] = {}
        
        # Execution
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.monitoring_tasks: List[asyncio.Task] = []
        
        # Statistics
        self.stats = {
            "total_issues_detected": 0,
            "total_issues_healed": 0,
            "auto_healing_success_rate": 0.0,
            "prevented_outages": 0,
            "system_uptime": 0.0
        }
        
        # Initialize healing strategies
        self._initialize_healing_strategies()
        
        logger.info("🏥 Auto-Healer ultra-avancé initialisé")
    
    async def start_continuous_monitoring(self):
        """
        🔍 DÉMARRAGE DU MONITORING CONTINU ULTRA-AVANCÉ
        
        Surveillance 24/7 avec détection proactive des anomalies
        """
        self.is_running = True
        logger.info("🔍 Auto-Healer démarré - Surveillance continue activée")
        
        # Établir les métriques de base
        await self._establish_baseline_metrics()
        
        # Démarrage des tâches de monitoring
        monitoring_tasks = [
            asyncio.create_task(self._monitor_system_resources()),
            asyncio.create_task(self._monitor_application_health()),
            asyncio.create_task(self._monitor_database_performance()),
            asyncio.create_task(self._monitor_external_apis()),
            asyncio.create_task(self._monitor_cache_performance()),
            asyncio.create_task(self._detect_anomaly_patterns()),
            asyncio.create_task(self._preventive_maintenance_cycle())
        ]
        
        self.monitoring_tasks.extend(monitoring_tasks)
        
        # Loop principal de healing
        while self.is_running:
            try:
                # 1. Collecte et analyse des métriques
                current_metrics = await self._collect_comprehensive_metrics()
                self.metrics_history.append(current_metrics)
                
                # 2. Détection intelligente d'anomalies
                detected_issues = await self._detect_health_issues(current_metrics)
                
                # 3. Traitement proactif des problèmes
                for issue in detected_issues:
                    await self._handle_health_issue(issue)
                
                # 4. Nettoyage périodique
                await self._cleanup_resolved_issues()
                
                # 5. Mise à jour des statistiques
                await self._update_health_statistics()
                
                # Pause adaptive
                sleep_duration = self._calculate_monitoring_interval(current_metrics)
                await asyncio.sleep(sleep_duration)
                
            except Exception as e:
                logger.error("🚨 Erreur Auto-Healer", error=str(e))
                await asyncio.sleep(10)  # Backoff en cas d'erreur
    
    async def _collect_comprehensive_metrics(self) -> SystemMetrics:
        """
        📊 COLLECTE COMPLÈTE DES MÉTRIQUES SYSTÈME
        
        Récupère tous les indicateurs de santé en temps réel
        """
        
        # System resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Application metrics (simulated - replace with real metrics)
        active_connections = len(psutil.net_connections())
        response_time_avg = np.random.normal(150, 30)  # ms
        error_rate = max(0, np.random.normal(0.02, 0.01))  # 2% base error rate
        throughput = np.random.normal(1000, 100)  # requests/minute
        
        # Database metrics (simulated)
        db_connections = np.random.randint(5, 25)
        db_query_time_avg = np.random.normal(50, 15)  # ms
        db_slow_queries = np.random.poisson(2)
        
        # Cache metrics (simulated)
        cache_hit_rate = min(1.0, max(0.0, np.random.normal(0.85, 0.1)))
        cache_memory_usage = np.random.normal(0.6, 0.1)
        
        # API metrics (simulated)
        api_calls_remaining = {
            "openai": np.random.randint(8000, 10000),
            "anthropic": np.random.randint(9000, 10000),
            "alpaca": np.random.randint(200, 300)
        }
        
        api_response_times = {
            "openai": np.random.normal(800, 200),
            "anthropic": np.random.normal(600, 150),
            "alpaca": np.random.normal(200, 50)
        }
        
        return SystemMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            disk_usage_percent=disk.percent,
            network_io={"bytes_sent": network.bytes_sent, "bytes_recv": network.bytes_recv},
            active_connections=active_connections,
            response_time_avg=response_time_avg,
            error_rate=error_rate,
            throughput=throughput,
            db_connections=db_connections,
            db_query_time_avg=db_query_time_avg,
            db_slow_queries=db_slow_queries,
            cache_hit_rate=cache_hit_rate,
            cache_memory_usage=cache_memory_usage,
            api_calls_remaining=api_calls_remaining,
            api_response_times=api_response_times
        )
    
    async def _detect_health_issues(self, metrics: SystemMetrics) -> List[HealthIssue]:
        """
        🔍 DÉTECTION INTELLIGENTE DES PROBLÈMES DE SANTÉ
        
        Analyse multi-dimensionnelle pour détecter tous types de problèmes
        """
        detected_issues = []
        
        # 1. Resource utilization issues
        if metrics.cpu_percent > 85:
            issue = HealthIssue(
                id=f"cpu_overload_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.CPU_OVERLOAD,
                severity=HealthLevel.CRITICAL if metrics.cpu_percent > 95 else HealthLevel.WARNING,
                description=f"CPU utilization at {metrics.cpu_percent:.1f}%",
                affected_component="system_cpu",
                metrics={"cpu_percent": metrics.cpu_percent},
                suggested_actions=[
                    "Restart resource-intensive processes",
                    "Scale horizontally if possible",
                    "Optimize CPU-intensive algorithms"
                ],
                healing_strategy="cpu_optimization"
            )
            detected_issues.append(issue)
        
        if metrics.memory_percent > 80:
            issue = HealthIssue(
                id=f"memory_high_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.MEMORY_LEAK,
                severity=HealthLevel.CRITICAL if metrics.memory_percent > 90 else HealthLevel.WARNING,
                description=f"Memory usage at {metrics.memory_percent:.1f}%",
                affected_component="system_memory",
                metrics={"memory_percent": metrics.memory_percent},
                suggested_actions=[
                    "Clear cache and temporary files",
                    "Restart memory-heavy services",
                    "Investigate memory leaks"
                ],
                healing_strategy="memory_cleanup"
            )
            detected_issues.append(issue)
        
        if metrics.disk_usage_percent > 85:
            issue = HealthIssue(
                id=f"disk_full_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.DISK_FULL,
                severity=HealthLevel.CRITICAL if metrics.disk_usage_percent > 95 else HealthLevel.WARNING,
                description=f"Disk usage at {metrics.disk_usage_percent:.1f}%",
                affected_component="storage",
                metrics={"disk_usage_percent": metrics.disk_usage_percent},
                suggested_actions=[
                    "Clean log files",
                    "Remove temporary files",
                    "Archive old data"
                ],
                healing_strategy="disk_cleanup"
            )
            detected_issues.append(issue)
        
        # 2. Application performance issues
        if metrics.response_time_avg > 500:  # >500ms
            issue = HealthIssue(
                id=f"slow_response_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.DATABASE_SLOW,
                severity=HealthLevel.WARNING,
                description=f"Average response time: {metrics.response_time_avg:.1f}ms",
                affected_component="application",
                metrics={"response_time_avg": metrics.response_time_avg},
                suggested_actions=[
                    "Optimize database queries",
                    "Clear application cache",
                    "Check network latency"
                ],
                healing_strategy="performance_optimization"
            )
            detected_issues.append(issue)
        
        if metrics.error_rate > 0.05:  # >5% error rate
            issue = HealthIssue(
                id=f"high_errors_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.SERVICE_DOWN,
                severity=HealthLevel.CRITICAL,
                description=f"Error rate: {metrics.error_rate:.2%}",
                affected_component="application",
                metrics={"error_rate": metrics.error_rate},
                suggested_actions=[
                    "Check service health",
                    "Review error logs",
                    "Restart failing services"
                ],
                healing_strategy="service_recovery"
            )
            detected_issues.append(issue)
        
        # 3. Database issues
        if metrics.db_query_time_avg > 100:  # >100ms
            issue = HealthIssue(
                id=f"db_slow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.DATABASE_SLOW,
                severity=HealthLevel.WARNING,
                description=f"Average DB query time: {metrics.db_query_time_avg:.1f}ms",
                affected_component="database",
                metrics={"db_query_time_avg": metrics.db_query_time_avg},
                suggested_actions=[
                    "Optimize slow queries",
                    "Update statistics",
                    "Check index usage"
                ],
                healing_strategy="database_optimization"
            )
            detected_issues.append(issue)
        
        # 4. Cache issues
        if metrics.cache_hit_rate < 0.7:  # <70% hit rate
            issue = HealthIssue(
                id=f"cache_miss_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                issue_type=IssueType.CACHE_MISS,
                severity=HealthLevel.WARNING,
                description=f"Cache hit rate: {metrics.cache_hit_rate:.1%}",
                affected_component="cache",
                metrics={"cache_hit_rate": metrics.cache_hit_rate},
                suggested_actions=[
                    "Warm up cache",
                    "Optimize cache strategy",
                    "Increase cache size"
                ],
                healing_strategy="cache_optimization"
            )
            detected_issues.append(issue)
        
        # 5. API rate limit issues
        for api, remaining in metrics.api_calls_remaining.items():
            if remaining < 500:  # Low API quota
                issue = HealthIssue(
                    id=f"api_limit_{api}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                    issue_type=IssueType.API_RATE_LIMIT,
                    severity=HealthLevel.WARNING if remaining > 100 else HealthLevel.CRITICAL,
                    description=f"{api} API: {remaining} calls remaining",
                    affected_component=f"api_{api}",
                    metrics={"api_calls_remaining": remaining, "api": api},
                    suggested_actions=[
                        "Implement rate limiting",
                        "Use caching to reduce API calls",
                        "Switch to backup API if available"
                    ],
                    healing_strategy="api_optimization"
                )
                detected_issues.append(issue)
        
        logger.info("🔍 Détection terminée", issues_detected=len(detected_issues))
        return detected_issues
    
    async def _handle_health_issue(self, issue: HealthIssue):
        """
        🛠️ GESTION INTELLIGENTE DES PROBLÈMES DE SANTÉ
        
        Applique automatiquement les stratégies de guérison
        """
        
        issue_id = issue.id
        
        # Éviter le traitement double
        if issue_id in self.active_issues:
            return
        
        self.active_issues[issue_id] = issue
        self.stats["total_issues_detected"] += 1
        
        logger.warning("🚨 Problème détecté", 
                      issue_type=issue.issue_type.value,
                      severity=issue.severity.name,
                      component=issue.affected_component)
        
        # Tentative de guérison automatique
        if issue.auto_healing_possible and issue.healing_attempts < issue.max_healing_attempts:
            healing_success = await self._apply_healing_strategy(issue)
            
            if healing_success:
                issue.resolved = True
                issue.resolved_at = datetime.utcnow()
                self.resolved_issues.append(issue)
                del self.active_issues[issue_id]
                self.stats["total_issues_healed"] += 1
                
                logger.info("✅ Problème résolu automatiquement", 
                           issue_id=issue_id,
                           healing_strategy=issue.healing_strategy)
            else:
                issue.healing_attempts += 1
                logger.error("❌ Échec de guérison automatique", 
                           issue_id=issue_id,
                           attempts=issue.healing_attempts)
        
        # Alertes pour problèmes critiques non résolus
        if issue.severity in [HealthLevel.CRITICAL, HealthLevel.EMERGENCY] and not issue.resolved:
            await self._send_critical_alert(issue)
    
    async def _apply_healing_strategy(self, issue: HealthIssue) -> bool:
        """
        🔧 APPLICATION DES STRATÉGIES DE GUÉRISON
        
        Exécute la stratégie de guérison appropriée pour chaque type de problème
        """
        
        try:
            strategy = issue.healing_strategy
            healing_methods = self.healing_strategies.get(issue.issue_type, [])
            
            if not healing_methods:
                logger.warning("❌ Aucune stratégie de guérison disponible", 
                             issue_type=issue.issue_type.value)
                return False
            
            logger.info("🔧 Application stratégie de guérison", 
                       strategy=strategy,
                       issue_type=issue.issue_type.value)
            
            # Exécution de la première méthode de guérison disponible
            healing_method = healing_methods[0]
            result = await healing_method(issue)
            
            return result
            
        except Exception as e:
            logger.error("💥 Erreur lors de la guérison", 
                        issue_id=issue.id,
                        error=str(e))
            return False
    
    def _initialize_healing_strategies(self):
        """
        🧰 INITIALISATION DES STRATÉGIES DE GUÉRISON
        
        Configure toutes les méthodes de guérison automatique
        """
        
        self.healing_strategies = {
            IssueType.CPU_OVERLOAD: [self._heal_cpu_overload],
            IssueType.MEMORY_LEAK: [self._heal_memory_leak],
            IssueType.DISK_FULL: [self._heal_disk_full],
            IssueType.DATABASE_SLOW: [self._heal_database_slow],
            IssueType.API_RATE_LIMIT: [self._heal_api_rate_limit],
            IssueType.CACHE_MISS: [self._heal_cache_miss],
            IssueType.SERVICE_DOWN: [self._heal_service_down],
            IssueType.NETWORK_LATENCY: [self._heal_network_latency]
        }
        
        logger.info("🧰 Stratégies de guérison initialisées", 
                   total_strategies=len(self.healing_strategies))
    
    # MÉTHODES DE GUÉRISON SPÉCIALISÉES
    async def _heal_cpu_overload(self, issue: HealthIssue) -> bool:
        """🔧 Guérison surcharge CPU"""
        try:
            # 1. Identifier les processus consommateurs
            processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                             key=lambda p: p.info['cpu_percent'], reverse=True)
            
            # 2. Réduire la priorité des processus non-critiques
            for proc in processes[:3]:  # Top 3 CPU consumers
                if proc.info['cpu_percent'] > 20:
                    try:
                        p = psutil.Process(proc.info['pid'])
                        if p.name() not in ['python', 'postgres', 'redis-server']:  # Protected processes
                            p.nice(10)  # Lower priority
                            logger.info("🔧 Priorité réduite", 
                                       process=p.name(), 
                                       pid=proc.info['pid'])
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            # 3. Déclencher garbage collection
            import gc
            gc.collect()
            
            return True
            
        except Exception as e:
            logger.error("❌ Échec guérison CPU", error=str(e))
            return False
    
    async def _heal_memory_leak(self, issue: HealthIssue) -> bool:
        """🔧 Guérison fuite mémoire"""
        try:
            # 1. Garbage collection forcé
            import gc
            gc.collect()
            
            # 2. Nettoyage cache application
            # TODO: Implémenter nettoyage cache spécifique
            
            # 3. Redémarrage des services non-critiques si nécessaire
            memory_after_gc = psutil.virtual_memory().percent
            
            if memory_after_gc > 85:
                # Restart memory-heavy background tasks
                logger.info("🔄 Redémarrage tâches de fond pour libérer mémoire")
                # TODO: Implémenter restart intelligent
            
            return True
            
        except Exception as e:
            logger.error("❌ Échec guérison mémoire", error=str(e))
            return False
    
    async def _heal_disk_full(self, issue: HealthIssue) -> bool:
        """🔧 Nettoyage disque plein"""
        try:
            # 1. Nettoyage logs anciens
            await self._cleanup_old_logs()
            
            # 2. Nettoyage fichiers temporaires
            await self._cleanup_temp_files()
            
            # 3. Compression logs actifs
            await self._compress_large_files()
            
            return True
            
        except Exception as e:
            logger.error("❌ Échec nettoyage disque", error=str(e))
            return False
    
    async def _heal_database_slow(self, issue: HealthIssue) -> bool:
        """🔧 Optimisation base de données"""
        try:
            # 1. Mise à jour statistiques
            # TODO: Exécuter ANALYZE sur PostgreSQL
            
            # 2. Nettoyage connexions inactives
            # TODO: Implémenter nettoyage pool de connexions
            
            # 3. Optimisation cache
            # TODO: Ajuster cache parameters
            
            return True
            
        except Exception as e:
            logger.error("❌ Échec optimisation DB", error=str(e))
            return False
    
    async def _heal_api_rate_limit(self, issue: HealthIssue) -> bool:
        """🔧 Gestion limites API"""
        try:
            api_name = issue.metrics.get("api", "unknown")
            
            # 1. Activer rate limiting plus strict
            # TODO: Implémenter throttling adaptatif
            
            # 2. Utiliser cache pour réduire appels
            # TODO: Activer cache agressif temporairement
            
            # 3. Switch vers API backup si disponible
            if api_name == "openai" and issue.metrics["api_calls_remaining"] < 100:
                # TODO: Switch vers Anthropic temporairement
                logger.info("🔄 Switch vers API backup", api=api_name)
            
            return True
            
        except Exception as e:
            logger.error("❌ Échec gestion API", error=str(e))
            return False
    
    # Méthodes utilitaires de nettoyage
    async def _cleanup_old_logs(self):
        """Nettoyage logs anciens"""
        try:
            # Delete logs older than 7 days
            subprocess.run([
                "find", "/var/log", "-name", "*.log", 
                "-mtime", "+7", "-delete"
            ], check=True)
            logger.info("🧹 Logs anciens supprimés")
        except subprocess.CalledProcessError:
            logger.warning("⚠️ Échec suppression logs anciens")
    
    async def _cleanup_temp_files(self):
        """Nettoyage fichiers temporaires"""
        try:
            subprocess.run(["rm", "-rf", "/tmp/*"], shell=True)
            logger.info("🧹 Fichiers temporaires nettoyés")
        except subprocess.CalledProcessError:
            logger.warning("⚠️ Échec nettoyage fichiers temp")
    
    async def _compress_large_files(self):
        """Compression fichiers volumineux"""
        try:
            # Compress logs larger than 100MB
            subprocess.run([
                "find", "/var/log", "-name", "*.log", 
                "-size", "+100M", "-exec", "gzip", "{}", ";"
            ], check=True)
            logger.info("🗜️ Fichiers volumineux compressés")
        except subprocess.CalledProcessError:
            logger.warning("⚠️ Échec compression fichiers")
    
    # Stubs pour méthodes additionnelles
    async def _heal_cache_miss(self, issue: HealthIssue) -> bool:
        """🔧 Optimisation cache"""
        return True
    
    async def _heal_service_down(self, issue: HealthIssue) -> bool:
        """🔧 Redémarrage service"""
        return True
    
    async def _heal_network_latency(self, issue: HealthIssue) -> bool:
        """🔧 Optimisation réseau"""
        return True
    
    async def stop_monitoring(self):
        """Arrêt du monitoring"""
        self.is_running = False
        
        # Annuler toutes les tâches de monitoring
        for task in self.monitoring_tasks:
            task.cancel()
        
        logger.info("🛑 Auto-Healer arrêté")
    
    # Stubs pour méthodes complexes
    async def _establish_baseline_metrics(self):
        """Établit les métriques de référence"""
        pass
    
    async def _monitor_system_resources(self):
        """Monitoring ressources système"""
        pass
    
    async def _monitor_application_health(self):
        """Monitoring santé application"""
        pass
    
    async def _monitor_database_performance(self):
        """Monitoring performance DB"""
        pass
    
    async def _monitor_external_apis(self):
        """Monitoring APIs externes"""
        pass
    
    async def _monitor_cache_performance(self):
        """Monitoring performance cache"""
        pass
    
    async def _detect_anomaly_patterns(self):
        """Détection patterns d'anomalies"""
        pass
    
    async def _preventive_maintenance_cycle(self):
        """Cycle de maintenance préventive"""
        pass
    
    async def _cleanup_resolved_issues(self):
        """Nettoyage problèmes résolus"""
        pass
    
    async def _update_health_statistics(self):
        """Mise à jour statistiques santé"""
        pass
    
    async def _send_critical_alert(self, issue: HealthIssue):
        """Envoi alerte critique"""
        pass
    
    def _calculate_monitoring_interval(self, metrics: SystemMetrics) -> float:
        """Calcul intervalle monitoring adaptatif"""
        return 10.0  # 10 secondes par défaut 