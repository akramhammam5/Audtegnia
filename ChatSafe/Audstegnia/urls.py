from django.urls import path
from . import views
from .views import * 
urlpatterns = [
    path('', hide , name='form_template_view'),
    path('extract/', extract , name='extract'),
]



