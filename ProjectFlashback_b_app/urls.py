from . import views
from django.urls import path, include

app_name = "ProjectFlashback_b_app"
urlpatterns = [
    path('<int:year>', views.testView, name='api-overview'),
]