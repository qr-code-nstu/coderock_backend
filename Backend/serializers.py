from rest_framework.serializers import *
from .models import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class UserSignInSerializer(ModelSerializer):
    password2 = CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

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
    class Meta:
        model = User
        fields = ('username', 'password')


class ExecutorSignInSerializer(ModelSerializer):
    class Meta:
        model = Executor
        fields = '__all__'


class ClientSignInSerializer(ModelSerializer):
    class Meta:
        model = Executor
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
