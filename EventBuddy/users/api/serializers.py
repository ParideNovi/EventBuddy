from rest_framework import serializers
from users.models import CustomUser,Profile

#serializer per endpoint per ottenere solo lo user
class UserDisplaySerializer(serializers.ModelSerializer):   
    #e_author = serializers.StringRelatedField(read_only=True) #every author shows the review of his event
    class Meta:
        model = CustomUser
        fields = ["username"]


#serializer per endpoint per ottenere solo lo user
class ProfileDisplaySerializer(serializers.ModelSerializer):   
    user = serializers.StringRelatedField()
    avatar = serializers.ImageField(read_only=True) #creeremo un serializer specifico per l'aggiornamento del nostro avatar 

    class Meta:
        model = Profile
        fields = "__all__"


class ProfileAvatarSerializer(serializers.ModelSerializer): #Modelserializer specifico Avatar tramite singolo endpoit di tipo formdata (non Json)! 
 # in questo caso senza model apposito meglio usare delle generic APIview con i ViewSets
    class Meta:                           
        model = Profile
        fields = ["avatar"]   #permette di modificare solo gli avatar #vedi views.url