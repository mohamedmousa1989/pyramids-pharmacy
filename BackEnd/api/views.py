import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    MedicationSerializer,
    RefillRequestSerializer
)
from api.models import Medication, RefillRequest
from django.db.models import Count, Sum


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'status': 'error',
                'message': 'Both username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'type': 'Bearer',
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class MedicationAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MedicationSerializer

    def get(self, request):
        medications = Medication.objects.all()
        serializer = self.serializer_class(medications, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Medication added successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RefillRequestAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefillRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Refill request added successfully'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):

        statistics = RefillRequest.objects.values(
            'medication__name'
        ).annotate(
            total_refills=Count('id'),
            total_quantity=Sum('quantity')
        ).order_by('medication__name')

        return Response({
            'refill_statistics': list(statistics)
        })

        