from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Default URL pattern
    path('', RedirectView.as_view(pattern_name='login'), name='home'),  # Redirect to login page by default

    # Admin URLs
    path('admin/', admin.site.urls),

    # Include URLs of the 'tyr' app
    path('', include('tyr.urls')),

    # Add URLs for other apps here

]
