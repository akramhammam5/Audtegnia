from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include, reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.home, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('chat/<int:pk>/', views.chat_view, name='chat'),
    path('new_chat/<int:pk>', views.new_chat, name='new-chat'),
    path('call/', views.videocall, name='call'),
    path('steg/', views.hide , name='steg'),
    path('extract/', views.extract , name='extract'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('record-and-send/', views.record_and_send, name='record_and_send'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='chat/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='chat/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='chat/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='chat/password_reset_complete.html'), name='password_reset_complete'),
]
