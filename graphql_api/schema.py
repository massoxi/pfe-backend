import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.db.models import Q
import json

from graphql_api.models import Protocole, Temoin, Message, User, Medicin
from graphql_api.users.schema import Mutation as user_mutation, Query as user_query


class MessageType(DjangoObjectType):
    class Meta:
        model = Message

class SendAlert(graphene.Mutation):
    status = graphene.Boolean()
    errorMessage = graphene.String()

    class Arguments:
        content = graphene.String()

    def mutate(self, info, content):
        errorMessage = ""
        user = info.context.user
        if not user or user.is_anonymous:
            status = False
            errorMessage = "Utilisateur non connecté"
        else:
            status = True
            Message.objects.create(expediteur=user, contenu=content, diffusion=True)
        return SendAlert(status=status, errorMessage=errorMessage)

class SendMessage(graphene.Mutation):
    status = graphene.Boolean()
    errorMessage = graphene.String()

    class Arguments:
        username = graphene.String()
        content = graphene.String()

    def mutate(self, info, username, content):
        errorMessage = ""
        user = info.context.user
        if not user or user.is_anonymous:
            status = False
            errorMessage = "Utilisateur non connecté"
        else:
            status = True
            destinateur = User.objects.get(username=username)
            Message.objects.create(expediteur=user, contenu=content, destinateur=destinateur, diffusion=False)
        return SendMessage(status=status, errorMessage=errorMessage)

class Respiration(graphene.Mutation):
    instructions = graphene.List(graphene.String)
    img = graphene.String()

    class Arguments:
        age = graphene.String()
        trauma = graphene.Boolean()

    def mutate(self, info, age, trauma):
        if(trauma):
            p = Protocole.objects.get(type="respiration", cas_precis="bouche a nez")
        else:
            if(age == 'N'):
                p = Protocole.objects.get(type="respiration", cas_precis="bouche a bouche et nez")
            else:
                p = Protocole.objects.get(type="respiration", cas_precis="bouche a bouche")
        return Respiration(instructions=p.data, img=p.img.path)

class Reanimation(graphene.Mutation):
    instructions = graphene.List(graphene.String)
    img = graphene.String()

    class Arguments:
        age = graphene.String()

    def mutate(self, info, age):
        cas = {"N": "nourrisson",
               "E": "enfant",
               "A": "adulte",
               }
        p = Protocole.objects.get(type="reanimation", cas_precis=cas[age])
        return Reanimation(instructions=p.data, img=p.img.path)

class Pouls(graphene.Mutation):
    instructions = graphene.List(graphene.String)
    img = graphene.String()

    class Arguments:
        age = graphene.String()

    def mutate(self, info, age):
        cas = {"N": "brachiale",
               "E": "carotidien",
               "A": "carotidien",
               }
        p = Protocole.objects.get(type="pouls", cas_precis=cas[age])
        return Reanimation(instructions=p.data, img=p.img.path)

class Query(user_query, graphene.ObjectType):
    protection = graphene.JSONString()
    lva = graphene.JSONString()
    saignement = graphene.JSONString()
    evalRespiration = graphene.JSONString()
    fetchMessages = graphene.List(MessageType)
    fetchMessagesMedecin = graphene.List(MessageType)

    def resolve_protection(self, info):
        data = dict()
        p = Protocole.objects.filter(type='protection', cas_precis='generale')[0]
        data['instructions'] = p.data
        p = Protocole.objects.filter(type='protection', cas_precis='degagement')[0]
        data['degagement'] = {'img': p.img.path, 'instructions': p.data}
        return data

    def resolve_fetchMessages(self, info):
        user = info.context.user
        return Message.objects.filter(destinateur=user)

    def resolve_fetchMessagesMedecin(self, info):
        user = info.context.user
        messages = Message.objects.filter(Q(destinateur=user) | Q(diffusion=True))
        """
        data = dict()
                    for m in messages :
            message = {
                'name' : m.expediteur.first_name + m.expediteur.last_name,
                'username' : m.expediteur.username,
                'contenu' : m.contenu,
                'date' : m.date.strftime("%H:%M:%S | %m/%d/%Y"),
                'avatar' : '',
            }
            if (m.expediteur.avatar):
                message['avatar'] = m.expediteur.avatar.path
            data.append(message)

        """
        return messages #data

    def resolve_lva(self, info):
        data = dict()
        p = Protocole.objects.get(type="liberte des voies aeriennes", cas_precis="subluxation de la mandibule")
        if (p.img.path):
            data["img"] = p.img.path
        data["instructions"] = p.data
        return data

    def resolve_evalRespiration(self):
        data = dict()
        p = Protocole.objects.get(type="respiration", cas_precis="evaluation")
        if (p.img.path):
            data["img"] = p.img.path
        data["instructions"] = p.data
        return data

    def resolve_saignement(self, info):
        data = dict()
        p = Protocole.objects.get(type="saignement", cas_precis="generale")
        if (p.img.path):
            data["img"] = p.img.path
        data["instructions"] = p.data
        return data

class Mutation(user_mutation, graphene.ObjectType):
    send_alert = SendAlert.Field()
    sendMessage = SendMessage.Field()
    respiration = Respiration.Field()
    reanimation = Reanimation.Field()
    poulsation = Pouls.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
