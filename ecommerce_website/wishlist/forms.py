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

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wishlist'].queryset = WishList.objects.filter(user=user)

    class Meta:
        model = WishListItem
        fields = ['wishlist']
        labels = {
            'wishlist': 'Select A List'
        }
