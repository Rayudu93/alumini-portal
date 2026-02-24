# events/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Event
from .serializers import EventSerializer
from accounts.permissions import IsAlumni


class CreateEventView(APIView):
    permission_classes = [IsAuthenticated, IsAlumni]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.save(created_by=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class EventListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = Event.objects.all().order_by("-date")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class RegisterEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if event.registered_users.filter(id=request.user.id).exists():
            return Response(
                {"detail": "Already registered"},
                status=status.HTTP_400_BAD_REQUEST
            )

        event.registered_users.add(request.user)
        return Response({"detail": "Registered successfully"})

class MyRegisteredEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = request.user.registered_events.all().order_by("-date")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
