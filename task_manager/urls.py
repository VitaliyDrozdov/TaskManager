from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from tasks.views import redirect_to_tasks

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("tasks.urls")),
    path("", redirect_to_tasks),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
