from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt import CustomTokenObtainPairSerializer
from .permissions import IsStudent, IsAlumni
from .models import StudentProfile, AlumniProfile

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        if role not in ["STUDENT", "ALUMNI"]:
            return Response(
                {"error": "Invalid role"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            email=email,
            password=password,
            role=role
        )

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        StudentProfile.objects.create(
            user=request.user,
            department=request.data["department"],
            graduation_year=request.data["graduation_year"],
            bio=request.data.get("bio", "")
        )
        return Response({"message": "Student profile created"})


class AlumniProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAlumni]

    def post(self, request):
        AlumniProfile.objects.create(
            user=request.user,
            company=request.data["company"],
            designation=request.data["designation"],
            experience=request.data["experience"]
        )
        return Response({"message": "Alumni profile created"})
