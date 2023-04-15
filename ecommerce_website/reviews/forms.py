from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Review

from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class ReviewForm(forms.ModelForm):
    product_rating = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'create-review-form'
        self.helper.form_class = 'review-form'
        self.helper.form_method = 'POST'

        self.helper.add_input(Submit('submit', 'Submit Review'))

    class Meta:
        model = Review
        fields = ['headline', 'body', 'bottom_line', 'product_rating']
