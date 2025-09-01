from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from .models import User, Igreja, Campus, Papel
from .serializers import LoginSerializer, UserSerializer, IgrejaSerializer, CampusSerializer, PapelSerializer
from .permissions import IsTenantUser


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        login(request, user)
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({'message': 'Logout realizado com sucesso'})
    except Exception:
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class IgrejaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IgrejaSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Igreja.objects.filter(id=self.request.user.igreja.id)


class CampusViewSet(viewsets.ModelViewSet):
    serializer_class = CampusSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Campus.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return User.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)


class PapelViewSet(viewsets.ModelViewSet):
    serializer_class = PapelSerializer
    permission_classes = [IsTenantUser]

    def get_queryset(self):
        return Papel.objects.filter(igreja=self.request.user.igreja)

    def perform_create(self, serializer):
        serializer.save(igreja=self.request.user.igreja)
