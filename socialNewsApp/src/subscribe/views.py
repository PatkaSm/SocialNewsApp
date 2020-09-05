from blog.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from mikroblog.models import MicroPost
from subscribe.models import Subscribe
from tag.models import Tag
from user.models import User


@login_required
def user_subscribe(request, pk):
    user = get_object_or_404(User, pk=pk)
    type = Subscribe.Type.SUB
    sub, created = Subscribe.objects.get_or_create(owner=request.user, user=user, type=type)
    block = Subscribe.objects.filter(owner=request.user, user=user, type=Subscribe.Type.BLOCK).first()
    if not created: #user jest obserwowany wiec go odobserwujemy
        sub.delete()
        messages.warning(request, f'Odobserwowałeś użytkownika {user.username}!')
    elif created and block:  # user nie jest zasubowany więc go obserwujemy i usuwamy banicje
        sub.save()
        block.delete()
        messages.success(request,
                         f'Obserwujesz użytkownika {user.username}! Teraz jego posty będą widoczne w zakładce X')
    else:
        sub.save()
        messages.success(request,
                         f'Obserwujesz użytkownika {user.username}! Teraz jego posty będą widoczne w zakładce X')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def user_block(request, pk):
    user = get_object_or_404(User, pk=pk)
    type = Subscribe.Type.BLOCK
    block, created = Subscribe.objects.get_or_create(owner=request.user, user=user, type=type)
    sub = Subscribe.objects.filter(owner=request.user, user=user, type=Subscribe.Type.SUB).first()
    if not created: #user jest zbanowany wiec go odbanowujemy
        block.delete()
        messages.success(request,
                         f'Usunąłeś użytkownika {user.username} z czarnej listy! Od teraz jego posty'
                         f'będą dla ciebie widoczne.')
    elif created and sub:  # user nie jest zbanowany więc go banujemy i usuwamy obserwacje
        block.save()
        sub.delete()
        messages.warning(request, f'Dodałeś użytkownika {user.username} do czarnej listy! Od teraz jego posty'
                         f' nie będą dla ciebie widoczne.')
    else:
        block.save()
        messages.warning(request,
                         f'Dodałeś użytkownika {user.username} do czarnej listy! Od teraz jego posty'
                         f' nie będą dla ciebie widoczne.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def tag_subscribe(request, slug):
    tag = get_object_or_404(Tag, word=slug)
    sub, created = Subscribe.objects.get_or_create(owner=request.user, tag=tag, type=Subscribe.Type.SUB)
    block = Subscribe.objects.filter(owner=request.user, tag=tag, type=Subscribe.Type.BLOCK).first()
    if not created:  # tag jest zasubowany więc go odsubowujemy
        sub.delete()
        messages.warning(request, f'Odobserwowałeś tag {tag.word}!')
    elif created and block:  # tag nie jest zasubowany więc go subujemy i usuwamy banicje
        sub.save()
        block.delete()
        messages.success(request, f'Obserwujesz tag {tag.word}! Teraz posty o tej tematyce będą widoczne w zakładce X')
    else:
        sub.save()
        messages.success(request, f'Obserwujesz tag {tag.word}! Teraz posty o tej tematyce będą widoczne w zakładce X')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def tag_block(request, slug):
    tag = get_object_or_404(Tag, word=slug)
    block, created = Subscribe.objects.get_or_create(owner=request.user, tag=tag, type=Subscribe.Type.BLOCK)
    sub = Subscribe.objects.filter(owner=request.user, tag=tag, type=Subscribe.Type.SUB).first()
    if not created:  # tag jest zbanowany więc go odbanowujemy
        block.delete()
        messages.success(request,
                         f'Usunąłeś tag {tag.word} z czarnej listy! Teraz posty o tej tematyce będą '
                         f'dla ciebie widoczne.')
    elif created and sub: # tag nie jest zbanowany więc go banujemy i usuwamy obserwacje
        block.save()
        sub.delete()
        messages.warning(request,
                         f'Dodałeś tag {tag.word} do czarnej listy! Teraz posty o tej tematyce '
                         f'nie będą dla ciebie widoczne!')
    else:  # tag nie jest zbanowany więc go banujemy i usuwamy obserwacje:
        block.save()
        messages.warning(request,
                         f'Dodałeś tag {tag.word} do czarnej listy! Teraz posty o tej tematyce '
                         f'nie będą dla ciebie widoczne!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def fav_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    type = Subscribe.Type.SUB
    fav, created = Subscribe.objects.get_or_create(owner=request.user, post=post, type=type)
    if not created:
        fav.delete()
        messages.warning(request,
                         f'Usunąłeś post z ulubionych!.')
    else:
        fav.save()
        messages.success(request, f'Dodałeś post do ulubionych! Możesz go teraz znaleźć w zakładce "ulubione".')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def fav_micro_post(request, pk):
    micro_post = get_object_or_404(MicroPost, pk=pk)
    type = Subscribe.Type.SUB
    fav, created = Subscribe.objects.get_or_create(owner=request.user, micro_post=micro_post, type=type)
    if not created:
        fav.delete()
        messages.warning(request,
                         f'Usuąłeś wpis z ulubionych!')
    else:
        fav.save()
        messages.success(request, f'Dodałeś wpis z ulubionych! Możesz go teraz znaleźć w zakładce "ulubione".')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
