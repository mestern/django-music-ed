from django.template.defaultfilters import slugify
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse
from django.db import models
import os


#  ___________-------------posts section-------------_____________

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250, choices=Status.choices, default=Status.DRAFT)
    file = models.FileField(upload_to='documents/', blank=True, null=True, )
    view = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    # objects = jalali.jManager()
    published = PublishedManager()


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        # for Persian localization model name in the admin panel
        # verbose_name = "پست"
        # chon jame post to minevesht (posts) bayad jamesh ro taqir dad
        # verbose_name_plural = "پست ها"

    # def delete(self, using=None, keep_parents=False):
    #     if pre_delete:
    #         print("sig", "*"*30)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app1:post_details", args=[self.id])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    image = models.ImageField(upload_to='profile/', blank=True, null=True)
    # location = models.CharField(max_length=120)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: {self.post}"

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['-created'])
        ]



class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(blank=True, upload_to='posts')
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    @receiver(post_delete)
    def pre_delete(sender, instance, **kwargs):
        if isinstance(instance, Image):
            if instance.image:  # Replace your_file_field with the name of your FileField/ImageField
                instance.image.delete(save=False)


# #  ___________-------------options section-------------_____________

class Ticket(models.Model):
    SUBJECT_CHOICES = [
        ('SUG', 'suggestions'),
        ('CRT', 'criticism'),
        ('REP', 'report')
    ]
    # name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ticket')
    name = models.CharField(max_length=30)
    subject = models.CharField(choices=SUBJECT_CHOICES, default=SUBJECT_CHOICES[2])
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=250)
    message = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    # publish = jalali.jDateTimeField(default=jalali.timezone.now)

    def __str__(self):
        return self.phone

    # class Meta:
    #     ordering = ['name']
    #     indexes = [
    #         models.Index(fields=['name'])







