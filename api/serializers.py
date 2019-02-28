from rest_framework import serializers
from events.models import EventModel, Booking, Follow
from django.contrib.auth.models import User






class UserSerializer(serializers.ModelSerializer):
    follow_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'followings', 'followers','follow_count',]
    def get_follow_count(self, obj):
        return obj.followers.count()

class FollowingSerializer(serializers.ModelSerializer):
    """docstring for FollowingSerializer"""
    class Meta:
        model = User
        fields = ['username',]
      

class FollowSerializer(serializers.ModelSerializer):
    following = FollowingSerializer()
    class Meta:
        model = Follow
        fields = ['following',]


class EventListSerializer(serializers.ModelSerializer):
    detail = serializers.HyperlinkedIdentityField(
            view_name = 'api-detail',
            lookup_field = 'id',
            lookup_url_kwarg = 'event_id',
        )
    class Meta:
        model = EventModel
        fields = ['id', 'title', 'detail']

class EventDetailSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    
    class Meta:
        model = EventModel
        fields = '__all__'

class OrganizerListSerializer(serializers.ModelSerializer):
    myevents = EventDetailSerializer(many=True)
    class Meta:
        model = User
        fields = ['myevents']


class UserBookingListSerializer(serializers.ModelSerializer):
    # mybookings = EventListSerializer(many=True)
    event = EventDetailSerializer()
    class Meta:
        model = Booking
        fields = ['event' ,'seats']


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        exclude = ['organizer',]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data
        
