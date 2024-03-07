from django import views
from django.urls import path
from .views import *

app_name = 'API'

urlpatterns = [
    path('registre', AdminRegisterView.as_view()),
    path('modules', ModuleView.as_view()),
    path('module/<uuid:pk>', ModuleView.as_view()),
    path('presences', PresenceList.as_view()),
    path('presence/<str:pk>', PresenceList.as_view()),
    path('presence/<str:pk>', PresenceView.as_view()),
    path('sessions', SessionView.as_view()),
    path('session/<uuid:pk>', SessionView.as_view()),
    path('users', UserView.as_view()),
    path('user/<uuid:pk>', UserView.as_view()),
    path('logout', LogoutView.as_view()),

]