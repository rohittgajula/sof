from django.shortcuts import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .serializers import UserSerializer, CreateUpdateSerializer
from .models import User
from .pagination import CustomPagination

from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response({
        'status':200,
        'user':serializer.data
    }, status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_users(request):
    users = User.objects.all().order_by('created_at')
    serializer = UserSerializer(users, many=True)
    data = serializer.data

    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response({
        'status':status.HTTP_200_OK,
        'message':'All users.',
        'users':result_page
    })

@swagger_auto_schema(method='POST', request_body=CreateUpdateSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    data = request.data
    serializer = CreateUpdateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status':201,
            'data':serializer.data
        }, status.HTTP_201_CREATED)
    else:
        return Response({
            'status':400,
            'error':serializer.errors
        }, status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='PATCH', request_body=CreateUpdateSerializer)
@api_view(['PATCH'])
def update_user(request, pk):
    user = get_object_or_404(User, id=pk)

    if request.user != user:
        return Response({
            'status':403,
            'error':'You do not have permission to update this profile.'
        }, status.HTTP_403_FORBIDDEN)

    data = request.data
    serializer = CreateUpdateSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status':200,
            'data':serializer.data
        }, status.HTTP_200_OK)
    else:
        return Response({
            'status':400,
            'error':serializer.errors
        }, status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_user(request, pk):
    user = get_object_or_404(User, id=pk)
    print(user, request.user)

    if request.user != user:
        return Response({
            'status':403,
            'error':'You do not have permission to delete this profile.'
        }, status.HTTP_403_FORBIDDEN)
    
    user.delete()
    return Response({
        'status':200,
        'data':f'{user.email} deleted successfully.'
    }, status.HTTP_200_OK)

