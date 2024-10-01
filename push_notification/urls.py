from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewset

app_name = "push_notification"

router = DefaultRouter()

router.register(r"user", UserViewset, basename="user-apis")


urlpatterns = [
    path("", include(router.urls)),
]
