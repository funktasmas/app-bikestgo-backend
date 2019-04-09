from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # api
    path('api/store/', include('apps.store.api.urls'), name='api_store'),
]
