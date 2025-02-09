from django.urls import path, include
from .views import CustomLoginView, DashboardView, PersonalizacionView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", CustomLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),  name='logout'),      
    path('mi-panel/', DashboardView.as_view(), name='dashboard'),
    path('personalizacion/', PersonalizacionView.as_view(), name='personalizacion_view'),



]