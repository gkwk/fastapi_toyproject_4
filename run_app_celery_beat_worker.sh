#!/bin/bash
CELERY_BEAT_QUEUE_NAME=${CELERY_BEAT_QUEUE_NAME}
celery -A app_celery_beat_worker.celery_beat_worker.celery_beat_worker_app worker -Q $CELERY_BEAT_QUEUE_NAME --pool=prefork --prefetch-multiplier=1 --concurrency=2 -E