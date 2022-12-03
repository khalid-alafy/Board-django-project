from django.contrib import admin
from django.urls import path,include 
from boards import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('boards.board_url'),name="index"),
    path('', include('accounts.url'),name="index"),
]
