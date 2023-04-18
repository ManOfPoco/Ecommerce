from django import forms

from .models import WishList, WishListItem


class WishlistForm(forms.ModelForm):

    class Meta:
        model = WishList
        fields = ['list_name', 'is_default']
        labels = {
            'is_default': 'Make default'
        }


class WishListItemAddForm(forms.ModelForm):

    class Meta:
        model = WishListItem
        fields = ['wishlist']
        labels = {
            'wishlist': 'Select A List'
        }
