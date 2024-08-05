from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
import PIL.Image as Image
from anim.models import anim
from django.core.validators import RegexValidator


class Subscription(models.Model):
    DURATION_CHOICES = [
        (30, 'یک ماهه'),
        (90, 'سه ماهه'),
        (180, 'شش ماهه'),
        (365, 'یک ساله'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField(choices=DURATION_CHOICES)

    def __str__(self):
        return self.name



class Profile(models.Model):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('fa', 'Farsi'),
   )
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    photo = models.ImageField(_('photo'),default='p_photos/profile.png')
    bio = models.TextField(_('bio'),default='', blank=True)
    admin = models.BooleanField(_('admin'),default=False)
    translator = models.BooleanField(_('translator'),default=False)
    bloger = models.BooleanField(_('bloger'),default=False)
    manager = models.BooleanField(_('manager'),default=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_('phone'),validators=[phone_regex], max_length=17, blank=True)
    telegram = models.URLField(_('telegram'),default='', blank=True)
    language = models.CharField(default='fa', choices=LANGUAGE_CHOICES, max_length=5)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    subscription_end = models.DateField(_('subscription_end'),null=True, blank=True)
    

    def save(self, *args, **kwargs):
        super().save()

    def __str__(self):
        return f'{self.user.username}'


class DiscountCode(models.Model):
    code = models.CharField(_('code'),max_length=50, unique=True)
    discount = models.DecimalField(_('discount'),max_digits=5, decimal_places=2)
    start_date = models.DateField(_('start_date'))
    end_date = models.DateField(_('end_date'))


class Follow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')    
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owner', 'reciever')

        
    def __str__(self):
        return f'{self.owner.username} follows {self.reciever.username}'


class Save(models.Model) :
    owner = models.ForeignKey(User, related_name='save_owner', on_delete=models.CASCADE)    
    anim = models.ForeignKey(anim, on_delete=models.CASCADE, related_name='anim_saves')
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'anim')

    def __str__(self) :
        return '%s saved %s... post'%(self.owner.username, self.anim.description[:15])



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Follow.objects.create(owner=instance, reciever=instance)



@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user.save()
    pass
