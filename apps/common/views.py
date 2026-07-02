from django.shortcuts import render

from django.http import JsonResponse
from .tasks import test_task

def health(request):
    return JsonResponse({
        "status": "ok",
        "service": "hubbi-auto-api"
    })


def celery_test(request):
    task = test_task.delay()

    return JsonResponse({
        "message": "Tarefa enviada com sucesso.",
        "task_id": task.id,
    })
