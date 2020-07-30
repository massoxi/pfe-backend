from graphene import Mutation, ObjectType, Field, List, String, Boolean
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model, authenticate, login, logout



class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(Mutation):
    user = Field(UserType)

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String()
        first_name = String()
        last_name = String()
        is_superuser = Boolean()

    def mutate(self, info, username, password, **kwargs):
        user = get_user_model()(
            username=username,
        )
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
        username = kwargs['username']
        user = get_user_model().objects.get(username=username)
        login(request=info.context, user=user,
              backend='django.contrib.auth.backends.ModelBackend')
        return cls(user=info.context.user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()


class Query(ObjectType):
    users = List(UserType)
    logout = Boolean()

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_logout(self, info):
        if (info.context.user.is_authenticated):
            logout(request=info.context)
            success = True
        else:
            success = False

        return success
