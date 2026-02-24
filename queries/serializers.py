from rest_framework import serializers
from .models import Query, Answer

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = "__all__"

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

