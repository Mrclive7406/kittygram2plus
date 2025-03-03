from rest_framework import viewsets
from rest_framework.throttling import ScopedRateThrottle
from .throttling import WorkingHoursRateThrottle
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import OwnerOrReadOnly, ReadOnly
from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle,)
    throttle_scope = 'low_request'
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                    filters.OrderingFilter)
    filterset_fields = ('color', 'birth_year')
    search_fields = ('achievements__name', 'owner__username')
    ordering_fields = ('name', 'birth_year')
    ordering = ('birth_year',)
    
    def get_queryset(self):
        queryset = Cat.objects.all()
        color = self.kwargs['color']
        queryset = queryset.filter(color=color)
        return queryset 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions() 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer