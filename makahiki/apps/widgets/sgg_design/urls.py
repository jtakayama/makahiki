'''
URLs definition for the SGG Designer.
Created on Feb 4, 2013

@author: Cam Moore
'''

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<action_type>[\w]+)/(?P<slug>[\w\d\-]+)/$',
        'apps.widgets.sgg_design.views.view_action',
        name='action_details'),
    url(r'^update_smart_grid/$',
        'apps.widgets.sgg_design.views.update_sgg',
        name="update_smart_grid"),
)
