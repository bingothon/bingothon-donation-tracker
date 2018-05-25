from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import ugettext_lazy

import tracker.views

# Set custom headers for admin site based on site name in settings.
admin.AdminSite.site_title = ugettext_lazy('{} site admin'.format(settings.SITE_NAME))
admin.AdminSite.site_header = ugettext_lazy('{} administration'.format(settings.SITE_NAME))

prefix = ''
if settings.SITE_PREFIX.strip('/'):
    prefix = settings.SITE_PREFIX.lstrip('/')

urlpatterns = [
    path(prefix, include('tracker.urls')),
    path(prefix + 'admin/lookups/', include('ajax_select.urls')),
    path(prefix + 'admin/', admin.site.urls),
    path(prefix + 'logout', tracker.views.logout),
]

try:
    import importlib

    importlib.import_module('tracker_ui')
    urlpatterns.append(path(prefix + 'ui', include('tracker_ui.urls')), )
except ModuleNotFoundError:
    print("Could not locate tracker_ui module, starting without it")
