"""
🛡️ SECURITY SUPERVISOR - SUPERVISION ET SÉCURITÉ
================================================

Ce module implémente la supervision de sécurité de l'orchestrateur :
- Health checks avancés et diagnostics système
- Monitoring intelligent avec alertes prédictives
- Détection CVE et analyse de vulnérabilités
- Supervision de l'intégrité des données
"""

import logging
import json
import psutil
import asyncio
import aiohttp
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import os
import platform
import docker
import requests
import sys
sys.path.append('/app/backend')
from database.connection import get_db

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """États de santé du système"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"

class AlertSeverity(Enum):
    """Niveaux de sévérité des alertes"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    SECURITY = "security"

class CVESeverity(Enum):
    """Sévérité des vulnérabilités CVE"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class HealthCheckResult:
    """Résultat d'un health check"""
    component: str
    status: HealthStatus
    message: str
    metrics: Dict[str, Any]
    timestamp: datetime
    response_time_ms: float
    recommendations: List[str]

@dataclass
class SecurityAlert:
    """Alerte de sécurité"""
    alert_id: str
    severity: AlertSeverity
    component: str
    title: str
    description: str
    impact: str
    remediation: List[str]
    detected_at: datetime
    resolved_at: Optional[datetime]
    metadata: Dict[str, Any]

@dataclass
class CVEVulnerability:
    """Vulnérabilité CVE détectée"""
    cve_id: str
    severity: CVESeverity
    score: float
    component: str
    version: str
    description: str
    vector: str
    exploit_available: bool
    patch_available: bool
    remediation_steps: List[str]
    discovered_at: datetime

