#!/bin/bash

if [[ "${1}" == "worker" ]]; then
  # Запуск воркета для выполнения задач
  celery --app=src.tasks.tasks:celery worker --concurrency=4 -l INFO
elif [[ "${1}" == "beat" ]]; then
  # Запуск планировщика задач
  celery --app=src.tasks.tasks:celery beat -l INFO
fi