from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Igreja, Campus, Papel


class IgrejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Igreja
        fields = ['id', 'nome', 'cnpj', 'endereco', 'telefone', 'email', 'site', 'logo', 'plano']
        read_only_fields = ['id']


class CampusSerializer(serializers.ModelSerializer):
    nivel_display = serializers.CharField(source='get_nivel_display', read_only=True)
    
    class Meta:
        model = Campus
        fields = ['id', 'nome', 'nivel', 'nivel_display', 'campus_pai', 'endereco', 'telefone', 'email']
        read_only_fields = ['id', 'igreja']


class UserSerializer(serializers.ModelSerializer):
    igreja_nome = serializers.CharField(source='igreja.nome', read_only=True)
    campus_nome = serializers.CharField(source='campus.nome', read_only=True)
    nivel_acesso_display = serializers.CharField(source='get_nivel_acesso_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'telefone', 'foto',
            'igreja', 'igreja_nome', 'campus', 'campus_nome', 'nivel_acesso', 'nivel_acesso_display',
            'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('Conta desativada.')
                if not user.igreja.ativa:
                    raise serializers.ValidationError('Igreja inativa.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Credenciais inválidas.')
        else:
            raise serializers.ValidationError('Username e password são obrigatórios.')


class PapelSerializer(serializers.ModelSerializer):
    nivel_minimo_display = serializers.CharField(source='get_nivel_minimo_display', read_only=True)
    
    class Meta:
        model = Papel
        fields = ['id', 'nome', 'descricao', 'nivel_minimo', 'nivel_minimo_display']
        read_only_fields = ['id', 'igreja']
