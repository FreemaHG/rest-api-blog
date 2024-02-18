#!/bin/bash

if [[ "${1}" == "worker" ]]; then
  # Запуск воркета для выполнения задач
  celery --app=src.tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "beat" ]]; then
  # Запуск планировщика задач
  celery --app=src.tasks.tasks:celery beat -l INFO
elif [[ "${1}" == "flower" ]]; then
  # Запуск flower
  celery --app=src.tasks.tasks:celery flower
fi