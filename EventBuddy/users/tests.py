#da importare tutto 
import json
#from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase #classe del framework per fare i test
from rest_framework import status
from users.models import Profile, CustomUser
from events.models import Event,Review
from events.api.serializer import EventSerializer,ReviewSerializer
from users.api.serializers import UserDisplaySerializer, ProfileDisplaySerializer,ProfileAvatarSerializer
from datetime import datetime
#from django.utils import timezone


#test endpoint registration, new user
class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app",
                "password1": "change_me_123", "password2": "change_me_123"}
        response = self.client.post("/api/rest-auth/registration/", data)
        #verify if the status code is 201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileViewSetTestCase(APITestCase):

    def setUp(self):  #ovvero setUp popolazione DB con istanze per poi usarlo per i test
        self.user = CustomUser.objects.create_user(username="Alighieri",
                                             password="una_password_non_decifrabile")
        self.token = Token.objects.create(user=self.user) #genero Token
        self.api_authentication()       

    def api_authentication(self):                   
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)     # creo il metodo autentificaz

#i test veri e propri di questa classe

    list_url = reverse("current-user") # fornito automaticamente da Router o da noi se abbiamo settato il basename (in urls)
    def test_profile_list_un_authenticated(self):           
        self.client.force_authenticate(user=None)  #richeista non autenticata
        response = self.client.get(self.list_url)   #chiediamo un get verso list_url
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) #ci aspettiamo non sia autorizzato

    def test_profile_list_authenticated(self): #da utenti autenticati(quelli nel DB)
        response = self.client.get(self.list_url) #stesso endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)   #OK

