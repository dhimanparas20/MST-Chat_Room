from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('', include(router.urls)),
    path('login/', views.Login.as_view(), name="login"),
    path('home/', views.Home.as_view(), name="home"),
    path('logout/', views.Logout.as_view(), name="logout"),

]
