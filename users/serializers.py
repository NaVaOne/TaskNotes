from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import CustomUser

# Сериализатор для регистрации (Djoser)
class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'email', 
            'username', 
            'password', 
            'timezone', 
            'receive_notifications'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

# Сериализатор для логина (JWT)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Меняем поле для аутентификации с username на email
        attrs['username'] = attrs.get('email', '')  # Для совместимости
        data = super().validate(attrs)
        
        # Добавляем кастомные поля в ответ
        data.update({
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'timezone': self.user.timezone,
            'receive_notifications': self.user.receive_notifications
        })
        return data

# Сериализатор для профиля (Djoser)
class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'timezone',
            'receive_notifications'
        )
        read_only_fields = ('email',)  
# from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.password_validation import validate_password
# from .models import CustomUser

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password],
#         style={'input_type': 'password'}
#     )
#     password2 = serializers.CharField(
#         write_only=True,
#         required=True,
#         style={'input_type': 'password'}
#     )

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password', 'password2', 'timezone', 'receive_notifications')
#         extra_kwargs = {
#             'email': {'required': True}
#         }

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Пароли не совпадают"})
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop('password2')
#         return CustomUser.objects.create_user(**validated_data)

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         data.update({
#             'username': self.user.username,
#             'email': self.user.email,
#             'timezone': self.user.timezone
#         })
#         return data

# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'timezone', 'receive_notifications')
#         read_only_fields = ('username',)

#     def validate_email(self, value):
#         if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
#             raise serializers.ValidationError("Этот email уже используется")
#         return value