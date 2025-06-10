from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from .models import Skill, StudySession, User, UserProfile
from .serializers import SkillSerializer, StudySessionSerializer, UserSerializer, UserProfileSerializer, RegisterSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
# Create your views here.


# APIS
class SkillListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Skill.objects.filter(user=request.user)
        serializer = SkillSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_skill(self, pk):
        return get_object_or_404(Skill, pk=pk, user=self.request.user)

    def get(self, request, pk):
        skill = self.get_skill(pk)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    def put(self, request, pk):
        skill = self.get_skill(pk)
        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        skill = self.get_skill(pk)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SessionListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = StudySession.objects.filter(user=request.user)
        serializer = StudySessionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudySessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_session(self, pk):
        return get_object_or_404(StudySession, pk=pk, user=self.request.user)

    def get(self, request, pk):
        session = self.get_session(pk)
        serializer = StudySessionSerializer(session)
        return Response(serializer.data)

    def put(self, request, pk):
        session = self.get_session(pk)
        serializer = StudySessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        session = self.get_session(pk)
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterAPIView(views.APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# WEB SITES
class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "core/session_list.html", context= {
                "logged":False,
            })
        else:
            sessions = StudySession.objects.filter(user=request.user)
            count = sessions.count()
            return render(request, "core/session_list.html", context= {
                "logged":True,
                "sessions":sessions,
                "count":count,
                "user":request.user
            })
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "core/register.html"

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "core/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

class ProfileView(View):
    def get(self, request, user_id):
        if not request.user.is_authenticated:
            return render(request, "core/profile.html", context= {
                "logged":False,
            })
        else:
            user_profile = get_object_or_404(UserProfile, user__id=user_id)
            return render(request, "core/profile.html", context= {
                "logged":True,
                "user":request.user,
                "user_profile":user_profile
            })