from users.models import CustomUser #modello User
from django.db.models.signals import post_save #segnale inviato ogni volta che l'istanza viene salvata
from django.dispatch import receiver #decoratore utilizzato per ricevere il segnale post_save e per associare un Profilo tramite la funzione def..
from users.models import Profile
#file per la creazione automatica di un profilo, ogni qualvolta viene aggiunto (registrato) un User
@receiver(post_save, sender=CustomUser) #signal da User
def create_profile(sender, instance, created, **kwargs): #il flag created == True ci segnala istanza appena creata
    # print("Created: ", created)
    if created:
        Profile.objects.create(user=instance)


#to use created go to file init.py