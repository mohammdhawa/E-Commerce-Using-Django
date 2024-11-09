from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.defaultfilters import default
from django.views.generic import DetailView

from orders.models import CartDetail
from .forms import SignupForm, UserActivationForm
from .models import Profile
from django.contrib.auth.models import User
from accounts.models import Address, Phone
from django.http import JsonResponse
from django.db import IntegrityError


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
            if profile.code == code.strip():
                profile.code = ''
                profile.save()
                user.is_active = True
                user.save()

                return redirect('accounts/login')
    else:
        form = UserActivationForm()


    return render(request, 'accounts/activate.html', {'form': form})


class ProfileView(DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Get the profile of the currently logged-in user
        profile = Profile.objects.get(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        addresses = Address.objects.filter(user=self.request.user).order_by('-default')
        contact_numbers = Phone.objects.filter(user=self.request.user).order_by('type')
        context['addresses'] = addresses
        context['address_count'] = addresses.count()
        context['contact_numbers'] = contact_numbers
        context['contact_numbers_count'] = contact_numbers.count()
        return context


def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        # Use request.FILES to get the uploaded image file
        if 'image' in request.FILES:
            profile.image = request.FILES['image']

        name = request.POST.get('name')
        if name:
            mylist = name.split()
            user.first_name = ' '.join(mylist[:-1])
            user.last_name = mylist[-1]

        email = request.POST.get('email')
        if email:
            user.email = email

        profile.save()
        user.save()
        return redirect('profile')

    return redirect('profile')


def add_address(request):
    addresses = Address.objects.filter(user=request.user)
    count = addresses.count()

    if count < 3:
        if request.method == 'POST':
            type = request.POST.get('type')
            address = request.POST.get('address')
            default = request.POST.get('default')

            if default:
                default = True
            else:
                default = False

            if default:
                for address in addresses:
                    address.default = False
                    address.save()
            elif not default:
                default = True
            elif addresses and not any(obj.default for obj in addresses):
                addresses[0].default = True
                addresses[0].save()

            Address.objects.create(user=request.user, type=type, address=address, default=default)
    return redirect('profile')


def edit_address(request):
    if request.method == 'POST':
        flag = False
        address_id = int(request.POST.get('address_id', 0))
        address_type = request.POST.get('type')
        address_text = request.POST.get('address')
        default = request.POST.get('default') == 'on'  # Check if 'default' is checked

        # Get the address object
        my_address = Address.objects.get(id=address_id)

        # Print debug statement
        print("\n--------------------------------- Default --------------------------")

        # Update fields
        if default:
            my_address.default = True
            flag = True
        my_address.type = address_type
        my_address.address = address_text
        my_address.save()

        # Reset default status for other addresses if necessary
        if flag:
            user_addresses = Address.objects.filter(user=request.user).exclude(id=my_address.id)
            for user_address in user_addresses:
                user_address.default = False
                user_address.save()  # Save changes

        return redirect('profile')
    return redirect('profile')


def delete_address(request, pk):
    addresses = Address.objects.filter(user=request.user).exclude(id=pk)
    address = Address.objects.get(id=pk)
    address.delete()

    if addresses and not any(obj.default for obj in addresses):
        addresses[0].default = True
        addresses[0].save()


    return redirect('profile')


def add_contact_number(request):
    numbers = Phone.objects.filter(user=request.user)
    numbers_count = numbers.count()

    if numbers_count < 3:
        if request.method == 'POST':
            new_type = request.POST.get('type')
            new_number = request.POST.get('number')

            if new_type == 'Primary':
                for number in numbers:
                    number.type = 'Secondary'
                    number.save()
            elif not numbers:
                new_type = 'Primary'
            elif numbers and not any(obj.type == 'Primary' for obj in numbers):
                numbers[0].type = 'Primary'
                numbers[0].save()

            Phone.objects.create(user=request.user, type=new_type, number=new_number)

    return redirect('profile')


def delete_contact_number(request, pk):
    numbers = Phone.objects.filter(user=request.user).exclude(id=pk)
    number = Phone.objects.get(id=pk)
    number.delete()

    if numbers and not any(obj.type == 'Primary' for obj in numbers):
        numbers[0].type = 'Primary'
        numbers[0].save()

    return redirect('profile')
