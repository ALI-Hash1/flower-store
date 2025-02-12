from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password):
        if not phone_number:
            raise ValueError('user must have phone number.')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, email, password):
        user = self.create_user(phone_number, password)

        if not email:
            raise ValueError('superuser must have email.')

        user.email = email
        user.is_admin = True
        user.save()

        return user
