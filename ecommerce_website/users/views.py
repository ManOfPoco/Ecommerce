from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.messages.views import SuccessMessageMixin
from .forms import MyUserCreationForm, EditProfileForm, EditUserForm

from products.models import Product
from cart.models import CartItem

from django.contrib.auth.decorators import login_required


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_products"] = Product.objects.get_popular_products()
        context['cart_items_count'] = CartItem.objects.get_cart_items_count(
            self.request)
        return context


@login_required(login_url='/users/sign-in/')
def edit_profile(request):

    if request.method == 'POST':
        user_form = EditUserForm(
            request.POST,
            instance=request.user)
        profile_form = EditProfileForm(
            request.POST,
            instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()

            return redirect(reverse('users:edit-profile'))
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(
            instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'breadcrumb': {
            'My Account': 'users:profile',
            'Edit Profile': None
        },
        'cart_items_count': CartItem.objects.get_cart_items_count(request)
    }
    return render(request, 'users/user-edit-template.html', context)


class SignUpView(SuccessMessageMixin, FormView):
    template_name = 'registration/sign-up.html'
    form_class = MyUserCreationForm
    success_url = 'sign-in'
    success_message = "Account was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cart_items_count'] = CartItem.objects.get_cart_items_count(
            self.request)
        return context

    def form_valid(self, form: MyUserCreationForm):
        form.save()
        return super().form_valid(form)