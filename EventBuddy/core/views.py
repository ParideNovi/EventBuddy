from django.contrib.auth.mixins import LoginRequiredMixin #per accesso ai soli User aut
from django.views.generic.base import TemplateView #per reindirizzare dei template
from django.conf import settings
#view per il richiamo del template(html) dell'homepage della SPA
class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):       #per il template da reidirizzare
        if settings.DEBUG:
            template_name = "index.html"
        else:
            template_name = "index-dev.html" 
        return template_name
