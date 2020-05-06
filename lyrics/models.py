from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from six import python_2_unicode_compatible
# Create your models here.


class Album(models.Model):
    objects = models.Manager()
    album = models.CharField(max_length=200)

    def __str__(self):
        return self.album


class Artist(models.Model):
    objects = models.Manager()
    artist_name = models.CharField(max_length=100)

    def __str__(self):
        return self.artist_name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


@python_2_unicode_compatible
class Post(models.Model, HitCountMixin):
    objects = models.Manager()  # Our default Manager
    published = PublishedManager()  # Custom Model Manager

    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published'),
    }
    username = models.CharField(max_length=100, blank=True, verbose_name='Submitted by')
    artists = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True, related_name='artist_list')
    artist = models.CharField(max_length=100, verbose_name='Artist/band')
    title = models.CharField(max_length=100, verbose_name='Song title')
    slug = models.SlugField(max_length=120, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    albums = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True, related_name='album_detail')
    album = models.CharField(max_length=100, blank=True)
    content = models.TextField(verbose_name='lyrics')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # hei hi post zawh veleh a, a luh leh na tur a ni
        return reverse('home')  # homepage a luh nghalna.
        #  return reverse('post-detail', kwargs={'pk': self.pk})  # hei hi kan thil post zawh chiah a luh nghalna.


@receiver(pre_save, sender=Post)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].title)
    kwargs['instance'].slug = slug





