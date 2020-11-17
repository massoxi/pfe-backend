from graphene import Mutation, ObjectType, Field, List, String, Boolean, JSONString
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model, authenticate, login, logout
from graphql_api.models import User, Temoin, Medicin

class UserType(DjangoObjectType):
    class Meta:
        model = User

class TemoinType(DjangoObjectType):
    class Meta:
        model = Temoin


class CreateUser(Mutation):
    user = Field(TemoinType)

    class Arguments:
        email = String(required=True)
        password = String(required=True)
        first_name = String()
        last_name = String()

    def mutate(self, info, email, password, **kwargs):
        user = Temoin(username=email)
        user.set_password(password)
        if kwargs:
            for elt in kwargs:
                setattr(user, elt, kwargs[elt])
        user.save()
        return CreateUser(user=user)

class CreatePhysician(Mutation):
    user = Field(UserType)

    class Arguments:
        email = String(required=True)
        password = String(required=True)
        first_name = String()
        last_name = String()

    def mutate(self, info, email, password, **kwargs):
        user = Medicin(username=email)
        user.set_password(password)
        if kwargs:
            for elt in kwargs:
                setattr(user, elt, kwargs[elt])
        user.save()
        return CreateUser(user=user)

class Login(graphql_jwt.JSONWebTokenMutation):
    user = Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        print("Hey there!")
        username = kwargs['username']
        user = User.objects.get(username=username)
        if user:
            login(request=info.context, user=user,
              backend='django.contrib.auth.backends.ModelBackend')
            return cls(user=info.context.user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()


class Query(ObjectType):
    logout = Boolean()

    def resolve_logout(self, info):
        if (info.context.user.is_authenticated):
            logout(request=info.context.user)
            success = True
        else:
            success = False
        return success