from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', Home.as_view(), name="home"),
                  path("register/", register, name="register"),
                  path("login/", user_login, name="login"),
                  path("logout/", user_logout, name="logout"),
                  path("delete/", user_delete, name="delete"),
                  path('event/<int:pk>/', event, name="event"),
                  path('event/create/', event_create, name="createevent"),
                  path('profile/<str:slug>/', profile, name="profile"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
