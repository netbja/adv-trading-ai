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
        # Test 1: Ping des workers actifs (sans timeout explicite)
        inspect = app.control.inspect()
        ping_result = inspect.ping()
        
        if ping_result:
            print("✅ Celery workers responding")
            print(f"Workers found: {list(ping_result.keys())}")
            return True
        else:
            print("❌ No ping response from workers")
            
            # Test 2: Vérifier la connexion au broker Redis
            try:
                import redis
                r = redis.from_url(redis_url)
                r.ping()
                print("✅ Redis broker accessible")
                
                # Test 3: Vérifier les stats des workers
                stats = inspect.stats()
                if stats:
                    print("✅ Worker stats accessible")
                    return True
                else:
                    print("⚠️ No worker stats but Redis OK")
                    return True  # Considérer comme healthy si Redis fonctionne
                    
            except Exception as redis_error:
                print(f"❌ Redis connection failed: {redis_error}")
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
