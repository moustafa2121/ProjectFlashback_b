from . import views
from django.urls import path, include

app_name = "ProjectFlashback_b_app"
urlpatterns = [
    path('', views.testView, name='testView'),
]