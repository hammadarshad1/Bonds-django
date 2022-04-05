from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """To create user using custom fields"""
        if not email:
            raise ValueError("Invalid Email!!")
        user = self.model(
            email=self.normalize_email(email),
            **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """To create superuser using custom fields"""
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
