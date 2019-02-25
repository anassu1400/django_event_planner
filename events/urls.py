from django.urls import path
from .views import Login, Logout, Signup, home, event_create, event_list, event_detail, event_update, event_delete, dashboard, book

urlpatterns = [
	path('', home, name='home'),
	path('create/', event_create, name='event-create'),
	path('list/', event_list, name='event-list'),
	path('book/<int:event_id>', book, name='booking'),
	path('dashboard/', dashboard, name='dashboard'),
	path('detail/<int:event_id>/', event_detail, name='event-detail'),
	path('update/<int:event_id>/', event_update, name='event-update'),
	path('delete/<int:event_id>/', event_delete, name='event-delete'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]