#test retrieve dei dati di una singola istanza di profilo (su db creato)
    def test_profile_detail_retrieve(self):
        response = self.client.get(reverse("profile-details", kwargs={"user_id__username": "Alighieri"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], "Alighieri") 

    def test_profile_update_by_owner(self):
        response = self.client.put(reverse("profile-details", kwargs={"user_id__username": "Alighieri"}), #PUT
                                   {"location": "Anchiano", "bio": "Genio tra i Geni"})
        self.assertEqual(response.status_code, status.HTTP_200_OK) #se put è ok
        self.assertEqual(json.loads(response.content),   #controlliamo che il response sia corretto
                         {"id": 1, "user": "Alighieri", "bio": "Genio tra i Geni",
                          "location": "Anchiano", "avatar": None,"birth_date":None})

    def test_profile_update_by_random_user(self):   
        random_user = CustomUser.objects.create(username="random", #generiamo user random 
                                          password="psw123123")
        self.client.force_authenticate(user=random_user) #forziamo autentificazione con random user
        response = self.client.put(reverse("profile-details", kwargs={"user_id__username": "Alighieri"}), #PUT
                                   {"bio": "Hacked!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) #ci aspettiamo che non vada



#classe test per la EventList e  UserEventList con relative modifiche, importiamo Event,Review e Profilestatusserializer

class EventViewSetTestCase(APITestCase):
    url = reverse("event-list") #url
#set db
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="Alighieri",
                                             password="una_password_non_decifrabile")

        d = datetime(2015, 10, 11, 23, 55, 59, 342380)
        self.event = Event.objects.create(author=self.user, #generiamo un evento
                                                   title="Evento divertente",description="ci si diverte",
                                                   start_date=d,location="Roma",
                                                   picture=None)

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

#test endpoint listaeventi sia autenticati che non autenticati
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_events_list_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#creazione nuovo evento
    def test_event_create_authenticated(self):
        self.api_authentication()
        data = {"title": "un nuovo evento!","description":"ci si divertiva",
        "start_date": "2001-01-02T12:02:00Z","location":"Milano"}
                    
        response = self.client.post(self.url, data)     #post tramite client 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #creato lo stato 
        self.assertEqual(response.data["author"], "Alighieri")  #verifichiamo autore se inserito corretto
        self.assertEqual(response.data["title"], "un nuovo evento!")
        self.assertEqual(response.data["description"], "ci si divertiva")
        self.assertEqual(response.data["start_date"], "2001-01-02T12:02:00Z")

    def test_event_create_un_authenticated(self):
        self.client.force_authenticate(user=None)        
        data = {"title": "un nuovo evento!","description":"ci si divertiva",
        "start_date": "2001-01-02T12:02:00Z","location":"Milano"}
        response = self.client.post(self.url, data)     #post tramite client 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) #creato lo stato 

    def test_single_event_retrieve(self):
        serializer_data = EventSerializer(instance=self.event).data#prendo i dati del nostro event salvato su DB
        #chiamata test tipo get (url diverso da quello globale)
        response = self.client.get(reverse("event-detail", kwargs={"slug": serializer_data['slug']})) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)    #carico in json i dati presi con GET 
        self.assertEqual(serializer_data, response_data) #comparo la serializzazione con il json

#endpoint aggiornamenti status con user che ha creato status, sia con casuale
    def test_event_update_owner(self):
        serializer_data = EventSerializer(instance=self.event).data
        data = {"title": "titolo aggiornato","description":"ci si divertiva",
        "start_date": "2001-01-02T12:02:00Z","location":"Milano"}
        response = self.client.put(reverse("event-detail", kwargs={"slug": serializer_data['slug']}),
                                           data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "titolo aggiornato")

    def test_event_update_random_user(self):
        serializer_data = EventSerializer(instance=self.event).data
        random_user = CustomUser.objects.create(username="random_user",
                                          password="psw123123")
        self.client.force_authenticate(user=random_user)
        data = {"title": "sei stato hackerato!"}
        response = self.client.put(reverse("event-detail", kwargs={"slug": serializer_data['slug']}),
                                           data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




class ReviewViewSetTestCase(APITestCase):
#set db
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="Alighieri",
                                             password="una_password_non_decifrabile")

        d = datetime(2025, 10, 11, 23, 55, 59, 342380)
        self.event = Event.objects.create(author=self.user, #generiamo un evento NON SCADUTO
                                                   title="Evento divertente",description="ci si diverte",
                                                   start_date=d,location="Roma",expired_event=False,
                                                   picture=None)

        d = datetime(2015, 10, 11, 23, 55, 59, 342380)
        self.event_expired = Event.objects.create(author=self.user, #generiamo un evento SCADUTO
                                                   title="Evento passato",description="ci si diverte",
                                                   start_date=d,location="Roma",expired_event=True,
                                                   picture=None)

        self.review = Review.objects.create(author=self.user,event=self.event_expired, #generiamo una review 
                                           rating=5,body="Mi sono divertito")          #collegata a ev SCADUTO
                                                   
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()


#test endpoint lista-recensioni sia autenticati che non autenticati
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_events_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        serializer_data = ReviewSerializer(instance=self.review).data
        response = self.client.get(reverse("event-review-list", kwargs={"slug": serializer_data['event_slug']}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_events_list_authenticated(self):
        serializer_data = ReviewSerializer(instance=self.review).data
        response = self.client.get(reverse("event-review-list", kwargs={"slug": serializer_data['event_slug']}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


#creazione nuovo evento autenticato(user ha già reensito)/non autenticato/random (user non ha recensito)

    def test_review_create_un_authenticated(self):
        self.client.force_authenticate(user=None)        
        data = {"body":"una nuova recensione","rating":"4"}
        serializer_data = ReviewSerializer(instance=self.review).data
        response = self.client.post(reverse("create-review", kwargs={"slug": serializer_data['event_slug']}),
                                    data=data)     #post tramite client 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) #non autorizzato

    def test_review_create_authenticated_ev_expired(self):
        self.api_authentication()
        data = {"body": "una nuova recensione","rating":"4"}          
        serializer_data = ReviewSerializer(instance=self.review).data
        response = self.client.post(reverse("create-review", kwargs={"slug": serializer_data['event_slug']}),
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) #Review già fatta da user-auth
    
    def test_review_create_random_user_ev_not_expired(self):
        random_user = CustomUser.objects.create(username="random_user",
                                          password="psw123123")
        self.client.force_authenticate(user=random_user)       
        data = {"body":"una nuova recensione","rating":"4"}
        serializer_data = EventSerializer(instance=self.event).data  #uso evento non scaduto
        response = self.client.post(reverse("create-review", kwargs={"slug": serializer_data['slug']}),
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) #evento non scaduto BAD REQUEST

   
    def test_review_create_random_user_ev_expired(self):
        random_user = CustomUser.objects.create(username="random_user",
                                          password="psw123123")
        self.client.force_authenticate(user=random_user)       
        data = {"body":"una nuova recensione","rating":4}
        serializer_data = ReviewSerializer(instance=self.review).data
        response = self.client.post(reverse("create-review", kwargs={"slug": serializer_data['event_slug']}),
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #creato lo stato 
        self.assertEqual(response.data["body"], "una nuova recensione")  #verifichiamo autore se inserito corretto
        self.assertEqual(response.data["rating"], 4)

'''
    def test_single_review_retrieve(self):
        serializer_data = ReviewSerializer(instance=self.review).data#prendo i dati della nostra review salvato su DB
        #chiamata test tipo get (url diverso da quello globale)
        response = self.client.get(reverse("review-detail", kwargs={"slug": serializer_data['slug']})) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)    #carico in json i dati presi con GET 
        self.assertEqual(serializer_data, response_data) #comparo la serializzazione con il json

#endpoint aggiornamenti status con user che ha creato status, sia con casuale
    def test_review_update_owner(self):
        serializer_data = EventSerializer(instance=self.event).data
        data = {"title": "titolo aggiornato","description":"ci si divertiva",
        "start_date": "2001-01-02T12:02:00Z","location":"Milano"}
        response = self.client.put(reverse("event-detail", kwargs={"slug": serializer_data['slug']}),
                                           data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "titolo aggiornato")

    def test_review_update_random_user(self):
        serializer_data = EventSerializer(instance=self.event).data
        random_user = CustomUser.objects.create(username="random_user",
                                          password="psw123123")
        self.client.force_authenticate(user=random_user)
        data = {"title": "sei stato hackerato!"}
        response = self.client.put(reverse("event-detail", kwargs={"slug": serializer_data['slug']}),
                                           data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



'''
#in fine test per la  ReviewList e UserEventReview view

#una volta settati i test, possiamo modificare le funzioni della webapp aspettandoci cmq lo stesso risultato
