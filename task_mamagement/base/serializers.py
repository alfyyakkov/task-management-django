from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Task

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'assigned_to',
            'assigned_to_id',
            'due_date',
            'status',
            'completion_report',
            'worked_hours',
        ]
        read_only_fields = ['status', 'completion_report', 'worked_hours']
