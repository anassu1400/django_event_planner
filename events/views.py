from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import (
    UserSignup,
    UserLogin,
    EventForm,
    BookingForm,
    ProfileForm,
    )
from .models import EventModel, Booking, Follow, User
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
import datetime
from django.db.models import Q
from django.http import JsonResponse

from django.core.mail import send_mail
from django.conf import settings

def home(request):
    events = EventModel.objects.all()[:3]
    context ={
        'events': events
    }
    return render(request, 'home.html', context)

#doubles as details page
def book(request, event_id):
    #permissions
    if request.user.is_anonymous:
        return redirect('login')
    #get the event we'd like to book
    event = EventModel.objects.get(id=event_id)
    #get the bookings that are to this event
    bookings = Booking.objects.filter(event=event)
    #get number of seats set for the event
    form = BookingForm()
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            my_seats = form.cleaned_data['seats']
            # new_seats = event.seats - my_seats
            seats = event.seats_left()
            if my_seats > seats:
                messages.warning(request, "The event doesn't have enough seats.")
            else:
                book = Booking(user= request.user, event= event, seats = my_seats)
                book.save()
                title = 'Thank you for booking with '+str(book.event.organizer.username)
                content = 'Dear, ' + str(request.user.username) + '\nhere are the details of your booking: \n'+'event: ' + str(event.title) +'\ndate and time: ' + str(event.date) + ', ' + str(event.time) + '\nat: ' + event.location + '\n with ' + str(my_seats) + ' seats.'  + '\nthank you for using our website!'
                send_mail(
                    title,
                    content, 
                  settings.EMAIL_HOST_USER,
                  [request.user.email],
                 )
                messages.success(request, "Booking successful.")
                return redirect('event-detail', event_id)
    context = {
        "form":form,
        "event": event,
        "bookings": bookings,
    }
    return render(request, 'event_detail.html', context)


def event_create(request):
    if request.user.is_anonymous:
        return redirect("login")
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            title = 'A new event by '+str(event.organizer.username) + ' check it out!'
            content = 'Dear, ' + request.user.username + '\nhere are the details of the new event: \n' + 'event: ' + str(event.title) +'\ndate and time: ' + str(event.date) + ', ' + str(event.time) + '\nat: ' + event.location + '\n with ' + str(event.seats) + ' seats.' + '\nthank you for using our website!'
            print(event.organizer.followers.values_list('follower__email', flat=True))
            send_mail(
                            title,
                            content,
                            settings.EMAIL_HOST_USER,
                            event.organizer.followers.values_list('follower__email', flat=True),
                            fail_silently=False)
            return redirect('event-detail', event.id)
    context = {
        'eventform' : form,
        }
    return render(request, 'create_event.html', context)


def event_update(request, event_id):
    event_obj = EventModel.objects.get(id=event_id)
    if not (request.user.is_staff or request.user == event_obj.organizer):
        return redirect('login')
    form = EventForm(instance=event_obj)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    context = {
        "event_obj": event_obj,
        "form":form,
    }
    return render(request, 'event_update.html', context)


def dashboard(request):
    my_events = request.user.myevents.all()
    my_bookings = request.user.mybookings.all()
    unique_bookings = list(set(my_bookings))
    context = {
        "events": my_events,
        "bookings": unique_bookings,
    }
    return render(request, 'dashboard.html', context)


def event_delete(request, event_id):
    if not request.user.is_staff:
        return redirect('login')
    EventModel.objects.get(id=event_id).delete()
    return redirect('home')

#list view with search bar
def event_list(request):
    events = EventModel.objects.filter(date__gte=datetime.date.today())
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(organizer__username__icontains=query)
        ).distinct()
    context = {
       "events": events,
    }
    return render(request, 'event_list.html', context)


class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


#delete the reservation if possible!
def reservation_delete(request, event_id, booking_id):
    event_reservation = Booking.objects.get(id=booking_id)
    event = event_reservation.event
    if event_reservation.time_left() <= 3 and event.date <= datetime.date.today():
        messages.warning(request, "You can't delete the reservation, Too late!")
        return redirect('dashboard')
    else:
        event_reservation.delete()
        messages.success(request, "successfully Deleted, Find another event!")
        return redirect('dashboard')


def my_profile(request):
    if request.user.is_anonymous:
        return redirect('login')
    context={
        'user': request.user
    }
    return render(request, 'profile.html', context)

def update_profile(request):
    user = request.user
    if request.user.is_anonymous:
        return redirect('login')
    form = ProfileForm(instance=user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('my-profile')
    context = {
        "user": user,
        "form":form,
    }
    return render(request, 'profile_update.html', context)

def profile(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    user = User.objects.get(id=user_id)
    follow_list = []
    if request.user.is_authenticated:
        follow_list = user.followers.all().values_list('follower', flat=True)
    events = user.myevents.all()
    context={
        'user': user,
        'events': events,
        'follow_list': follow_list,
    }
    return render(request, 'profile.html', context)

def follow(request, user_id):
    follow = User.objects.get(id=user_id)

    if request.user.is_anonymous:
        return redirent('login')
    
    follow, created = Follow.objects.get_or_create(follower=request.user, following=follow)
    if created:
        action = 'followed'
    else:
        follow.delete()
        action = 'unfollowed'
    response = {
        "action": action,
    }
    return JsonResponse(response, safe=False)


