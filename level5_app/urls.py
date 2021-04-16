from django.urls import path
from level5_app import views

app_name = 'level5_app'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('user_login/', views.user_login, name='user_login'),
]
