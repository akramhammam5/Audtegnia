from django.urls import path
from . import views
from .views import * 
urlpatterns = [
    path('', form_template_view , name='form_template_view'),
]



