from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser
from users.models import Profile

class CustomUserAdmin(UserAdmin):
    #add_form = "bio" #classe di form da noi definita per la creazione
    # form =    per update
    model = CustomUser
    #the custom fields are presents, but i can't show it in the Admin Django page, because 
    #i can't override CustomUser.add_fieldsets  --> try to use admin.site.register(CustomUser)
    
    #CustomUser.add_fieldsets = (
    #    (('Personal info'), {
    #        'classes': ('wide',),
    #        'fields': ('username', 'password1', 'password2','bio','location'),
    #    }),
    #)
    list_display = ["username","email","is_staff"] #show it #"location"

#admin.site.register(CustomUser) or manage fields by API or register a new CustomUser
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)


