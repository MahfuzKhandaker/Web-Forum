from django.shortcuts import render,reverse  , redirect, get_object_or_404
from webforum.models import Forum, Topic, Post
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from .forms import NewTopicForm , PostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView
from django.utils import timezone

# def home(request):
#     forums = Forum.objects.all()
#     return render(request, 'home.html', {'forums':forums})
class ForumListView(ListView):
    model = Forum
    context_object_name = 'forums'
    template_name = 'home.html'

# def forum_topics(request, pk):
#     forum = get_object_or_404(Forum, pk=pk) 
#     queryset = forum.topics.order_by('-last_updated').annotate(replies=(Count('posts') -1))
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 10)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)

#     context = {
#         'forum':forum,
#         'topics': topics
#     }
#     return render(request, 'topics.html', context)
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['forum'] = self.forum
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.forum = get_object_or_404(Forum, pk=self.kwargs.get('pk'))
        queryset = self.forum.topics.order_by('-last_updated').annotate(replies=(Count('posts') -1))
        return queryset


# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic': topic})

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, forum__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_on')
        return queryset

@login_required
def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)

    form = NewTopicForm()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.started_by = request.user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)

    else:
        form = NewTopicForm()

    context = {
        'forum':forum, 
        'form':form
        }
    return render(request, 'new_topic.html', context )




@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk':pk, 'topic_pk':topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url = topic_url,
                id = post.pk,
                page = topic.get_page_count()
            )

            return redirect(topic_post_url)
        
    else:
        form = PostForm()

    return render(request, 'reply_topic.html', {'topic': topic, 'form':form})
    

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_on = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.forum.pk, topic_pk=post.topic.pk)