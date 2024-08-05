from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from rating.models import Rating
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.utils.translation import gettext_lazy as _



class anim(models.Model):
    status = (
        ('منتشر نشده','منتشر نشده'),
        ('در حال انتشار','در حال انتشار'),
        ('منتشر شده','منتشر شده'),
    )

    name_english = models.CharField(_('name_english'),unique=True,max_length=255)
    name_farsi = models.CharField(_('name_farsi'),unique=True,max_length=255)
    name_Japanese = models.CharField(_('name_Japanese'),unique=True,max_length=255)
    description = models.TextField(_('description'))
    trailer = models.FileField(_('trailer'),upload_to="media/TR/", blank=True)
    photo = models.ImageField(_('photo'),default='media/photo/default.jpg')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(_('status'),max_length=13,choices=status)
    seasion = models.IntegerField(_('seasion'),default=1)
    max_episod = models.IntegerField(_('max_episod'),default=12)
    publication_year = models.IntegerField(_('publication_year'),validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)])
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)
    accepted = models.BooleanField(_('accepted'),default=False)
    tags = TaggableManager()
    ratings = GenericRelation(Rating)
    comments = GenericRelation(Comment)

    def average_rating(self):
        total_ratings = self.ratings.count()
        if total_ratings > 0:
            return (sum([rating.average for rating in self.ratings.all()]) / total_ratings) * 10
        else:
            return None

    class Meta:
        ordering = ['-created_at']

    def str(self) -> str:
        return self.name_english



class View(models.Model):
    anim = models.ForeignKey(anim, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(_('timestamp'),auto_now_add=True)



class anim_video(models.Model):
    anim = models.ForeignKey(anim, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField(_('video'))
    episod = models.IntegerField(_('episod'),default=1)
    accepted = models.BooleanField(_('accepted'),default=False)
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)


    class Meta:
        verbose_name_plural = 'episod'
        ordering = ['episod']

class anim_sub(models.Model):
    anim = models.ForeignKey(anim, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subtile = models.FileField(_('subtile'))
    episod = models.IntegerField(_('episod'),default=1)
    accepted = models.BooleanField(_('accepted'),default=False)
    created_at = models.DateTimeField(_('created_at'),auto_now_add=True)

    class Meta:
        verbose_name_plural = 'subtiles'
        ordering = ['-created_at']
