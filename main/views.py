from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Post, Sport
from acc.models import Profile
from .forms import PostForm
from django.http import JsonResponse, HttpResponseRedirect, Http404
import pdb
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import  User
import json
import datetime
import requests
from steemconnect.client import Client
from steemconnect.operations import Comment, Vote
#from steem.steemd import Steemd
# Create your views here.
from django.template.defaultfilters import slugify

class ViewMixin:
    page=None
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
#hghg
    def get_context_data(self, *args, **kwargs):
        context = super(ViewMixin, self).get_context_data(*args, **kwargs)
        context['sports'] = Sport.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            offset = int(request.POST.get('offset'))
            sport_id = (request.POST.get('sport_id'))
            new_offset = offset + settings.PAGE_LENGTH
            if sport_id == '*':
                posts = self.main_queryset
            else:
                posts = self.main_queryset.filter(sport_id=sport_id)[offset:new_offset]
                #pdb.set_trace()
            if self.page == 'review':
                context={'posts': posts, 'page': 'review'}
            else:
                context = {'posts': posts}
            response = render_to_string('includes/post_list.html', context)
            return JsonResponse({'data': response, 'offset': new_offset})
        else:
            return Http404('Invalid Access')


@method_decorator(csrf_exempt, name='dispatch')
class homeView(ViewMixin, ListView):
    main_queryset=Post.objects.filter(status='approved').order_by('-approved_date')
    queryset =main_queryset[:settings.PAGE_LENGTH]


@method_decorator(csrf_exempt, name='dispatch')
class BlogView(LoginRequiredMixin, ViewMixin, ListView):

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_date')[:settings.PAGE_LENGTH]

    def post(self, request, *args, **kwargs):
        self.main_queryset=Post.objects.filter(author=self.request.user).order_by('-created_date')
        return  super(BlogView, self).post(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class reviewView(ViewMixin,ListView):
    main_queryset=Post.objects.filter(status='submitted').order_by('-created_date')
    queryset = main_queryset[:settings.PAGE_LENGTH]

    def get_context_data(self, *args, **kwargs):
        context=super(reviewView, self).get_context_data(*args, **kwargs)
        context['page']='review'
        return context

    def post(self,request,*args, **kwargs):
        self.page='review'
        return super(reviewView, self).post(request, *args, **kwargs)


class CreatePost(CreateView):
    model=Post
    form_class=PostForm

    def form_valid(self, form):
        post=form.save(commit=False)
        post.author=self.request.user
        tags=self.request.POST.get('tags')
        tags_list=tags.split(',')
        post.status='submitted'
        if not self.request.user.username == 'admin':# remember to remove in production
            user=self.request.user
        else:
            user=User.objects.get(username='areoye')

        profile=Profile.objects.get(user=user)
        status=post.save()
        if status == 'Exist':
            messages.warning(self.request, 'Value Error, Use a different title ')
            #pdb.set_trace()
            return HttpResponseRedirect('/')
        form.save_m2m()

        cli=get_c(profile)


        comment=Comment(
            author=user.username,
            permlink=post.slug,
            body=post.body,
            title=post.title,
            parent_permlink="sportherald",
            json_metadata={"app": "sportherald.app", 'tags':tags_list}
        )
        try:
            rich=cli.broadcast([comment.to_operation_structure()])


            messages.success(self.request, 'Post Submitted and under review')
            #pdb.set_trace()
        except:
            messages.warning(self.request, 'Network Error')

        #pdb.set_trace()


        #return JsonResponse({'status': 200, 'slug': post.slug, 'posting_key': posting_key, 'username': user.username})
        return HttpResponseRedirect('/')
'''
    def form_invalid(self,form):
        pdb.set_trace()
'''


@method_decorator(csrf_exempt, name='dispatch')
class PostStatus(View):
    def post(self, request,*args, **kwargs):
        id = request.POST.get('id')
        status=request.POST.get('status')
        comment=request.POST.get('comment')
        try:
            post=Post.objects.get(id=id)
            post.status=status
            post.approved_date= timezone.now()
            post.save()
            posts=Post.objects.filter(status='submitted')[:settings.PAGE_LENGTH]
            response=render_to_string('includes/post_list.html', {'posts':posts, 'page':'review'})
            now=datetime.datetime.now()
            new_slug=now.strftime("%Y-%m-%d-%H%M")
            slug=slugify(comment)+new_slug
            if not self.request.user.username == 'admin':  # remember to remove in production
                user = self.request.user
            else:
                user = User.objects.get(username='areoye')

            comment = Comment(
                author=user.username,
                body=comment,
                permlink=slug,
                title='',
                parent_permlink=post.slug,
                parent_author=post.author.username,
                json_metadata={"app": "sportherald.app" }
            )
            profile = Profile.objects.get(user=user)
            com=get_c(profile)
            rich=com.broadcast([comment.to_operation_structure()])
            #pdb.set_trace()

            return  JsonResponse({'status':200, 'message':'Successfully Updated',
                                  'data':response})

        except Post.DoesNotExist:
            return JsonResponse({'status':404, 'message':'Post not found'})

@login_required
def upvote(request, id):
    try:
        post=Post.objects.get(id=id)
    except:
        pass
    vote=Vote(
        voter='ckole',#request.user.username,
        author='areoye',#post.author.username,
        permlink=post.slug,
        percent=100,

    )
    user=User.objects.get(username='ckole')
    profile=get_profile(user)
    c=get_c(profile)
    res=c.broadcast(vote.to_operation_structure())
    #s=Steemd()
    #content=s.get_content(author=post.author.username, permlink=post.slug)
    #post.update(content)
    pdb.set_trace()
    return HttpResponseRedirect('/')

def get_c(profile):
    refresh_token = profile.refresh_token
    url = "https://v2.steemconnect.com/api/oauth2/token"
    response_access = requests.post(url, data={'refresh_token': refresh_token,
                                               'client_id': 'sportherald.app',
                                               'client_secret': settings.CLIENT_SECRET,
                                               'scope': "vote,comment,offline, comment_options,claim_reward_balance"})
    access_token = response_access.json().get('access_token')
    c = Client(access_token=access_token, client_id='sportherald.app', client_secret=settings.CLIENT_SECRET)
    return c

def get_profile(user):
    return Profile.objects.get(user__username=user)

class PostDetail(ViewMixin, DetailView):
    model=Post
    context_object_name = 'post'
    template_name = 'details.html'
    page='detail'


class CommentView(View):

    def get(self, *args, **kwargs ):
        comm=self.request.GET.get('comment')
        post_id=self.request.GET.get('id')
        now = datetime.datetime.now()
        new_slug = now.strftime("%Y-%m-%d-%H%M")
        slug = slugify(comm) + new_slug
        user=self.request.user
        post = Post.objects.get(id=post_id)
        comment = Comment(
            author=user.username,
            body=comm,
            permlink=slug,
            title='',
            parent_permlink=post.slug,
            parent_author=post.author.username,
            json_metadata={"app": "sportherald.app"}
        )
        profile = Profile.objects.get(user=user)
        com = get_c(profile)
        rich = com.broadcast([comm.to_operation_structure()])
        return JsonResponse({'status': 200, 'message': 'Successfully Updated',
                             })



