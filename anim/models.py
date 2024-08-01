from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from rating.models import Rating
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime


class anim(models.Model):
    status = (
        ('منتشر نشده','منتشر نشده'),
        ('در حال انتشار','در حال انتشار'),
        ('منتشر شده','منتشر شده'),
    )
    name_english = models.CharField(unique=True,max_length=255)
    name_farsi = models.CharField(unique=True,max_length=255)
    name_Japanese = models.CharField(unique=True,max_length=255)
    description = models.TextField()
    trailer = models.FileField(upload_to="media/TR/", blank=True)
    photo = models.ImageField(default='media/photo/default.jpg')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=13,choices=status)
    seasion = models.IntegerField(default=1)
    max_episod = models.IntegerField(default=12)
    publication_year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(datetime.datetime.now().year)])
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
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
    timestamp = models.DateTimeField(auto_now_add=True)



class anim_video(models.Model):
    anim = models.ForeignKey(anim, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.FileField()
    episod = models.IntegerField(default=1)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'episod'
        ordering = ['episod']

class anim_sub(models.Model):
    anim = models.ForeignKey(anim, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    subtile = models.FileField()
    episod = models.IntegerField(default=1)
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'subtiles'
        ordering = ['-created_at']
