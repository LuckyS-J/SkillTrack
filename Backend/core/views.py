from django.shortcuts import render, redirect
from rest_framework import views, status
from rest_framework.response import Response
from .models import Skill, StudySession, User, UserProfile
from .serializers import SkillSerializer, StudySessionSerializer, UserSerializer, UserProfileSerializer, RegisterSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import StudySessionForm, SkillForm, CustomAuthenticationForm, CustomUserCreationForm
from django.db.models import Avg, Sum, Count
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
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
            return render(request, "core/session_list.html", context={
                "logged": False,
            })
        else:
            sessions = StudySession.objects.filter(user=request.user)
            count = sessions.count()
            return render(request, "core/session_list.html", context={
                "logged": True,
                "sessions": sessions,
                "count": count,
                "user": request.user
            })


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "core/register.html"


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "core/login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")


class ProfileView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request, user_id):
        if not request.user.is_authenticated:
            return render(request, "core/profile.html", context={
                "logged": False,
            })
        else:
            user_profile = get_object_or_404(UserProfile, user__id=user_id)
            return render(request, "core/profile.html", context={
                "logged": True,
                "user": request.user,
                "user_profile": user_profile
            })


class AddStudySessionView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = StudySessionForm(user=request.user)
        return render(request, "core/session_add.html", {"form": form})

    def post(self, request):
        form = StudySessionForm(request.POST, user=request.user)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect("home")
        else:
            return render(request, "core/session_add.html", {"form": form})


class AddSkillView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = SkillForm()
        return render(request, "core/skill_add.html", {"form": form})

    def post(self, request):
        form = SkillForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect("home")
        else:
            return render(request, "core/skill_add.html", {"form": form})


class DashboardView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        sessions = StudySession.objects.filter(user=request.user)
        if sessions.exists():
            total_sessions = sessions.count()
            total_duration = sessions.aggregate(
                Sum("duration"))["duration__sum"]
            
            avg_duration = sessions.aggregate(Avg("duration"))["duration__avg"]
            if avg_duration:
                average_duration = avg_duration.total_seconds() / 60
            else:
                average_duration = 0

            last_session = (StudySession.objects.filter(
                user=request.user).order_by('-date')).first()

            # Charts
            top_categories_qs = sessions.values('skill__category').annotate(total=Count('id')).order_by('-total')[:3]
            top_categories_labels = [c['skill__category'] or 'Uncategorized' for c in top_categories_qs]
            top_categories_data = [c['total'] for c in top_categories_qs]

            daily_sessions_qs = sessions.values('date').annotate(total=Sum('duration')).order_by('date')
            daily_labels = [DateFormat(item['date']).format(
                'Y-m-d') for item in daily_sessions_qs]
            daily_data = [
                round(item['total'].total_seconds() /
                      60, 1) if item['total'] else 0
                for item in daily_sessions_qs
            ]

            return render(request, "core/dashboard.html", context={
                "is_session": True,
                "total_sessions": total_sessions,
                "total_hours": total_duration,
                "average_session_duration": average_duration,
                "top_categories": {
                    "labels": top_categories_labels,
                    "data": top_categories_data,
                },
                "daily_study": {
                    "labels": daily_labels,
                    "data": daily_data,
                },
                "last_session": last_session,
            })

        else:
            return render(request, "core/dashboard.html", {"is_session": False})


class EditStudySessionView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request, pk):
        session = get_object_or_404(StudySession, pk=pk, user=request.user)
        form = StudySessionForm(instance=session, user=request.user)
        return render(request, "core/session_edit.html", {"form": form, "session": session})

    def post(self, request, pk):
        session = get_object_or_404(StudySession, pk=pk, user=request.user)
        form = StudySessionForm(
            request.POST, instance=session, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, "core/session_edit.html", {"form": form, "session": session})


class AllSkillsView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "core/skill_list.html", context={
                "logged": False,
            })
        else:

            skills = Skill.objects.filter(user=request.user)
            count = skills.count()
            return render(request, "core/skill_list.html", context={
                "logged": True,
                "skills": skills,
                "count": count,
                "user": request.user
            })


class EditSkillView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request, pk):
        skill = get_object_or_404(Skill, pk=pk, user=request.user)
        form = SkillForm(instance=skill)
        return render(request, "core/skill_edit.html", {"form": form, "session": skill})

    def post(self, request, pk):
        skill = get_object_or_404(Skill, pk=pk, user=request.user)
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, "core/skill_edit.html", {"form": form, "session": skill})


class DeleteStudySessionView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def post(self, request, pk):
        session = get_object_or_404(StudySession, pk=pk, user=request.user)
        session.delete()
        return redirect("home")


class DeleteSkillView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def post(self, request, pk):
        skill = get_object_or_404(Skill, pk=pk, user=request.user)
        skill.delete()
        return redirect("home")
