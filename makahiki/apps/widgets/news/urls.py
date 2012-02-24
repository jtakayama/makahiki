from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('',
    url(r'^popular-tasks/$', 'widgets.news.views.get_popular_tasks', name="news_popular_tasks"),
    url(r'^team-members/$', 'widgets.news.views.team_members', name="news_team_members"),
)
