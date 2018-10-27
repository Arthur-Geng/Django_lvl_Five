from django.urls import path
from Application import views

app_name = 'application'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('special', views.special, name='special'),
    path('', views.SchoolListView.as_view(), name='list'),
    path('show', views.show, name = 'show'),

]
