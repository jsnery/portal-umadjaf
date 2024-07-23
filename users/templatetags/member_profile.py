from django import template
from users.models import UserProfiles, User


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


@register.simple_tag
def return_profile_bio(user_id):
    try:
        profile = UserProfiles.objects.get(user_id=user_id)
        return profile.bio
    except UserProfiles.DoesNotExist:
        return 'No bio available'


@register.simple_tag
def return_user_whatsapp(user_id):
    try:
        user = User.objects.get(id=user_id)
        number_filter = "".join([i for i in user.number_phone if i.isnumeric()])
        whatsapp_link = f'https://wa.me/55{number_filter}'
        return whatsapp_link
    except UserProfiles.DoesNotExist:
        return 'No whatsapp available'