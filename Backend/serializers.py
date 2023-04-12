from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.serializers import *
from .models import *
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserSignInSerializer(ModelSerializer):
    password2 = CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({"password": "Password fields didn't match."})

        return attrs

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user


class UserLogInSerializer(ModelSerializer):
    username = CharField(max_length=255)
    password = CharField(max_length=255, write_only=True)
    token = CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(
                'Если пользовательне нашел username и password'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise ValidationError(
                'Пользователь отправляет почту и пароль . Он не должен быть пустым'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }

    class Meta:
        model = User
        fields = ('username', 'password', 'token')


class ExecutorSignInSerializer(ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class ClientSignInSerializer(ModelSerializer):


    # Apply custom validation either here, or in the view.
    class Meta:
        model = Client
        fields = '__all__'


class ExecutorSerializer(ModelSerializer):
    id = UserSerializer()

    class Meta:
        model = Executor
        fields = ('id', 'first_name', 'second_name', 'last_name',
                  'image', 'phone', 'about')


class ClientSerializer(ModelSerializer):
    id = UserSerializer()

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'second_name', 'last_name',
                  'image', 'phone', 'about')


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        field = '__all__'


class LoginSerializer(ModelSerializer):
    username = CharField(
        label="Username",
        write_only=True
    )
    password = CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: wrong username or password.'
                raise ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

    class Meta:
        model = Client
        fields = ('username', 'password')
