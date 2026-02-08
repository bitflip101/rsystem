from django.contrib import admin
from django.urls import path, include
# from portal.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("portal.urls")),
    # path('', home_view, name='home')

    # This line adds login, logout, password reset, etc.,
    # It also automatically looks for templates in a folder named 'registration'
    path('accounts/', include('django.contrib.auth.urls')),
]
