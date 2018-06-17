from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.urls import reverse
import pdb
from steem.steemd import Steemd
import datetime

# Create your models here.


class Sport(models.Model):
    name=models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, max_length=200)
    thumbnail=models.ImageField()


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Sport, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()
    status=models.CharField(max_length=200, choices=(('submitted', 'submitted'),
                                                     ('approved', 'approved'), ('rejected','rejected')))
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    sport=models.ForeignKey(Sport, on_delete=models.CASCADE, null=True)
    tags=TaggableManager()
    slug = models.SlugField(null=True, blank=True, max_length=200)
    created_date=models.DateTimeField(auto_now_add=True, null=True)
    approved_date=models.DateTimeField(null=True)
    online=models.BooleanField(default=False)
    likes=models.IntegerField(null=True)
    comment=models.IntegerField(null=True)
    shares=models.IntegerField(null=True)
    pending_payout=models.CharField(max_length=200, null=True)

    def update(self,post):
        self.likes=post.pop('net_votes')
        self.comment=post.pop('children')
        self.shares=post.pop('net_rshares')
        self.pending_payout=post.pop('pending_payout_value')
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:post_detail', kwargs={'slug': self.slug})



    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)+'author-'+self.author.username
            post=Post.objects.filter(slug=self.slug)
            #pdb.set_trace()
            if post.count() > 1:
                return 'Exist'

        return super(Post, self).save(*args, **kwargs)

def update_post():
    s=Steemd()
    now=datetime.datetime.now()
    users = User.objects.all()
    for user in users:
        posts = s.get_discussions_by_author_before_date(user.username, None, now.strftime("%Y-%m-%dT%H:%M"), 10)
        for post in posts:
            print('here')
            try:
                steem_post = Post.objects.get(slug=post.pop('root_permlink'))
                steem_post.update(post)

            except Post.DoesNotExist:
                print('does not exist')
                pass


