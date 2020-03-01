from django.conf.urls import include, url

from django.contrib import admin
from django.urls import path

import tracker.urls
import ajax_select.urls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles import views

urlpatterns = [
    path('tracker/', include(tracker.urls)),
    path('admin/lookups/', include(ajax_select.urls)),
    path('admin/', admin.site.urls)
]

if settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('static/<path:path>', views.serve),
    ]
