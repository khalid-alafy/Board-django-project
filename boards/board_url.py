from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required
from froala_editor import views as f_views


urlpatterns = [
    path('', views.BoardListView.as_view(),name="home"),
    path('boards/<int:board_id>/',views.board_topics,name="board_topics"),
    path('boards/<int:board_id>/new/',views.NewTopicView.as_view(),name="new_topic"),
    path('boards/<int:board_id>/topics/<int:topic_id>/',views.topic_posts,name="topic_posts"),
    path('boards/<int:board_id>/topics/<int:topic_id>/reply',views.ReplyTopicView.as_view(),name="reply_topic"),
    path('boards/<int:board_id>/topics/<int:topic_id>/posts/<int:post_id>/edit',login_required(views.PostUpdateView.as_view()),name="edit_post"),
    path('froala_editor/',include('froala_editor.urls'))

]

