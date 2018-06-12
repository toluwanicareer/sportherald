from django.core.management.base import BaseCommand, CommandError
from steem.steemd import Steemd
from django.contrib.auth.models import User
from main.models import Post
import datetime
from django.utils import timezone

class Command(BaseCommand):
    args=''
    help ='Check the Invetsment, and update necessary Investment daily'

    def handle(self, *args, **options):
        s=Steemd()
        now=datetime.datetime.now()

        users=User.objects.all()
        for user in users:
            posts=s.get_discussions_by_author_before_date('areoye', None, now.strftime("%Y-%m-%dT%H:%M"), 10)
            for post in posts:
                try:
                    steem_post=Post.objects.get(slug=post.pop('root_permlink'))
                except Post.DoesNotExist:
                    pass
                steem_post.update(post)














