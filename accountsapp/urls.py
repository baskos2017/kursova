from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('auth/', auth, name='auth'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('comment/', comments, name='comments'),
    path('activate/<int:user_id>/', activate, name='activate'),
]