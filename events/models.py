from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # temporarily allow null for existing events
        blank=True,
        related_name='events_created'
    )
    registered_users = models.ManyToManyField(
        User,
        related_name='registered_events',
        blank=True,
        editable=False
    )

    def __str__(self):
        return self.title

    def clean(self):
        """
        Validate that only ADMIN users can create an event.
        """
        if self.created_by and self.created_by.role != User.ADMIN:
            raise ValidationError("Only ADMIN users can create events.")

    def save(self, *args, **kwargs):
        # run validation before saving
        self.clean()
        super().save(*args, **kwargs)

    def register_user(self, user):
        if user.role != User.ALUMNI:
            raise ValidationError("Only ALUMNI users can register for this event.")

        # Make sure this Event instance is saved before adding users
        if self.pk is None:
            self.save()  # Save the event first if not already saved

        # Check if the user is already registered
        if not EventRegistration.objects.filter(event=self, user=user).exists():
            # Create the EventRegistration log
            EventRegistration.objects.create(event=self, user=user)
            # Add the user to the ManyToMany field
            self.registered_users.add(user)  # add() automatically saves the relation



class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')  # prevent duplicate registrations

    def __str__(self):
        return f"{self.user} registered for {self.event}"
