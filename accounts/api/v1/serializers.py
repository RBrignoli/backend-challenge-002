"""
API V1: Accounts Serializers
"""
###
# Libraries
###
from django.contrib.auth.models import User
from rest_auth.models import TokenModel
from rest_auth.serializers import (
    UserDetailsSerializer as BaseUserDetailsSerializer,
    PasswordResetSerializer as BasePasswordResetSerializer,
)
from rest_framework import serializers
from rest_framework.validators import ValidationError

from accounts.forms import (
    CustomResetPasswordForm,
)

from accounts.models import User

from rest_auth.registration.serializers import RegisterSerializer as BaseRegisterSerializer


###
# Serializers
###
class UserTokenSerializer(serializers.ModelSerializer):
    user = BaseUserDetailsSerializer()

    class Meta:
        model = TokenModel
        fields = ('key', 'user',)


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        user = self.context['request'].user

        if user.email == email:
            raise ValidationError('Cannot change to the same email.')

        if User.objects.exclude(id=user.id).filter(email=email).exists():
            raise ValidationError('Another account already exists with this email.')

        return email


class PasswordResetSerializer(BasePasswordResetSerializer):
    password_reset_form_class = CustomResetPasswordForm

    def get_email_options(self):
        return {
            'subject_template_name': 'account/password_reset_subject.txt',
            'email_template_name': 'account/password_reset_message.txt',
            'html_email_template_name': 'account/password_reset_message.html',
        }


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('height', 'weight', 'date_of_birth', 'gender')

class RegisterSerializer(BaseRegisterSerializer):

    corporate = serializers.SlugRelatedField(
        slug_field='name',
        write_only=True,
        queryset = Corporation.objects.all(),
        required = True,
    )

    name = serializers.CharField(
        write_only=True,
        max_lenght=64,
        required=True,
        allow_blank=False,
    )



    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username',''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'name': self.validated_data.get('name', ''),
            'corporate': self.validated_data('corporate', ''),

        }

    def custom_signup(self, request, user):
        user.corporate = self.get_cleaned_data().get('corporate'),
        user.name = self.get_cleaned_data().get('name')
        user.save()
        pass

    def validate(self, data):
        if data.get('corporate') and data.get('corporate').users.filter(name=data.get('name')).exist():
            raise serializers.ValidationError({'name':("A user is already registered with this name")})
        return super().validate(data)




