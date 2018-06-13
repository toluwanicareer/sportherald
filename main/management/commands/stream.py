from django.core.management.base import BaseCommand, CommandError
from steem.steemd import Steemd
from django.contrib.auth.models import User
from main.models import Post
import datetime
from django.utils import timezone
from main.models import update_post

class Command(BaseCommand):
    args=''
    help ='Check the Invetsment, and update necessary Investment daily'

    def handle(self, *args, **options):
        s=Steemd()
        now=datetime.datetime.now()
        update_post()

















