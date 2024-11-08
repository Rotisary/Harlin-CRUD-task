from django.urls import path
from users.views import (
    register, 
    login_view, 
    logout_view,
    verify_user
)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify/<str:username>/', verify_user, name='verify-user')
]