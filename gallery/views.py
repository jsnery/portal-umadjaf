from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.http import JsonResponse
from users.models import IsUmadjaf, Roles, User, UserProfiles, UserRoles
from events.models import Event
from .models import Gallery, GalleryMarked, GalleryMarkedUser
from django.http import HttpResponseRedirect
from datetime import datetime


def gallery(request):
    gallerie = Gallery.objects.all().order_by('-id')
    events = Event.objects.all().order_by('-id')
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        user_id = request.user.id
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
        member_ok = IsUmadjaf.objects.filter(user_id=request.user).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=request.user).checked
    else:
        user_id = 0
        is_admin = False
        is_media_manager = False
        is_umadjaf = False

    return render(
        request, 'gallery/pages/gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_umadjaf': is_umadjaf,
            'user_id': user_id,
            'galleries': gallerie,
            'events': events
        }
    )


def search_gallery(request):
    galleries = Gallery.objects.all().order_by('-id')
    events = Event.objects.all().order_by('-id')
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        user_id = request.user.id
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
        member_ok = IsUmadjaf.objects.filter(user_id=request.user).exists()
        if member_ok:
            is_umadjaf = IsUmadjaf.objects.get(user_id=request.user).checked
    else:
        user_id = 0
        is_admin = False
        is_media_manager = False
        is_umadjaf = False

    search = request.GET.get('eventSelect')
    print("Pesquisa: ", search)
    if search:
        galleries = Gallery.objects.filter(event_id=search).order_by('-id')

        if search == '0':
            galleries = Gallery.objects.filter(event_id__gt=1000).order_by('-id')

        if search == '':
            galleries = Gallery.objects.all().order_by('-id')

    return render(
        request, 'gallery/pages/gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'is_umadjaf': is_umadjaf,
            'user_id': user_id,
            'galleries': galleries,
            'events': events
        }
    )


def gallery_marked_user_manager(request):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
    else:
        is_admin = False
        is_media_manager = False

    if not is_authenticated:
        return redirect('users:login')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    galleries_marked_user = GalleryMarkedUser.objects.all().order_by('-id')

    return render(
        request, 'gallery/pages/manager_gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'galleries_marked': galleries_marked_user,
        }
    )


def add_to_gallery(request):
    notification = False

    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
    else:
        is_admin = False
        is_media_manager = False

    if not is_authenticated:
        return redirect('users:login')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    all_events = Event.objects.all().order_by('-id')
    # all_members = User.objects.filter(isumadjaf__checked=True).order_by('-complete_name')

    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        image = request.FILES.get('image')
        author_id = request.user.id

        if not Event.objects.filter(id=event_id).exists():
            event_date = request.POST.get('event_date')
            if event_date == '':
                notification = True
                return render(
                    request,
                    'gallery/pages/add_to_gallery.html',
                    context={
                        'is_authenticated': is_authenticated,
                        'is_admin': is_admin,
                        'is_media_manager': is_media_manager,
                        'all_events': all_events,
                        'notification': notification
                    }
                )
            event_date_ = datetime.strptime(event_date, '%Y-%m-%d')
        else:
            event_date_ = Event.objects.get(id=event_id).date

        if event_id == 0 or event_id == '0':
            event_id = int(''.join([i for i in event_date if i.isdigit()]))

        gallery = Gallery(
            event_id=event_id,
            event_date=event_date_,
            image=image,
            author_id=author_id
        )
        gallery.save()

        gallery_marked = GalleryMarked(gallery=gallery)
        gallery_marked.save()

        return redirect('gallery:add_to_gallery')

    return render(
        request,
        'gallery/pages/add_to_gallery.html',
        context={
            'is_authenticated': is_authenticated,
            'is_admin': is_admin,
            'is_media_manager': is_media_manager,
            'all_events': all_events,
            'notification': notification
        }
    )


def mark_gallery(request, gallery_id):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        if IsUmadjaf.objects.filter(user_id=request.user).exists():
            is_umadjaf = IsUmadjaf.objects.get(user_id=request.user).checked
    else:
        is_umadjaf = False

    if not is_umadjaf:
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=gallery_id)
    gallery_marked = GalleryMarked.objects.get(gallery=gallery)
    user_id = request.user.id

    solicitation = GalleryMarkedUser(gallery_marked=gallery_marked, user_id=user_id)
    solicitation.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unmark_gallery(request, gallery_id):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        if IsUmadjaf.objects.filter(user_id=request.user).exists():
            is_umadjaf = IsUmadjaf.objects.get(user_id=request.user).checked
    else:
        is_umadjaf = False

    if not is_umadjaf:
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=gallery_id)
    gallery_marked = GalleryMarked.objects.get(gallery=gallery)
    user_id = request.user.id

    solicitation = GalleryMarkedUser.objects.get(gallery_marked=gallery_marked, user_id=user_id)
    solicitation.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def check_mark_gallery(request, gallery_id, user_id):
    is_authenticated = request.user.is_authenticated

    if is_authenticated:
        is_admin = request.user.is_staff # Verifica se o usuário é admin
        is_media_manager = UserRoles.objects.filter(user_id=request.user, role_id=Roles.objects.get(role='MediaManager')).exists()
    else:
        is_admin = False
        is_media_manager = False

    if not is_authenticated:
        return redirect('users:login')

    if not (is_media_manager or is_admin):
        return redirect('gallery:gallery')

    gallery = Gallery.objects.get(id=gallery_id)
    gallery_marked = GalleryMarked.objects.get(gallery=gallery)
    marked_user = GalleryMarkedUser.objects.get(
        gallery_marked=gallery_marked,
        user_id=user_id
        )

    if marked_user.marked_confirm:
        marked_user.marked_confirm = False
    else:
        marked_user.marked_confirm = True

    marked_user.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
