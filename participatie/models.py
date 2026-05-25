from django.db import models
from django.utils.text import slugify

THEME_CHOICES = [
    ('veiligheid', 'Veiligheid'),
    ('verkeer',    'Verkeer & Mobiliteit'),
    ('groen',      'Groen & Duurzaamheid'),
    ('wonen',      'Wonen'),
    ('onderwijs',  'Onderwijs & Jeugd'),
    ('zorg',       'Zorg & Welzijn'),
    ('cultuur',    'Cultuur & Sport'),
    ('overig',     'Overig'),
]


class Proposal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='overig')
    votes = models.IntegerField(default=0)
    votes_for = models.IntegerField(default=0)
    votes_against = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-votes', '-created_at']


class LiveUpdate(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
