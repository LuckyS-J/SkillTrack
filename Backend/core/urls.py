from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/skills", views.SkillListCreateAPIView.as_view(),
         name="skill-list-create"),
    path("api/skills/<int:pk>",
         views.SkillDetailAPIView.as_view(), name="skill-detail"),
    path("api/sessions",
         views.SessionListCreateAPIView.as_view(), name="session-list-create"),
    path("api/sessions/<int:pk>",
         views.SessionDetailAPIView.as_view(), name="session-detail"),
    path("api/register/", views.RegisterAPIView.as_view(), name="api-register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token-refresh")
]
