from django.core.management.base import BaseCommand, CommandError
from steem.blockchain import Blockchain
from steem.post import Post
from main.models import Post as sport_post

class Command(BaseCommand):
    args=''
    help ='Check the Invetsment, and update necessary Investment daily'

    def handle(self, *args, **options):
        blockchain = Blockchain()
        stream = map(Post, blockchain.stream(filter_by=['comment']))
        #while True:

        for post in stream:
            #tags = post["tags"]
            if post.is_main_post() and post.parent_permlink == 'sportherald' :
                permlink=post.permlink
                try:
                    sportherald_post=sport_post.objects.get(slug=permlink)
                    sportherald_post.update(post)
                except Post.DoesNotExist:
                    pass








