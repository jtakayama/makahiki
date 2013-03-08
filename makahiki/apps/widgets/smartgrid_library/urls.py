'''URL definitions for the Smart Grid Game Library.
Created on Mar 8, 2013

@author: carletonmoore
'''

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<action_type>[\w]+)/(?P<slug>[\w\d\-]+)/add/$',
        'apps.widgets.smartgrid_library.views.add_action',
        name='library_add_action'),
)