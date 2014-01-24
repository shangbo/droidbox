from django.conf.urls import patterns, include, url

from django.contrib import admin
from droidbox_upload.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',current_datetime),
    url(r'^upfile_form/$',upload_form),
    url(r'^upfile/$',upload),
    # url(r'^time/$',current_datetime),
    # url(r'^template_time/$',current_datetime_template),
    # url(r'^time/plus/(\d{1,2})/$',hours_ahead),
    url(r'^admin/', include(admin.site.urls)),
)
