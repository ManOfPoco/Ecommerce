from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from cart.mixins import CartItemsCountMixin

from django.contrib.messages.views import SuccessMessageMixin
from .forms import MyUserCreationForm, EditProfileForm, EditUserForm, UserLoginForm
from wishlist.forms import WishListItemAddForm

from products.models import Product, ProductImages
from cart.models import CartItem
from orders.models import Order

from django.db.models import Count, Prefetch


from django.contrib.auth.decorators import login_required


class ProfileView(LoginRequiredMixin, CartItemsCountMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_products"] = Product.objects.get_popular_products()
        context['wishlist_item_add_form'] = WishListItemAddForm(
            self.request.user)
        return context


@login_required
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


class SignUpView(CartItemsCountMixin, SuccessMessageMixin, FormView):
    template_name = 'registration/sign-up.html'
    form_class = MyUserCreationForm
    success_url = '/account/sign-in/'
    success_message = "Account was created successfully"

    def form_valid(self, form: MyUserCreationForm):
        form.save()
        return super().form_valid(form)


class CustomLoginView(CartItemsCountMixin, LoginView):
    template_name = 'registration/sign-in.html'
    authentication_form = UserLoginForm


class OrderListView(CartItemsCountMixin, ListView):
    template_name = 'users/orders.html'
    context_object_name = 'orders'
    model = Order

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(order_products_total=Count(
            'order_item')).select_related('order_status', 'user').order_by('created_at')

        return queryset


class OrderDetailView(CartItemsCountMixin, DetailView):
    template_name = 'users/order-detail.html'
    model = Order
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['products'] = order.order_item.filter(
            order=order).prefetch_related(Prefetch('product__images'))
        context['breadcrumb'] = {
            'Orders': 'users:orders',
            'Order': None
        }

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('order_item')
        return queryset
