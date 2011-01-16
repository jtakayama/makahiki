from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.decorators.cache import never_cache

from components.makahiki_base import restricted
from pages.view_profile.forms import ProfileForm
from components.makahiki_facebook.models import FacebookProfile

@login_required
def index(request):
  user = request.user
  form = ProfileForm(initial={
    "display_name": user.get_profile().name,
    "alert_email": user.email,
    "event_email": user.email,
  })
  
  # Retrieve Facebook information.
  fb_profile = None
  fb_enabled = False
  try:
    import components.makahiki_facebook.facebook as facebook
    
    fb_enabled = True
    fb_user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
    if fb_user:
      try:
        fb_profile = request.user.facebookprofile
      except FacebookProfile.DoesNotExist:
        fb_profile = FacebookProfile.create_or_update_from_fb_user(request.user, fb_user)
      
  except ImportError:
    pass
  
  return render_to_response("view_profile/index.html", {
    "form": form,
    "fb_profile": fb_profile,
    "fb_enabled": fb_enabled,
  }, context_instance=RequestContext(request))

@never_cache
def profile(request, user_id, template_name="makahiki_profiles/profile.html"):    
    other_user = get_object_or_404(User, pk=user_id)
    
    # Check that the user has permission to view this profile.
    if request.user.is_authenticated():
        if request.user == other_user:
          is_me = True
        elif other_user.get_profile().floor == request.user.get_profile().floor or request.user.is_staff: 
          is_me = False
        else:
          return restricted(request, "You are not allowed to view this user's profile page.")
    else:
        return restricted(request, "You are not allowed to view this user's profile page.")
        
    # Create initial return dictionary.
    return_dict = {
        "is_me": is_me,
        "activities_enabled": False,
        "other_user": other_user,
        "floor": other_user.get_profile().floor,
    }
    
    # Load activities for the user.
    try:
      from components.activities import get_incomplete_task_members
      return_dict["activities_enabled"] = True
      
      user_activities = get_incomplete_task_members(other_user)
      return_dict["user_commitments"] = user_activities["commitments"]
      return_dict["user_activities"] = user_activities["activities"]
    
    except ImportError:
      pass
      
    # Load standings for user.
    try:
      from components.standings import generate_standings_for_profile
      
      return_dict["standings"] = generate_standings_for_profile(other_user, is_me)
      
    except ImportError:
      pass
      
    # Retrieve the current energy goal.
    try:
      from components.energy_goals import get_info_for_user
      
      if is_me:
        return_dict["energy_goal"] = get_info_for_user(other_user)
    except ImportError:
      pass
      
    return render_to_response(template_name, return_dict, context_instance=RequestContext(request))

@login_required
def profile_edit(request, form_class=ProfileForm, **kwargs):
    
    template_name = kwargs.get("template_name", "makahiki_profiles/profile_edit.html")
    
    if request.is_ajax():
        template_name = kwargs.get(
            "template_name_facebox",
            "makahiki_profiles/profile_edit_facebox.html"
        )
    
    profile = request.user.get_profile()
    
    if request.method == "POST":
        profile_form = form_class(request.POST, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect(reverse("profile_detail", args=[profile.pk]))
    else:
        profile_form = form_class(instance=profile)
        
    fb_profile = None
    fb_enabled = False
    try:
      import makahiki_facebook.facebook as facebook
      
      fb_enabled = True
      fb_user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_APP_ID, settings.FACEBOOK_SECRET_KEY)
      if fb_user:
        try:
          fb_profile = request.user.facebookprofile
        except FacebookProfile.DoesNotExist:
          fb_profile = FacebookProfile.create_or_update_from_fb_user(request.user, fb_user)
        
    except ImportError:
      pass
      
    return render_to_response(template_name, {
        "profile": profile,
        "profile_form": profile_form,
        "fb_profile": fb_profile,
        "fb_enabled": fb_enabled,
    }, context_instance=RequestContext(request))
