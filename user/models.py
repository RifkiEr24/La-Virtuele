from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, password=None):
        if not email or not username or not first_name:
            raise ValueError("Data is not complete")        

        user = self.model(email = email, username = username, first_name = first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, password):
        user = self.create_user(email = email, username = username, first_name = first_name, password = password)
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    avatar = models.ImageField(upload_to='media/avatar/', height_field='height', width_field='width')
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    objects = UserManager()
    
    def __str__(self):
        return self.username or ''

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True
    