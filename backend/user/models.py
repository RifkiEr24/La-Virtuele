from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
import os

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name=None, password=None, **kwargs):
        if not email or not username or not first_name:
            raise ValueError("Data is not complete")        

        user = self.model(email = email, username = username, first_name = first_name, last_name = last_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(email = email, username = username, first_name = first_name, last_name = last_name, password = password)
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
    avatar = models.ImageField(upload_to='media/avatar/', height_field='height', width_field='width', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()
    
    def __str__(self):
        return self.username or ''

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url

@receiver(models.signals.post_delete, sender=User)
def auto_delete_user_avatar_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

@receiver(models.signals.pre_save, sender=User)
def auto_delete_user_avatar_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False
    new_file = instance.avatar
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except ValueError:
            return False

@receiver(models.signals.post_save, sender=User)
def auto_set_username(sender, instance, created, **kwargs):
    if not instance.username:
        instance.username = f'{instance.first_name}_{instance.last_name}'.lower()
        instance.save()