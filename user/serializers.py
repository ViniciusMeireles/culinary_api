from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import transaction
from rest_framework import serializers

from user.fields import ChefResponsibilityList
from user.models import Chef, ChefResponsibility

USER_MODEL: type(AbstractUser) = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['password'].required = False
        return fields

    def create(self, validated_data):
        return USER_MODEL.objects.create_user(**validated_data)


class ChefSerializer(serializers.ModelSerializer):
    responsibilities = ChefResponsibilityList(
        label=ChefResponsibility.label.field.verbose_name,
        help_text=ChefResponsibility.label.field.help_text,
    )

    # User fields
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password', write_only=True, required=False)

    class Meta:
        model = Chef
        fields = [
            'id',
            'bio',
            'responsibilities',
            # User fields
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def validate(self, attrs):
        UserModelSerializer(
            data=self.initial_data,
            instance=self.instance.user if self.instance else None,
        ).is_valid(raise_exception=True)
        return super().validate(attrs)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        responsibilities = validated_data.pop('responsibilities', [])

        with transaction.atomic():
            user = USER_MODEL.objects.create_user(**user_data)
            chef = Chef.objects.create(user=user, **validated_data)
            chef.set_responsibilities(*responsibilities)
            return chef

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        responsibilities = validated_data.pop('responsibilities', [])

        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        super().update(instance, validated_data)

        if responsibilities is not None:
            instance.set_responsibilities(*responsibilities)
        return instance


class ChefSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Chef
        fields = ['full_name', 'username']

    def get_full_name(self, obj) -> str:
        return obj.user.get_full_name()