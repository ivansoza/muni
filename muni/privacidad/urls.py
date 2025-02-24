from django.urls import path
from .views import HomePrivacidad

urlpatterns = [
    path('', HomePrivacidad.as_view(), name='HomePrivacidad'), 

]