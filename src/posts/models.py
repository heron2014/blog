import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import permalink


class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug


class PostManager(models.Manager):
    def published(self):
        return super(PostManager, self).filter(published=True)

    def recent_posts(self):
        return self.published().filter('-created')[:5]


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User)
    published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)

    objects = PostManager()
    items = PostManager()

    class Meta:
        unique_together = ('title', 'slug')
        ordering = ['-created']

    def __unicode__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('single_post', kwargs={'slug': self.slug})


class PostImage(models.Model):
    post = models.ForeignKey(Post)
    image = models.ImageField(upload_to='posts/image/')
    title = models.CharField(max_length=120, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return str(self.image)


class Category(models.Model):
    posts = models.ManyToManyField(Post)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    username = models.CharField(max_length=45)
    email = models.EmailField(max_length=200)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return unicode("%s: %s" % (self.post, self.body[:60]))

