from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^view_rejected/(\d+)/$', 'widgets.profile.views.view_rejected', name="profile_rejected"),
)
