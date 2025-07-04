from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jalali


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
    slug = models.SlugField()
    publish = jalali.jDateTimeField(default=timezone.now)
    created = jalali.jDateTimeField(auto_now_add=True)
    update = jalali.jDateTimeField(auto_now=True)
    status = models.CharField(max_length=250, choices=Status.choices, default=Status.DRAFT)


    # objects = models.Manager()
    objects = jalali.jManager()
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app1:post_details", args=[self.id])


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
    publish = jalali.jDateTimeField(default=jalali.timezone.now)

    def __str__(self):
        return self.phone

    # class Meta:
    #     ordering = ['name']
    #     indexes = [
    #         models.Index(fields=['name'])
    #     ]