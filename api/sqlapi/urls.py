from django.urls import path,include
from sqlapi import views
urlpatterns = [
    path('register/',view=views.register,name="register"),
    path('login/',view=views.login_view,name="login"),
    path('input/',view=views.user_input_view,name="input"),

]
