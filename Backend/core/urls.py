from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #   APIS
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
    path("api/token/refresh", TokenRefreshView.as_view(), name="token-refresh"),

    #   WEB LINKS
    path("", views.HomeView.as_view(), name="home"),
    path("accounts/register/", views.RegisterView.as_view(), name="register"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("accounts/user-profile/<int:user_id>/",
         views.ProfileView.as_view(), name="profile"),
    path("sessions/add/", views.AddStudySessionView.as_view(), name="add-session"),
    path("skills/add/", views.AddSkillView.as_view(), name="add-skill"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("sessions/<int:pk>/edit/",
         views.EditStudySessionView.as_view(), name="edit-session"),
    path("skills/", views.AllSkillsView.as_view(), name="skills"),
    path("skills/<int:pk>/edit/", views.EditSkillView.as_view(), name="edit-skill"),
    path("sessions/<int:pk>/delete/",
         views.DeleteStudySessionView.as_view(), name="delete-session"),
    path("skills/<int:pk>/delete/",
         views.DeleteSkillView.as_view(), name="delete-skill"),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)