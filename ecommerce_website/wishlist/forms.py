from django import forms

from .models import WishList


class WishlistForm(forms.ModelForm):

    class Meta:
        model = WishList
        fields = ['list_name', 'is_default']
        labels = {
            'is_default': 'Make default'
        }
