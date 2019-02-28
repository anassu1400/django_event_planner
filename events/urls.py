from django.urls import path
from .views import (
	Login,
	Logout,
	Signup,
	home,
	event_create,
	event_list,
	event_update,
	event_delete,
	dashboard,
	book,
	reservation_delete,
	my_profile,
	update_profile,
	profile,
	follow,
	)

urlpatterns = [
	path('', home, name='home'),
	path('create/', event_create, name='event-create'),
	path('list/', event_list, name='event-list'),
	path('dashboard/', dashboard, name='dashboard'),
	path('detail/<int:event_id>/', book, name='event-detail'),
	path('update/<int:event_id>/', event_update, name='event-update'),
	path('delete/<int:event_id>/', event_delete, name='event-delete'),
	path('delete/reservation/<int:event_id>/<int:booking_id>/', reservation_delete, name='reservation-delete'),

	path('profile/', my_profile, name='my-profile'),
	path('profile/update/', update_profile, name='profile-update'),

	path('profile/<int:user_id>/', profile, name='profile'),
	path('profile/<int:user_id>/follow/', follow, name='follow'),

    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]