from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

class EventModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myevents')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-create', kwargs={'event_id':self.id})

    def seats_left(self):        
        return self.seats - sum(self.bookings.all().values_list('seats', flat=True))
        


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mybookings')
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE, related_name='bookings')
    seats = models.IntegerField()

    def time_left(self):
        return int(self.event.time.hour - (datetime.datetime.now().hour))

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
