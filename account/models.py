from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    # username = models.CharField(max_length=30, unique=True)
    # bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # AWS credentials fields
    aws_access_key_id = models.TextField( blank=True, null=True)
    aws_secret_access_key = models.TextField( blank=True, null=True)
    aws_region = models.TextField( blank=True, null=True)
    instance_id = models.TextField( blank=True, null=True)

    def __str__(self):
        return str(self.user)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = Profile.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile, sender=User)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# If the name already exists
# if not Category.objects.filter(name__iexact=self.name).exists():
#          super(Category, self).save(force_insert, force_update)