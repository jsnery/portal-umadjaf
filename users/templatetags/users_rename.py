from django import template
from users.models import UserProfiles


register = template.Library()

@register.simple_tag
def return_first_name(complete_name):
    return complete_name.split()[0]


@register.simple_tag
def return_profile_picture(user_id):
    try:
        profile = UserProfiles.objects.get(user_id=user_id)
        return profile.profile_picture.url
    except UserProfiles.DoesNotExist:
        return 'users/profile_pictures/default.jpg'