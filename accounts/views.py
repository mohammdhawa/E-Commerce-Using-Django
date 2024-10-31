from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .forms import SignupForm, UserActivationForm
from .models import Profile
from django.contrib.auth.models import User


def signup(request):
    # Create new user
    # send email: code
    # redirect: activate
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = form.save(commit=False) # Trigger signal --> create profile: code
            user.is_active = False
            user.save()

            profile = Profile.objects.get(user__username=username)

            # Send email
            send_mail(
                "Account Activation",
                f"Welcome {username} \nUse this code {profile.code} to activate your account.",
                "ismekbektop@gmail.com",
                [email],
                fail_silently=False,
            )

            return redirect('account-activate', username=username)

    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})


def user_activate(request, username):
    # code: activate
    # redirect: login
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = UserActivationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if profile.code == code:
                profile.code = ''
                profile.save()
                user.is_active = True
                user.save()

                return redirect('accounts/login')
    else:
        form = UserActivationForm()


    return render(request, 'accounts/activate.html', {'form': form})