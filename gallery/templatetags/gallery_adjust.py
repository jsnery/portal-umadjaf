from django import template
from django.utils.safestring import mark_safe
from events.models import Event
from gallery.models import Gallery, GalleryMarked, GalleryMarkedUser
from users.models import User, UserProfiles

register = template.Library()

@register.simple_tag
def get_event_name(event_id):
    try:
        event = Event.objects.get(id=event_id)
        return event.title
    except Event.DoesNotExist:
        # Retorna uma string vazia ou uma mensagem de erro personalizada
        return "Evento não encontrado"


@register.simple_tag
def get_gallery_marked_confirm(user_id, gallery_id):
    try:
        gallery = Gallery.objects.get(id=gallery_id)
        gallery_marked = GalleryMarked.objects.get(gallery=gallery)
        marked_user = GalleryMarkedUser.objects.get(gallery_marked=gallery_marked, user_id=user_id)
        if marked_user.marked_confirm:
            print(marked_user.marked_confirm)
            return 'checked'
        return 'waiting'
    except Exception:
        return 'unchecked'


@register.simple_tag
def get_user_complete_name(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user.complete_name
    except User.DoesNotExist:
        return "Usuário não encontrado"


@register.simple_tag
def get_user_picture(user_id):
    user = User.objects.get(id=user_id)
    profile = UserProfiles.objects.get(user_id=user)
    return profile.profile_picture.url
