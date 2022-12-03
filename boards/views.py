from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,Http404
from .models import Board,Topic,Post
from django.contrib.auth.models import User 
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from froala_editor.widgets import FroalaEditor


# Create your views here.
# def home(request):
#     boards=Board.objects.all()
#     return render(request,'home.html',{'boards':boards})

class BoardListView(ListView):
    model=Board
    context_object_name="boards"
    template_name="home.html"

def board_topics(request,board_id):
    # try:
    #     board=Board.objects.get(pk=board_id)
    # except Board.DoesNotExist:
    #     raise Http404
    board=get_object_or_404(Board,pk=board_id)
    queryset=board.topics.order_by('-created_dt').annotate(topic_no=Count('posts'))
    page=request.GET.get('page',1)
    paginator=Paginator(queryset,8)
    try:
        topics=paginator.page(page)
    except PageNotAnInteger:   
        topics=paginator.page(1)
    except EmptyPage:
        topics=paginator.page(paginator.num_pages)

    return render(request,'topics.html',{'board':board ,'topics':topics})

@method_decorator(login_required , name='dispatch') 
class NewTopicView(View):
    def render(self,request,board,form):
        return render(request,'new_topic.html',{'board':board,'form':form})
    def post(self,request,board_id):
        board=get_object_or_404(Board,pk=board_id)
        form= NewTopicForm(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            topic.board=board
            topic.created_by=request.user
            topic.save()
            post=Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=request.user,
                topic=topic
            )
            return redirect('board_topics',board_id=board.pk)
        return self.render(request,board,form)
    def get(self,request,board_id):
        board=get_object_or_404(Board,pk=board_id)
        form=NewTopicForm()
        return self.render(request,board,form)


# @login_required
# def new_topic(request,board_id):
#     board=get_object_or_404(Board,pk=board_id)
#     # user=User.objects.first()
#     if request.method=='POST':
#         form= NewTopicForm(request.POST)
#         if form.is_valid():
#             topic=form.save(commit=False)
#             topic.board=board
#             topic.created_by=request.user
#             topic.save()

#             post=Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 created_by=request.user,
#                 topic=topic
#             )
#             return redirect('board_topics',board_id=board.pk)
#     else:
#         form=NewTopicForm()
#     # if request.method=='POST':
#     #     subject=request.POST['subject']
#     #     message=request.POST['message']
#     #     user=User.objects.first()

#     #     topic=Topic.objects.create(subject=subject,board=board,created_by=user)
#     #     post=Post.objects.create(message=message,topic=topic,created_by=user)
#     #     return redirect('board_topics',board_id=board.pk)
#     return render(request,'new_topic.html',{'board':board,'form':form})

#new commit
def topic_posts(request,board_id,topic_id):
    topic=get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
    session_key="view_topic_{}".format(topic.pk)
    if not request.session.get(session_key,False):
        topic.views+=1
        topic.save()
        request.session[session_key]=True
    return render(request,'topic_posts.html',{'topic':topic})

@method_decorator(login_required , name='dispatch') 
class ReplyTopicView(View):
    def render(self,request,topic,form):
        return render(request,'reply_topic.html',{"topic":topic,"form":form})   
    
    def post(self,request,board_id,topic_id):
        topic=get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.topic=topic
            post.created_by=request.user
            post.save()

            topic.updated_by=request.user
            topic.updated_dt=timezone.now()
            topic.save()
            return redirect('topic_posts',board_id=board_id,topic_id=topic_id)
        return self.render(request,topic,form)
    
    def get(self,request,board_id,topic_id):
        topic=get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
        form=PostForm()
        return self.render(request,topic,form)


# def reply_topic(request,board_id,topic_id):
#      topic=get_object_or_404(Topic,board__pk=board_id,pk=topic_id)
#      if request.method=='POST':
#         form= PostForm(request.POST)
#         if form.is_valid():
#             post=form.save(commit=False)
#             post.topic=topic
#             post.created_by=request.user
#             post.save()

#             return redirect('topic_posts', board_id=board_id, topic_id=topic_id )
#      else:     
#         form=PostForm()
#      return render(request,'reply_topic.html',{'topic':topic,'form':form})
@method_decorator(login_required,name="dispatch")
# class PostUpdateView(UpdateView):
    # model=Post
    # fields=("message",)
    # template_name='edit_post.html'
    # pk_url_kwarg='post_id'
    # context_object_name='post'
    
    # def form_valid(self,form):
    #     post=form.save(commit=False)
    #     post.updated_by=self.request.user
    #     post.updated_dt=timezone.now()
    #     post.save()

    #     return redirect("topic_posts",board_id=post.topic.board.pk,topic_id=post.topic.pk)

# not complete
class PostUpdateView(View):
    def render(self,request,post,form):
        return render(request,'edit_post.html',{"post":post,"form":form})
    def post(self,request,board_id,topic_id,post_id):
        post=get_object_or_404(Post,board__pk=board_id,topic__pk=topic_id,pk=post_id)
        print(post)

    def get(self,request,board_id,topic_id,post_id):
        post=get_object_or_404(Post,topic__pk=topic_id,pk=post_id)
        # return HttpResponse(post.message,'khalid')
        form=PostForm()
        return self.render(request,post,form)