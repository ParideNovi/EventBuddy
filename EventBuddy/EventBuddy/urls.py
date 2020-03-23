from django.contrib import admin
from django.urls import path, include, re_path #re_path crea path url con espressioni regolari per la deviazione verso la indexView

from django_registration.backends.one_step.views import RegistrationView #one_step per login senza doppia autentificazione da broswer
from core.views import IndexTemplateView
from users.forms import CustomUserForm
from django.conf.urls.static import static
from django.conf import settings
#docum django registration piu passaggi
# https://django-registration.readthedocs.io/en/3.0/
# https://django-registration.readthedocs.io/en/3.0/custom-user.html
# https://django-registration.readthedocs.io/en/3.0/one-step-workflow.html

urlpatterns = [
    path('admin/', admin.site.urls),  #url administrazione
    #url registration tramite interfaccia client standard usando RegistrationView personalizzata con CustomUser
    path('accounts/register/',
        RegistrationView.as_view(form_class=CustomUserForm,
                                success_url="/"),
                                name="django_registration_register"),  
    path('accounts/',
        include("django_registration.backends.one_step.urls")),   # altri url del package django_registration
    path('accounts/',
        include("django.contrib.auth.urls")),   # url login tramite interfaccia standard
    path('api/',
        include("users.api.urls")),         # url api users app    
    path('api/',
        include("events.api.urls")),         # url api events app             
    path('api-auth/',
        include("rest_framework.urls")),   # url login tramite browsable api rest_framework     
    path('api/rest-auth/',                  
        include("rest_auth.urls")),        # url login tramite rest_auth
    path('api/rest-auth/registration/',    # endpoint api registration tramite rest_auth
        include("rest_auth.registration.urls")),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
       
urlpatterns.append(re_path(r"^.*$",IndexTemplateView.as_view(),name="entry-point") )             # every other request (if logged-in) will be mabage by vue router ]

#media in debug mode
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #debug media



