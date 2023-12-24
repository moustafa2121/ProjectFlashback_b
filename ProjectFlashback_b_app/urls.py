from . import views
from django.urls import path, include

app_name = "ProjectFlashback_b_app"
urlpatterns = [
    path('<int:year>/<int:batch>', views.phase1View, name='phase1View'),
]