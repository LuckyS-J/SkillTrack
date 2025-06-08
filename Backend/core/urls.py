from django.urls import path
from . import views

urlpatterns = [
    path("api/skills", views.SkillListCreateAPIView.as_view(),
         name="skill-list-create"),
    path("api/skills/<int:pk>",
         views.SkillDetailAPIView.as_view(), name="skill-detail"),
    path("api/sessions",
         views.SessionListCreateAPIView.as_view(), name="session-list-create"),
    path("api/sessions/<int:pk>",
         views.SessionDetailAPIView.as_view(), name="session-detail"),
]
