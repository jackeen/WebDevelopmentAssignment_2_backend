from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from WebDevelopmentAssignment_2_backend import settings


# Create your views here.

@api_view(['GET'])
def get_system_info(request):
    return Response(
        data={
            "application": settings.APP_NAME,
            "version": settings.APP_VERSION,
            'status': 'active'
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def logout(request):
    user = request.user
    Token.objects.get(user=user).delete()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_user_id(request):
    user = request.user

    return Response(
        data={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'group': user.groups.first(),
        },
        status=status.HTTP_200_OK
    )
