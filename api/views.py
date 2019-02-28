from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from events.models import EventModel, Booking, Follow
from django.contrib.auth.models import User

from .serializers import(
    EventListSerializer,
    OrganizerListSerializer,
    EventDetailSerializer,
    EventCreateUpdateSerializer,
    RegisterSerializer,
    UserBookingListSerializer,
    FollowingSerializer,
    FollowSerializer,
    # UserSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsNoob
from rest_framework.filters import SearchFilter, OrderingFilter
import datetime

class Following(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [AllowAny, IsAuthenticated,]
    def get_queryset(self):
        user = self.request.user
        print(user.followings.filter(follower=user))
        return user.followings.filter(follower=user)

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class EventList(ListAPIView):
    # queryset = EventModel.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [AllowAny,]
    filter_backends = [SearchFilter, OrderingFilter,]
    search_fields = ['title', 'description', 'organizer',]

    def get_queryset(self):
        return EventModel.objects.filter(date__gte=datetime.date.today())

class OrganizerEventList(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = OrganizerListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'


class UserBookingList(ListAPIView):
    # queryset = user.mybookings.all()
    serializer_class = UserBookingListSerializer
    
    def get_queryset(self):
        user = self.request.user
        return user.mybookings.filter(user=user)

# class BookerView(RetrieveAPIView):
#     """docstring for BookerView"""
#     serializer_class = UserSerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = 'event_id'

#     def get_queryset(self):
#         return EventModel.bookings.objects.all().values_list('user', flat=True)

        
class EventDetail(RetrieveAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [AllowAny,]

class EventCreate(CreateAPIView):
    serializer_class = EventCreateUpdateSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventUpdate(RetrieveUpdateAPIView):
    queryset = EventModel.objects.all()
    serializer_class = EventCreateUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsNoob,]

class EventDelete(DestroyAPIView):
    queryset = EventModel.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsNoob,]
