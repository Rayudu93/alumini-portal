from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from accounts.models import User
from .models import Query, Answer
from accounts.permissions import IsStudent, IsAlumni
from notifications.models import Notification
from .serializers import QuerySerializer



class QueryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Student → only their queries
        if user.role == User.STUDENT:
            queries = Query.objects.filter(student=user)

        # Alumni → all queries
        elif user.role == User.ALUMNI:
            queries = Query.objects

        else:
            queries = Query.objects.none()

        queries = queries.order_by("-created_at")
        serializer = QuerySerializer(queries, many=True)
        return Response(serializer.data)


class CreateQueryView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        query = Query.objects.create(
            student=request.user,
            title=request.data["title"],
            description=request.data["description"]
        )
        return Response({"id": query.id})


class AcceptQueryView(APIView):
    permission_classes = [IsAuthenticated, IsAlumni]

    def post(self, request, query_id):
        query = Query.objects.get(id=query_id)
        query.accepted_by = request.user
        query.status = "ACCEPTED"
        query.save()

        alumni_name = request.user.get_full_name() or request.user.email

        Notification.objects.create(
            user=query.student,
            message=f"Your query was accepted by alumni {alumni_name}"
        )

        return Response({"message": "Query accepted"})




class AnswerQueryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, query_id):
        """
        Only students can view answers
        """
        # Use query_id field instead of pk
        query = get_object_or_404(Query, query_id=query_id)
        answers = Answer.objects.filter(query=query)

        data = [
            {
                "id": answer.id,
                "content": answer.content,
                "alumni": answer.alumni.username,
                "created_at": answer.created_at,
            }
            for answer in answers
        ]

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, query_id):
        """
        Only alumni can answer
        """
        # Check if user is alumni
        if not hasattr(request.user, "role") or request.user.role != "ALUMNI":
            return Response(
                {"error": "Only alumni can answer queries"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Use query_id field to get the query
        query = get_object_or_404(Query, query_id=query_id)

        # Create the answer
        answer = Answer.objects.create(
            query=query,
            alumni=request.user,
            content=request.data.get("content")
        )

        # Mark query as completed
        query.status = "COMPLETED"
        query.save()

        alumni_name = request.user.get_full_name() or request.user.email
        # Notify the student
        Notification.objects.create(
            user=query.student,
            message=f'Your query has been answered {alumni_name}'
        )

        return Response(
            {"message": "Answer submitted and query marked as completed"},
            status=status.HTTP_201_CREATED
        )