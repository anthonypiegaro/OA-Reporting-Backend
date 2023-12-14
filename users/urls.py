from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomUserViewSet, 
    LogoutView, 
    CustomUserList,
    CustomUserIsStaff
)

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("simple-list-users/", CustomUserList.as_view({'get': 'list'}), name="simple_users"),
    path("is-staff/", CustomUserIsStaff.as_view(), name="is_staff"),
] 
