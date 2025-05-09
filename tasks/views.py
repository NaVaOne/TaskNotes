from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter  
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters
from .serializers import TaskSerializer, TaskListSerializer
from .models import Task
from .permissions import IsOwner

class TaskFilter(FilterSet):
    deadline_before = filters.DateTimeFilter(field_name='deadline', lookup_expr='lte')
    deadline_after = filters.DateTimeFilter(field_name='deadline', lookup_expr='gte')

    class Meta:
        model = Task
        fields = ['is_completed', 'is_alerted']

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    filter_backends = (DjangoFilterBackend, SearchFilter) 
    filterset_class = TaskFilter
    search_fields = ('title',)
    ordering_fields = ('deadline', 'created_at', 'updated_at')
    ordering = ['-created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        return TaskSerializer
