from managers.team_mgr.models import Post
from widgets.news.forms import WallForm

from widgets.smartgrid import get_available_golow_activities

def supply(request):
    user = request.user
    team = user.get_profile().team
    golow_activities = get_available_golow_activities(user)
    golow_posts = Post.objects.filter(team=team, style_class="user_post").select_related(
        'user__profile').order_by("-id")[:5]

    return {
        "golow_activities": golow_activities,
        "posts": golow_posts,
        "wall_form": WallForm(),
        }