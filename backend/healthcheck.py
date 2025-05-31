from celery import Celery

app = Celery('app.tasks.celery_app')
app.config_from_object('app.tasks.celery_app')

try:
    result = app.control.ping(timeout=1.0)
    if result:
        exit(0)
    else:
        exit(1)
except Exception:
    exit(1)
