from celery.result import AsyncResult
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from mangaki.models import UserBackgroundTask


class UserBGTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBackgroundTask
        fields = ('id', 'task_id')


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def task_status(request: Request, task_id: str) -> Response:
    bg_task = get_object_or_404(request.user.background_tasks, task_id=task_id)
    result = AsyncResult(bg_task.task_id)
    return Response({'id': result.id, 'status': result.state})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def user_tasks(request: Request) -> Response:
    return Response(UserBGTaskSerializer(request.user.background_tasks.all(), many=True).data)
