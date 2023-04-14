from django.shortcuts import render

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.contrib.auth.models import User

from django.contrib.messages.views import SuccessMessageMixin
from .forms import MyUserCreationForm


class AccountView(DetailView):
    models = User
    template_name = 'users/account.html'

    def get_queryset(self):
        return super().get_queryset()


class SignUpView(SuccessMessageMixin, FormView):
    template_name = 'registration/sign-up.html'
    form_class = MyUserCreationForm
    success_url = 'sign-in'
    success_message = "Account was created successfully"

    def form_valid(self, form: MyUserCreationForm):
        form.save()
        return super().form_valid(form)
