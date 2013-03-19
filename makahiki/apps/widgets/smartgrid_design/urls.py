'''
URLs definition for the SGG Designer.
Created on Feb 4, 2013

@author: Cam Moore
'''

from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^newcat/(?P<cat_slug>[\w\d\-]+)/(?P<level_slug>[\w\d\-]+)/(?P<priority>[\d]+)/$',
        'apps.widgets.smartgrid_design.views.instantiate_category',
        name='instantiate_category'),
    url(r'^newaction/(?P<action_slug>[\w\d\-]+)/(?P<cat_slug>[\w\d\-]+)/(?P<level_slug>[\w\d\-]+)' +
        '/(?P<priority>[\d]+)/$',
        'apps.widgets.smartgrid_design.views.instantiate_action',
        name='instantiate_action'),
    url(r'^delete_action/(?P<action_slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid_design.views.delete_action',
        name='delete_action'),
    url(r'^delete_category/(?P<cat_slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid_design.views.delete_category',
        name='delete_category'),
    url(r'^clear_from_grid/(?P<action_slug>[\w\d\-]+)/$',
        'apps.widgets.smartgrid_design.views.clear_from_grid',
        name='clear_from_grid'),
)
