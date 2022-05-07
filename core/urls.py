from django.urls import path, include
from rest_framework import routers

from api.v1.views import students


router = routers.DefaultRouter()
router.register(r'students', students.StudentViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
