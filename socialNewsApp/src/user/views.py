from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DetailView, CreateView
from user.forms import UserRegisterForm
from user.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f' {username} Twoje konto zostało założone! Możesz się teraz zalogować')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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
        context = {
            'user_posts': user_posts,
            'user_comments': user_comments,
            'user_micro_posts_reactions': user_micro_posts_reactions,
            'user_micro_posts': user_micro_posts,
            'user_post_reactions': user_posts_reactions,
            'user_reactions': user_posts + user_posts_reactions + user_micro_posts_reactions + user_comments + user_micro_posts
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


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_update.html'
    success_url = reverse_lazy('profile:password_change_done')

    def form_valid(self, form):
        messages.success(self.request, "Pomyślnie zmieniono hasło!")
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ChangePasswordDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'users/password_update_success.html'



