from django.shortcuts import render, redirect, get_object_or_404
from webforum.models import Forum, Topic, Post
from django.db.models import Count
from django.contrib.auth.models import User
from .forms import NewTopicForm , PostForm
from django.contrib.auth.decorators import login_required


def home(request):
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums':forums})


def forum_topics(request, pk):
    forum = get_object_or_404(Forum, pk=pk) 
    topics = forum.topics.order_by('-last_updated').annotate(replies=(Count('posts') -1))
    context = {
        'forum':forum,
        'topics': topics
    }
    return render(request, 'topics.html', context)


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


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, forum__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


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
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
        
    else:
        form = PostForm()

    return render(request, 'reply_topic.html', {'topic': topic, 'form':form})
    
