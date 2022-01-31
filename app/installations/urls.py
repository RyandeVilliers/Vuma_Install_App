from django.urls import path, include
from rest_framework.routers import DefaultRouter

from installations import views

router = DefaultRouter()

router.register('status', views.StatusViewSet)

app_name = 'installations'

# includes all urls registered with router and generated by DefaultRouter
urlpatterns = [
    path('', include(router.urls))
]