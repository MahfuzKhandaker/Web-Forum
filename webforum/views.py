from django.shortcuts import render, get_object_or_404
from webforum.models import Forum
from django.http import Http404

def home(request):
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums':forums})


def forum_topics(request, pk):
    forum = get_object_or_404(Forum, pk=pk) 
    return render(request, 'topics.html', {'forum': forum})

