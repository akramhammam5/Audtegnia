from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('chat/<int:pk>/', views.chat_view, name='chat'),
    path('new_chat/<int:pk>', views.new_chat, name='new-chat'),
    path('call/', views.videocall, name='call'),
]