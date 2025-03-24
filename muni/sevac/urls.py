# urls.py
from django.urls import path
from .views import HomeSevacView
urlpatterns = [
    path('', HomeSevacView.as_view(), name='homeSevac'), 

]
