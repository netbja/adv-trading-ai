#!/usr/bin/env python3
"""
Health check script for Celery workers and beat scheduler
"""
import sys
import os
from celery import Celery

# Configuration Redis depuis les variables d'environnement
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

# Créer l'app Celery avec la configuration correcte
app = Celery('app.tasks.celery_app', broker=redis_url, backend=redis_url)

# Configuration minimale pour le health check
app.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    broker_connection_retry_on_startup=True,
    worker_hijack_root_logger=False,
    task_ignore_result=True,
)

def health_check():
    """Vérification de santé Celery"""
    try:
        # Test 1: Ping des workers actifs
        inspect = app.control.inspect()
        ping_result = inspect.ping(timeout=2.0)
        
        if ping_result:
            print("✅ Celery workers responding")
            return True
        else:
            # Test 2: Vérifier si on peut accéder au broker Redis
            from celery.app.control import Inspect
            inspect = Inspect(app=app)
            stats = inspect.stats(timeout=1.0)
            
            if stats is not None:
                print("✅ Celery broker accessible")
                return True
            else:
                print("❌ No Celery workers found")
                return False
                
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    if health_check():
        print("🟢 Celery service healthy")
        sys.exit(0)
    else:
        print("🔴 Celery service unhealthy")
        sys.exit(1)
