from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone



class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, first name, last name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password=None):

        """
        Creates and saves a superuser with the given email, first name, last name and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user
    

    def check_user_credentials(self,email, first_name, last_name, password):
        
        from django.contrib.auth import get_user_model
    
        User = get_user_model()
    
        try:
        # First check if a user with this email exists
            user = User.objects.get(email=email,first_name = first_name, last_name = last_name)
        
        # Then verify the password
            if user.check_password(password):
                return True, user
            else:
            # Email exists but password is wrong
                return False, None
            
        except User.DoesNotExist:
        # No user with this email exists
            return False, None
# Define the User Model

class User(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True, verbose_name='email')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        # For simplicity, admin users have all permissions
        return self.is_admin
    
    def has_module_perms(self, app_label):
        # For simplicity, admin users have access to all modules
        return self.is_admin
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        db_table = 'User'
        ordering = ['id']