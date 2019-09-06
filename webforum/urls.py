from django.urls import path
from webforum import views

urlpatterns=[
    path('', views.ForumListView.as_view(), name='home'),
    path('forums/<int:pk>/', views.TopicListView.as_view(), name='forum_topics'),
    # http://127.0.0.1:8000/webforum/forums/1/new/
    path('forums/<int:pk>/new/', views.new_topic, name='new_topic'),
    # http://127.0.0.1:8000/webforum/forums/2/topics/5/
    path('forums/<int:pk>/topics/<int:topic_pk>/', views.PostListView.as_view(), name='topic_posts'),
    # http://127.0.0.1:8000/webforum/forums/2/topics/5/reply/
    path('forums/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('forums/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post')
]