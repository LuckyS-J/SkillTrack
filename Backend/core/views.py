from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from .models import Skill, StudySession, User, UserProfile
from .serializers import SkillSerializer, StudySessionSerializer, UserSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404
# Create your views here.


class SkillListCreateAPIView(views.APIView):
    def get(self, request):
        queryset = Skill.objects.all()
        serializer = SkillSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillDetailAPIView(views.APIView):
    def get_skill(self, pk):
        return get_object_or_404(Skill, pk=pk)

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
