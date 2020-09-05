from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DetailView, CreateView
from subscribe.models import Subscribe
from user.forms import UserRegisterForm
from user.models import User


class CreateUser(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        messages.success(self.request, f' {username} Twoje konto zostało założone! Możesz się teraz zalogować')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class UserDetailsView(DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        user_data = kwargs['object']
        user_posts = user_data.posts.all().count()
        user_comments = user_data.comments.all().count()
        user_micro_posts_reactions = user_data.reactions.filter(post=None).count()
        user_posts_reactions = user_data.reactions.filter(micro_post=None).count()
        user_micro_posts = user_data.micro_posts.all().count()
        is_subscribed = user_data.subscriptions.filter(type=Subscribe.Type.SUB)
        is_blocked = user_data.subscriptions.filter(type=Subscribe.Type.BLOCK)
        context = {
            'user': user_data,
            'user_posts': user_posts,
            'user_comments': user_comments,
            'user_micro_posts_reactions': user_micro_posts_reactions,
            'user_micro_posts': user_micro_posts,
            'user_post_reactions': user_posts_reactions,
            'user_reactions': user_posts + user_posts_reactions + user_micro_posts_reactions + user_comments +
                              user_micro_posts,
            'is_subscribed': is_subscribed,
            'is_blocked': is_blocked
        }
        return context


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'bio', 'location', 'birth_date', 'gender', 'facebook', 'twitter', 'ig',
              'public_email', 'user_page']
    template_name = 'users/user_update_form.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zapisano profil!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class AvatarUpdate(UpdateView):
    model = User
    fields = ['avatar']
    template_name = 'users/avatar_update.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zmieniono avatar!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class BackgroundUpdate(UpdateView):
    model = User
    fields = ['background']
    template_name = 'users/background_update.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zmieniono zdjęcie w tle!")
        super().form_valid(form)
        print(form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())


class EmailUpdate(UpdateView):
    model = User
    fields = ['email']
    template_name = 'users/email_update.html'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zmieniono email!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ChangePasswordView(PasswordChangeView):
    success_url = reverse_lazy('profile:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zmieniono hasło!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ChangePasswordDoneView(PasswordChangeDoneView):
    template_name = 'users/password_update_success.html'
