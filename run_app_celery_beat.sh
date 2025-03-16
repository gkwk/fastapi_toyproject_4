#!/bin/bash
celery -A app_celery_beat.celery_beat.celery_beat_app beat