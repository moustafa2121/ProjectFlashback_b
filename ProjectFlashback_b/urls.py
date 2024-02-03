from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('ProjectFlashback_b_app.urls')),
]
