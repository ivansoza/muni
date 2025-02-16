from django.urls import path, include
from .views import CustomLoginView, DashboardView, NewsView, PersonalizacionView,SocialMediaView,ServicesView, custom_upload_function, agregar_categoria, eliminar_noticia, editar_noticia
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", CustomLoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(next_page='home'),  name='logout'),      
    path('mi-panel/', DashboardView.as_view(), name='dashboard'),
    path('personalizacion/', PersonalizacionView.as_view(), name='personalizacion_view'),
    path('social-media/', SocialMediaView.as_view(), name='social_view'),
    path('noticias/', NewsView.as_view(), name='noticias_view'),
    path('servicios/', ServicesView.as_view(), name='servicios_view'),
    path("upload/", custom_upload_function, name="custom_upload_file"),
    path('agregar-categoria/', agregar_categoria, name='agregar_categoria'),
    path('editar-noticia/<int:noticia_id>/', editar_noticia, name='editar_noticia'),
    path('eliminar-noticia/<int:noticia_id>/', eliminar_noticia, name='eliminar_noticia'),

]