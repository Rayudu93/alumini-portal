from django.db import models
from accounts.models import User

class Query(models.Model):
    
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"

    STATUS_CHOICES = [
        (OPEN, "Open"),
        (ACCEPTED, "Accepted"),
        (COMPLETED,"Completed")
    ]

    query_id = models.CharField(max_length=8, unique=True, editable=False, null=True, blank=True)

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries")
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    accepted_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="accepted_queries"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.query_id:
            last_query = Query.objects.order_by('-id').first()
            if last_query:
                last_id = int(last_query.query_id[1:])
                new_id = last_id + 1
            else:
                new_id = 1
            self.query_id = f"Q{new_id:07d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.query_id



class Answer(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    alumni = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
