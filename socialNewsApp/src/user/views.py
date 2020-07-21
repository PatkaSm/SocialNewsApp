from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
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


def profile(request,pk):
    user_data = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {'user': user_data})
