'''Defines the URLs for the Smart Grid Play Tester.
Created on Jun 23, 2013

@author: Cam Moore
'''

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<action_type>[\w]+)/(?P<slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid_design_tester.views.view_action',
        name='tester_view_action'),
    url(r'^(?P<action_type>[\w]+)/(?P<slug>[\w\d\-]+)/add/$',
        'apps.widgets.smartgrid_design_tester.views.add_action',
        name='tester_activity_add'),
    url(r'^(?P<action_type>[\w]+)/(?P<slug>[\w\d\-]+)/drop/$',
        'apps.widgets.smartgrid_design_tester.views.drop_action',
        name='tester_activity_drop'),
    )
