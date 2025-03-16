#!/bin/bash
celery -A app_celery_worker.celery_worker.celery_worker_app worker --pool=prefork --prefetch-multiplier=1 --concurrency=2 -E