@dataclass
class SystemMetrics:
    """Métriques système complètes"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, int]
    process_count: int
    open_files: int
    active_connections: int
    load_average: List[float]
    uptime_seconds: int
    docker_containers: Dict[str, str]
    security_score: float

class SecuritySupervisor:
    """
    🛡️ SUPERVISEUR DE SÉCURITÉ ET SANTÉ
    
    Surveillance complète de la sécurité, santé système et détection CVE :
    - Monitoring en temps réel de tous les composants
    - Détection proactive des vulnérabilités
    - Alertes intelligentes et recommandations
    - Intégrité et conformité de sécurité
    """
    
    def __init__(self):
        self.health_history: List[HealthCheckResult] = []
        self.active_alerts: List[SecurityAlert] = []
        self.cve_database: List[CVEVulnerability] = []
        self.security_baseline: Dict[str, Any] = {}
        
        # Configuration
        self.check_interval = 30  # secondes
        self.alert_threshold = {
            "cpu": 85.0,
            "memory": 90.0,
            "disk": 95.0,
            "connections": 1000
        }
        self.cve_api_url = "https://cve.circl.lu/api"
        
        # Métriques
        self.total_checks = 0
        self.failed_checks = 0
        self.security_incidents = 0
        self.uptime_start = datetime.utcnow()
        
        # Docker client
        try:
            self.docker_client = docker.from_env()
        except Exception as e:
            logger.warning(f"⚠️ Docker non disponible: {e}")
            self.docker_client = None
        
        logger.info("🛡️ Security Supervisor initialisé - Surveillance active")

    async def run_comprehensive_health_check(self) -> Dict[str, HealthCheckResult]:
        """
        🏥 Effectuer un health check complet du système
        
        Returns:
            Dict des résultats par composant
        """
        try:
            start_time = datetime.utcnow()
            health_results = {}
            
            # Composants à vérifier
            components = [
                ("system", self._check_system_health),
                ("database", self._check_database_health),
                ("network", self._check_network_health),
                ("docker", self._check_docker_health),
                ("security", self._check_security_health),
                ("orchestrator", self._check_orchestrator_health)
            ]
            
            # Exécuter les checks en parallèle
            tasks = []
            for component, check_func in components:
                task = asyncio.create_task(self._run_single_check(component, check_func))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Compiler les résultats
            for i, (component, _) in enumerate(components):
                if isinstance(results[i], Exception):
                    health_results[component] = HealthCheckResult(
                        component=component,
                        status=HealthStatus.CRITICAL,
                        message=f"Check failed: {results[i]}",
                        metrics={},
                        timestamp=datetime.utcnow(),
                        response_time_ms=0.0,
                        recommendations=["Investigate component failure"]
                    )
                else:
                    health_results[component] = results[i]
            
            # Stocker l'historique
            self.health_history.extend(health_results.values())
            self.total_checks += len(health_results)
            
            # Analyser et générer des alertes
            await self._analyze_health_trends(health_results)
            
            total_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            logger.info(f"🏥 Health check complet terminé en {total_time:.1f}ms")
            
            return health_results
            
        except Exception as e:
            logger.error(f"❌ Erreur health check complet: {e}")
            return {}

    async def _run_single_check(self, component: str, check_func) -> HealthCheckResult:
        """🔍 Exécuter un check individuel avec mesure de performance"""
        
        start_time = datetime.utcnow()
        
        try:
            result = await check_func()
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            result.response_time_ms = response_time
            return result
            
        except Exception as e:
            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            logger.error(f"❌ Check {component} failed: {e}")
            
            return HealthCheckResult(
                component=component,
                status=HealthStatus.CRITICAL,
                message=f"Check failed: {str(e)}",
                metrics={},
                timestamp=datetime.utcnow(),
                response_time_ms=response_time,
                recommendations=[f"Investigate {component} failure"]
            )

    async def _check_system_health(self) -> HealthCheckResult:
        """🖥️ Vérifier la santé du système"""
        
        try:
            # Métriques système
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            
            metrics = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_usage": disk.percent,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "load_average": load_avg,
                "process_count": len(psutil.pids())
            }
            
            # Déterminer le statut
            if cpu_percent > 90 or memory.percent > 95 or disk.percent > 98:
                status = HealthStatus.CRITICAL
                message = "Critical resource usage detected"
            elif cpu_percent > 80 or memory.percent > 85 or disk.percent > 90:
                status = HealthStatus.WARNING
                message = "High resource usage"
            else:
                status = HealthStatus.HEALTHY
                message = "System resources optimal"
            
            # Recommandations
            recommendations = []
            if cpu_percent > 80:
                recommendations.append("Consider scaling or optimizing CPU-intensive processes")
            if memory.percent > 85:
                recommendations.append("Monitor memory leaks and consider increasing RAM")
            if disk.percent > 90:
                recommendations.append("Clean up disk space or increase storage")
            
            return HealthCheckResult(
                component="system",
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ System health check failed: {e}")
            raise

    async def _check_database_health(self) -> HealthCheckResult:
        """🗄️ Vérifier la santé de la base de données"""
        
        try:
            from app.database.connection import get_db
            
            start_time = datetime.utcnow()
            
            # Test de connexion simple
            with next(get_db()) as session:
                result = session.execute("SELECT 1")
                result.fetchone()
            
            connection_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Métriques additionnelles (simulées en dev)
            metrics = {
                "connection_time_ms": round(connection_time, 2),
                "active_connections": 5,  # Simulé
                "slow_queries": 0,       # Simulé
                "database_size_mb": 150  # Simulé
            }
            
            if connection_time > 1000:  # > 1 seconde
                status = HealthStatus.WARNING
                message = "Slow database connection"
                recommendations = ["Check database performance", "Optimize queries"]
            elif connection_time > 5000:  # > 5 secondes
                status = HealthStatus.CRITICAL
                message = "Very slow database connection"
                recommendations = ["Urgent database optimization needed"]
            else:
                status = HealthStatus.HEALTHY
                message = "Database connection healthy"
                recommendations = []
            
            return HealthCheckResult(
                component="database",
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ Database health check failed: {e}")
            return HealthCheckResult(
                component="database",
                status=HealthStatus.CRITICAL,
                message=f"Database connection failed: {str(e)}",
                metrics={},
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=["Check database configuration", "Verify database is running"]
            )

    async def _check_network_health(self) -> HealthCheckResult:
        """🌐 Vérifier la santé réseau"""
        
        try:
            # Test de connectivité
            test_urls = [
                "https://httpbin.org/status/200",
                "https://api.github.com",
                "https://www.google.com"
            ]
            
            successful_requests = 0
            total_response_time = 0
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                for url in test_urls:
                    try:
                        start_time = datetime.utcnow()
                        async with session.get(url) as response:
                            if response.status == 200:
                                successful_requests += 1
                            response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
                            total_response_time += response_time
                    except Exception as e:
                        logger.debug(f"Network test failed for {url}: {e}")
            
            # Métriques réseau
            net_io = psutil.net_io_counters()
            connections = len(psutil.net_connections())
            
            metrics = {
                "connectivity_success_rate": round(successful_requests / len(test_urls), 2),
                "average_response_time_ms": round(total_response_time / len(test_urls), 2),
                "bytes_sent": net_io.bytes_sent,
                "bytes_received": net_io.bytes_recv,
                "active_connections": connections,
                "packets_dropped": net_io.dropin + net_io.dropout
            }
            
            # Déterminer le statut
            success_rate = successful_requests / len(test_urls)
            if success_rate < 0.5:
                status = HealthStatus.CRITICAL
                message = "Poor network connectivity"
            elif success_rate < 0.8:
                status = HealthStatus.WARNING
                message = "Degraded network connectivity"
            else:
                status = HealthStatus.HEALTHY
                message = "Network connectivity good"
            
            recommendations = []
            if success_rate < 0.8:
                recommendations.append("Check internet connection stability")
            if connections > self.alert_threshold["connections"]:
                recommendations.append("High number of active connections detected")
            
            return HealthCheckResult(
                component="network",
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ Network health check failed: {e}")
            raise

    async def _check_docker_health(self) -> HealthCheckResult:
        """🐳 Vérifier la santé des conteneurs Docker"""
        
        try:
            if not self.docker_client:
                return HealthCheckResult(
                    component="docker",
                    status=HealthStatus.WARNING,
                    message="Docker client not available",
                    metrics={},
                    timestamp=datetime.utcnow(),
                    response_time_ms=0.0,
                    recommendations=["Install Docker or check Docker daemon"]
                )
            
            # Lister les conteneurs
            containers = self.docker_client.containers.list(all=True)
            running_containers = [c for c in containers if c.status == 'running']
            
            # Métriques Docker
            metrics = {
                "total_containers": len(containers),
                "running_containers": len(running_containers),
                "stopped_containers": len(containers) - len(running_containers),
                "container_details": {}
            }
            
            # Détails par conteneur
            for container in containers:
                try:
                    stats = container.stats(stream=False) if container.status == 'running' else {}
                    metrics["container_details"][container.name] = {
                        "status": container.status,
                        "image": container.image.tags[0] if container.image.tags else "unknown",
                        "created": container.attrs["Created"],
                        "health": stats.get("health", {}).get("Status", "unknown") if stats else "stopped"
                    }
                except Exception as e:
                    logger.debug(f"Error getting container stats for {container.name}: {e}")
            
            # Déterminer le statut
            critical_containers = ["backend", "frontend", "database", "redis"]
            critical_running = sum(1 for name in critical_containers 
                                 if any(name in c.name for c in running_containers))
            
            if critical_running < len(critical_containers) / 2:
                status = HealthStatus.CRITICAL
                message = "Critical containers not running"
            elif len(running_containers) < len(containers) * 0.8:
                status = HealthStatus.WARNING
                message = "Some containers stopped"
            else:
                status = HealthStatus.HEALTHY
                message = "All containers healthy"
            
            recommendations = []
            if critical_running < len(critical_containers):
                recommendations.append("Restart critical containers")
            
            return HealthCheckResult(
                component="docker",
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ Docker health check failed: {e}")
            return HealthCheckResult(
                component="docker",
                status=HealthStatus.WARNING,
                message=f"Docker check failed: {str(e)}",
                metrics={},
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=["Check Docker daemon status"]
            )

    async def _check_security_health(self) -> HealthCheckResult:
        """🔒 Vérifier la santé sécuritaire"""
        
        try:
            security_issues = []
            security_score = 100.0
            
            # Vérifier les permissions de fichiers critiques
            critical_files = [
                "/etc/passwd",
                "/etc/shadow", 
                "backend/app/config.py",
                ".env"
            ]
            
            file_permissions_ok = True
            for file_path in critical_files:
                if os.path.exists(file_path):
                    stat_info = os.stat(file_path)
                    mode = oct(stat_info.st_mode)[-3:]
                    
                    # Vérifications de sécurité basiques
                    if file_path in ["/etc/shadow", ".env"] and mode != "600":
                        security_issues.append(f"Insecure permissions on {file_path}: {mode}")
                        file_permissions_ok = False
                        security_score -= 15
            
            # Vérifier les ports ouverts
            connections = psutil.net_connections(kind='inet')
            listening_ports = [conn.laddr.port for conn in connections if conn.status == 'LISTEN']
            
            # Ports suspects
            suspicious_ports = [port for port in listening_ports if port in [22, 23, 21, 135, 445]]
            if suspicious_ports:
                security_issues.append(f"Suspicious ports open: {suspicious_ports}")
                security_score -= 10
            
            # Vérifier les processus suspects
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Processus à haute consommation
            high_cpu_procs = [p for p in processes if p['cpu_percent'] > 80]
            if high_cpu_procs:
                security_issues.append(f"High CPU processes detected: {[p['name'] for p in high_cpu_procs]}")
                security_score -= 5
            
            metrics = {
                "security_score": round(security_score, 1),
                "security_issues_count": len(security_issues),
                "file_permissions_ok": file_permissions_ok,
                "listening_ports": listening_ports,
                "process_count": len(processes),
                "suspicious_ports": suspicious_ports
            }
            
            # Déterminer le statut
            if security_score < 60:
                status = HealthStatus.CRITICAL
                message = "Critical security issues detected"
            elif security_score < 80:
                status = HealthStatus.WARNING
                message = "Security issues require attention"
            else:
                status = HealthStatus.HEALTHY
                message = "Security posture good"
            
            recommendations = []
            if not file_permissions_ok:
                recommendations.append("Fix file permissions on sensitive files")
            if suspicious_ports:
                recommendations.append("Review and secure open ports")
            if high_cpu_procs:
                recommendations.append("Investigate high CPU usage processes")
            
            return HealthCheckResult(
                component="security",
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ Security health check failed: {e}")
            raise

    async def _check_orchestrator_health(self) -> HealthCheckResult:
        """🎯 Vérifier la santé de l'orchestrateur"""
        
        try:
            # Vérifier les modules critiques
            from app.orchestrator.decision_engine import get_decision_engine
            from app.orchestrator.performance_tracker import get_performance_tracker
            
            decision_engine = get_decision_engine()
            performance_tracker = get_performance_tracker()
            
            # Métriques de l'orchestrateur
            recent_metrics = await performance_tracker.get_recent_metrics()
            
            metrics = {
                "decision_engine_active": hasattr(decision_engine, 'running') and decision_engine.running,
                "performance_tracker_active": performance_tracker is not None,
                "recent_success_rate": recent_metrics.get("success_rate", 0),
                "total_tasks": recent_metrics.get("total_tasks", 0),
                "average_execution_time": recent_metrics.get("average_execution_time", 0),
                "last_activity": recent_metrics.get("last_activity", "unknown")
            }
            
            # Déterminer le statut
            success_rate = metrics.get("recent_success_rate", 0)
            if success_rate < 50:
                status = HealthStatus.CRITICAL
                message = "Orchestrator performance critical"
            elif success_rate < 80:
                status = HealthStatus.WARNING
                message = "Orchestrator performance degraded"
            else:
                status = HealthStatus.HEALTHY
                message = "Orchestrator performing well"
            
            recommendations = []
            if success_rate < 80:
                recommendations.append("Review orchestrator decision logic")
                recommendations.append("Check for failed tasks and investigate causes")
            
            return HealthCheckResult(
                component="orchestrator",
                status=status,
                message=message,
                metrics=metrics,
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"❌ Orchestrator health check failed: {e}")
            return HealthCheckResult(
                component="orchestrator",
                status=HealthStatus.WARNING,
                message=f"Orchestrator check failed: {str(e)}",
                metrics={},
                timestamp=datetime.utcnow(),
                response_time_ms=0.0,
                recommendations=["Check orchestrator modules"]
            )

    async def scan_cve_vulnerabilities(self) -> List[CVEVulnerability]:
        """
        🔍 Scanner les vulnérabilités CVE dans le système
        
        Returns:
            Liste des vulnérabilités détectées
        """
        try:
            logger.info("🔍 Démarrage scan CVE...")
            vulnerabilities = []
            
            # Scanner les packages Python installés
            python_vulns = await self._scan_python_packages()
            vulnerabilities.extend(python_vulns)
            
            # Scanner les packages système (Ubuntu/Debian)
            if platform.system() == "Linux":
                system_vulns = await self._scan_system_packages()
                vulnerabilities.extend(system_vulns)
            
            # Scanner les images Docker
            if self.docker_client:
                docker_vulns = await self._scan_docker_images()
                vulnerabilities.extend(docker_vulns)
            
            # Mettre à jour la base CVE
            self.cve_database = vulnerabilities
            
            # Générer des alertes pour les CVE critiques
            await self._generate_cve_alerts(vulnerabilities)
            
            logger.info(f"🔍 Scan CVE terminé - {len(vulnerabilities)} vulnérabilités détectées")
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"❌ Erreur scan CVE: {e}")
            return []

    async def _scan_python_packages(self) -> List[CVEVulnerability]:
        """🐍 Scanner les vulnérabilités dans les packages Python"""
        
        vulnerabilities = []
        
        try:
            # Simuler la détection de vulnérabilités Python
            # En production, utiliser des outils comme safety, pip-audit
            
            known_vulns = [
                {
                    "cve_id": "CVE-2023-5752",
                    "package": "pip",
                    "version": "20.3.4",
                    "severity": "medium",
                    "description": "pip vulnerability in dependency resolution"
                },
                {
                    "cve_id": "CVE-2023-43804", 
                    "package": "urllib3",
                    "version": "1.26.5",
                    "severity": "high",
                    "description": "urllib3 cookie injection vulnerability"
                }
            ]
            
            for vuln_data in known_vulns:
                vulnerability = CVEVulnerability(
                    cve_id=vuln_data["cve_id"],
                    severity=CVESeverity(vuln_data["severity"]),
                    score=7.5 if vuln_data["severity"] == "high" else 5.0,
                    component=f"python:{vuln_data['package']}",
                    version=vuln_data["version"],
                    description=vuln_data["description"],
                    vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
                    exploit_available=False,
                    patch_available=True,
                    remediation_steps=[
                        f"Update {vuln_data['package']} to latest version",
                        "Run: pip install --upgrade " + vuln_data['package']
                    ],
                    discovered_at=datetime.utcnow()
                )
                vulnerabilities.append(vulnerability)
            
        except Exception as e:
            logger.error(f"❌ Erreur scan packages Python: {e}")
        
        return vulnerabilities

    async def _scan_system_packages(self) -> List[CVEVulnerability]:
        """📦 Scanner les vulnérabilités des packages système"""
        
        vulnerabilities = []
        
        try:
            # Utiliser apt ou autres gestionnaires de paquets
            # Simulé pour la démo
            
            system_vulns = [
                {
                    "cve_id": "CVE-2023-4911",
                    "package": "glibc",
                    "version": "2.31-0ubuntu9.9",
                    "severity": "high",
                    "description": "Buffer overflow in glibc's ld.so"
                }
            ]
            
            for vuln_data in system_vulns:
                vulnerability = CVEVulnerability(
                    cve_id=vuln_data["cve_id"],
                    severity=CVESeverity(vuln_data["severity"]),
                    score=8.1,
                    component=f"system:{vuln_data['package']}",
                    version=vuln_data["version"],
                    description=vuln_data["description"],
                    vector="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H",
                    exploit_available=True,
                    patch_available=True,
                    remediation_steps=[
                        "Update system packages: sudo apt update && sudo apt upgrade",
                        f"Specifically update {vuln_data['package']} package"
                    ],
                    discovered_at=datetime.utcnow()
                )
                vulnerabilities.append(vulnerability)
            
        except Exception as e:
            logger.error(f"❌ Erreur scan packages système: {e}")
        
        return vulnerabilities

    async def _scan_docker_images(self) -> List[CVEVulnerability]:
        """🐳 Scanner les vulnérabilités des images Docker"""
        
        vulnerabilities = []
        
        try:
            if not self.docker_client:
                return vulnerabilities
            
            images = self.docker_client.images.list()
            
            # Simuler scan d'images Docker
            for image in images[:3]:  # Limiter pour la démo
                if image.tags:
                    tag = image.tags[0]
                    
                    # Simuler des vulnérabilités trouvées
                    docker_vuln = CVEVulnerability(
                        cve_id="CVE-2023-5678",
                        severity=CVESeverity.MEDIUM,
                        score=6.5,
                        component=f"docker:{tag}",
                        version="latest",
                        description=f"Vulnerability found in base image {tag}",
                        vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N",
                        exploit_available=False,
                        patch_available=True,
                        remediation_steps=[
                            f"Update base image for {tag}",
                            "Rebuild container with latest base image"
                        ],
                        discovered_at=datetime.utcnow()
                    )
                    vulnerabilities.append(docker_vuln)
            
        except Exception as e:
            logger.error(f"❌ Erreur scan images Docker: {e}")
        
        return vulnerabilities

    async def _generate_cve_alerts(self, vulnerabilities: List[CVEVulnerability]):
        """🚨 Générer des alertes pour les CVE critiques"""
        
        try:
            for vuln in vulnerabilities:
                if vuln.severity in [CVESeverity.HIGH, CVESeverity.CRITICAL]:
                    alert = SecurityAlert(
                        alert_id=f"cve_{vuln.cve_id}_{int(datetime.utcnow().timestamp())}",
                        severity=AlertSeverity.SECURITY if vuln.severity == CVESeverity.CRITICAL else AlertSeverity.ERROR,
                        component=vuln.component,
                        title=f"CVE Vulnerability: {vuln.cve_id}",
                        description=vuln.description,
                        impact=f"Security vulnerability with CVSS score {vuln.score}",
                        remediation=vuln.remediation_steps,
                        detected_at=datetime.utcnow(),
                        resolved_at=None,
                        metadata={
                            "cve_id": vuln.cve_id,
                            "cvss_score": vuln.score,
                            "vector": vuln.vector,
                            "exploit_available": vuln.exploit_available
                        }
                    )
                    self.active_alerts.append(alert)
                    self.security_incidents += 1
            
        except Exception as e:
            logger.error(f"❌ Erreur génération alertes CVE: {e}")

    async def _analyze_health_trends(self, health_results: Dict[str, HealthCheckResult]):
        """📈 Analyser les tendances de santé et générer des alertes prédictives"""
        
        try:
            # Analyser les tendances sur les derniers checks
            if len(self.health_history) < 10:
                return
            
            recent_history = self.health_history[-10:]
            
            # Détecter les dégradations
            for component in ["system", "database", "network"]:
                component_history = [h for h in recent_history if h.component == component]
                
                if len(component_history) >= 3:
                    # Vérifier si la tendance se dégrade
                    statuses = [h.status for h in component_history[-3:]]
                    
                    if self._is_degrading_trend(statuses):
                        alert = SecurityAlert(
                            alert_id=f"trend_{component}_{int(datetime.utcnow().timestamp())}",
                            severity=AlertSeverity.WARNING,
                            component=component,
                            title=f"Degrading trend detected in {component}",
                            description=f"Component {component} showing degrading health trend",
                            impact="Potential service degradation if trend continues",
                            remediation=[
                                f"Investigate {component} performance issues",
                                "Monitor closely for further degradation"
                            ],
                            detected_at=datetime.utcnow(),
                            resolved_at=None,
                            metadata={"trend_analysis": True}
                        )
                        self.active_alerts.append(alert)
            
        except Exception as e:
            logger.error(f"❌ Erreur analyse tendances: {e}")

    def _is_degrading_trend(self, statuses: List[HealthStatus]) -> bool:
        """📉 Détecter si une tendance se dégrade"""
        
        # Convertir en scores numériques
        status_scores = {
            HealthStatus.HEALTHY: 4,
            HealthStatus.WARNING: 3,
            HealthStatus.DEGRADED: 2,
            HealthStatus.CRITICAL: 1,
            HealthStatus.UNKNOWN: 0
        }
        
        scores = [status_scores.get(status, 0) for status in statuses]
        
        # Tendance dégradante si le score diminue
        return len(scores) >= 2 and scores[-1] < scores[0]

    async def get_security_dashboard(self) -> Dict[str, Any]:
        """📊 Obtenir le tableau de bord sécurité complet"""
        
        try:
            # Health check récent
            health_results = await self.run_comprehensive_health_check()
            
            # Métriques système actuelles
            system_metrics = await self._collect_system_metrics()
            
            # Résumé des alertes
            active_alerts_summary = {
                "total": len(self.active_alerts),
                "by_severity": {},
                "recent": []
            }
            
            for alert in self.active_alerts:
                severity = alert.severity.value
                active_alerts_summary["by_severity"][severity] = active_alerts_summary["by_severity"].get(severity, 0) + 1
            
            active_alerts_summary["recent"] = [
                {
                    "title": alert.title,
                    "severity": alert.severity.value,
                    "component": alert.component,
                    "detected_at": alert.detected_at.isoformat()
                }
                for alert in sorted(self.active_alerts, key=lambda x: x.detected_at, reverse=True)[:5]
            ]
            
            # Résumé CVE
            cve_summary = {
                "total_vulnerabilities": len(self.cve_database),
                "by_severity": {},
                "critical_count": len([v for v in self.cve_database if v.severity == CVESeverity.CRITICAL]),
                "high_count": len([v for v in self.cve_database if v.severity == CVESeverity.HIGH])
            }
            
            for vuln in self.cve_database:
                severity = vuln.severity.value
                cve_summary["by_severity"][severity] = cve_summary["by_severity"].get(severity, 0) + 1
            
            dashboard = {
                "timestamp": datetime.utcnow().isoformat(),
                "overall_health": self._calculate_overall_health(health_results),
                "system_metrics": system_metrics,
                "health_components": {
                    component: {
                        "status": result.status.value,
                        "message": result.message,
                        "response_time_ms": result.response_time_ms
                    }
                    for component, result in health_results.items()
                },
                "security_score": await self._calculate_security_score(),
                "alerts_summary": active_alerts_summary,
                "cve_summary": cve_summary,
                "uptime_seconds": (datetime.utcnow() - self.uptime_start).total_seconds(),
                "statistics": {
                    "total_checks": self.total_checks,
                    "failed_checks": self.failed_checks,
                    "success_rate": round((self.total_checks - self.failed_checks) / max(1, self.total_checks) * 100, 1),
                    "security_incidents": self.security_incidents
                }
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"❌ Erreur génération dashboard sécurité: {e}")
            return {}

    async def _collect_system_metrics(self) -> SystemMetrics:
        """📊 Collecter les métriques système complètes"""
        
        try:
            # Métriques CPU et mémoire
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Métriques réseau
            net_io = psutil.net_io_counters()
            
            # Processus et connexions
            process_count = len(psutil.pids())
            connections = len(psutil.net_connections())
            
            # Charge système
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            
            # Uptime
            uptime_seconds = (datetime.utcnow() - self.uptime_start).total_seconds()
            
            # Conteneurs Docker
            docker_containers = {}
            if self.docker_client:
                try:
                    containers = self.docker_client.containers.list(all=True)
                    for container in containers:
                        docker_containers[container.name] = container.status
                except Exception as e:
                    logger.debug(f"Error getting Docker containers: {e}")
            
            return SystemMetrics(
                cpu_usage=cpu_percent,
                memory_usage=memory.percent,
                disk_usage=disk.percent,
                network_io={
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv
                },
                process_count=process_count,
                open_files=len(psutil.Process().open_files()) if hasattr(psutil.Process(), 'open_files') else 0,
                active_connections=connections,
                load_average=list(load_avg),
                uptime_seconds=int(uptime_seconds),
                docker_containers=docker_containers,
                security_score=await self._calculate_security_score()
            )
            
        except Exception as e:
            logger.error(f"❌ Erreur collecte métriques système: {e}")
            return SystemMetrics(
                cpu_usage=0, memory_usage=0, disk_usage=0,
                network_io={}, process_count=0, open_files=0,
                active_connections=0, load_average=[0, 0, 0],
                uptime_seconds=0, docker_containers={},
                security_score=0.0
            )

    def _calculate_overall_health(self, health_results: Dict[str, HealthCheckResult]) -> str:
        """🏥 Calculer l'état de santé global"""
        
        if not health_results:
            return "unknown"
        
        statuses = [result.status for result in health_results.values()]
        
        if HealthStatus.CRITICAL in statuses:
            return "critical"
        elif HealthStatus.WARNING in statuses:
            return "warning"
        elif all(status == HealthStatus.HEALTHY for status in statuses):
            return "healthy"
        else:
            return "degraded"

    async def _calculate_security_score(self) -> float:
        """🔒 Calculer le score de sécurité global"""
        
        try:
            base_score = 100.0
            
            # Pénalités pour alertes actives
            for alert in self.active_alerts:
                if alert.severity == AlertSeverity.CRITICAL:
                    base_score -= 25
                elif alert.severity == AlertSeverity.ERROR:
                    base_score -= 15
                elif alert.severity == AlertSeverity.WARNING:
                    base_score -= 5
            
            # Pénalités pour CVE
            for vuln in self.cve_database:
                if vuln.severity == CVESeverity.CRITICAL:
                    base_score -= 20
                elif vuln.severity == CVESeverity.HIGH:
                    base_score -= 10
                elif vuln.severity == CVESeverity.MEDIUM:
                    base_score -= 5
            
            return max(0.0, min(100.0, base_score))
            
        except Exception as e:
            logger.error(f"❌ Erreur calcul score sécurité: {e}")
            return 50.0

# Instance globale
_security_supervisor: Optional[SecuritySupervisor] = None

def get_security_supervisor() -> SecuritySupervisor:
    """🛡️ Obtenir l'instance du superviseur de sécurité"""
    global _security_supervisor
    if _security_supervisor is None:
        _security_supervisor = SecuritySupervisor()
    return _security_supervisor 