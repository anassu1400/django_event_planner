from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
class EventModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    datetime = models.DateTimeField()
    seats = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myevents')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-create', kwargs={'event_id':self.id})

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mybookings')
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, related_name='bookings')
    seats = models.IntegerField()
