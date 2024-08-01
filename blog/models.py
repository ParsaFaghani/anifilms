from django.db import models

class Article(models.Model):
    name = models.CharField(unique=True,max_length=255)
    description = models.TextField()
    photo_code = models.CharField(max_length=255,editable=False, default='media/photo/default.jpg',blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    comments = GenericRelation(Comment)
    ratings = GenericRelation(Rating)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self) -> str:
        return self.name_english