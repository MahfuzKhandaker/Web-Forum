from django.shortcuts import render
from webforum.models import Forum

def home(request):
    forums = Forum.objects.all()
    return render(request, 'home.html', {'forums':forums})
