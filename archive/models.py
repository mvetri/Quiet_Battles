from django.db import models


class Chapter(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    subtitle = models.CharField(max_length=250)

    description = models.TextField()

    # image = models.URLField(blank=True)
    image = models.ImageField(
    upload_to='chapters/',
    blank=True,
    null=True
)

    chapter_number = models.PositiveIntegerField(default=1)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['chapter_number']