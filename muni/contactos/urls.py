from django.urls import path
from .views import HomeContactsView

urlpatterns = [
    path('', HomeContactsView.as_view(), name='homeContacts'), 
]