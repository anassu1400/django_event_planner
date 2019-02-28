"""event_planner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    EventList,
    EventDetail,
    EventCreate,
    EventUpdate,
    EventDelete,
    OrganizerEventList,
    RegisterView,
    UserBookingList,
    Following,
)
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),

    path('api/login/', obtain_jwt_token, name='api-login'),
    path('api/register/', RegisterView.as_view(), name='api-register'),

    path('api/', EventList.as_view(), name='api-list'),
    path('api/organizer_events/<int:user_id>/', OrganizerEventList.as_view(), name='api-organizer-list'),
    path('api/bookings/', UserBookingList.as_view(), name='api-user-booking'),
    path('api/<int:event_id>/', EventDetail.as_view(), name='api-detail'),
    path('api/add/', EventCreate.as_view(), name='api-create'),
    path('api/<int:event_id>/update/', EventUpdate.as_view(), name='api-update'),
    path('api/<int:event_id>/delete/', EventDelete.as_view(), name='api-delete'),
    path('api/following/', Following.as_view(), name='api-following'),

]


if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)