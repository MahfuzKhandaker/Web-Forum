from django.shortcuts import render, redirect, get_object_or_404
from webforum.models import Forum, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm 

def home(request):
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums':forums})


def forum_topics(request, pk):
    forum = get_object_or_404(Forum, pk=pk) 
    contex = {
        'forum':forum
    }
    return render(request, 'topics.html', contex)


def new_topic(request, pk):
    forum = get_object_or_404(Forum, pk=pk)
    user = User.objects.first()

    form = NewTopicForm()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.forum = forum
            topic.started_by = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('forum_topics', pk=forum.pk)

    else:
        form = NewTopicForm()

    context = {
        'forum':forum, 
        'form':form
        }
    return render(request, 'new_topic.html', context )