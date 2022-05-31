from django.contrib import admin
from django.urls import include, path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('', include('main.urls')),
    path('main/', include('main.urls')),
    path('django-admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),

    #wagtail
    path('admin/', include(wagtailadmin_urls)),    path("accounts/", include("django.contrib.auth.urls")),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
]
