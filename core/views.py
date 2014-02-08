# import django deps
from django.views.generic import TemplateView


# home view
class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context

home_view = HomeView.as_view()
