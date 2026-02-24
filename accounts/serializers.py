# api/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.password_validation import validate_password

from .models import User, StudentProfile, AlumniProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    # Student fields
    department = serializers.CharField(required=False)
    graduation_year = serializers.IntegerField(required=False)

    # Alumni fields
    company = serializers.CharField(required=False)
    designation = serializers.CharField(required=False)
    experience = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = (
            "email", "password", "password2", "role",
            "department", "graduation_year",
            "company", "designation", "experience",
        )

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")

        role = data.get("role")

        if role == User.STUDENT and not all([data.get("department"), data.get("graduation_year")]):
            raise serializers.ValidationError("Student profile data missing")

        if role == User.ALUMNI and not all([data.get("company"), data.get("designation")]):
            raise serializers.ValidationError("Alumni profile data missing")

        return data

    @transaction.atomic
    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        validated_data.pop("password2")

        student_data = {
            "department": validated_data.pop("department", None),
            "graduation_year": validated_data.pop("graduation_year", None),
        }

        alumni_data = {
            "company": validated_data.pop("company", None),
            "designation": validated_data.pop("designation", None),
            "experience": validated_data.pop("experience", None),
        }

        user = User.objects.create(email=validated_data["email"], role=role)
        user.set_password(password)
        user.save()

        if role == User.STUDENT:
            StudentProfile.objects.create(user=user, **student_data)

        if role == User.ALUMNI:
            AlumniProfile.objects.create(user=user, **alumni_data)

        return user
