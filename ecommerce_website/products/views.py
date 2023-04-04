from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Category


class CategoryView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.get(slug=kwargs.get(
            'slug')).get_children().prefetch_related('children')
        return context

    def get_template_names(self):
        return [f"products/{self.kwargs.get('slug')}.html"]
