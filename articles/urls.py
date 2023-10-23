from django.urls import path
# from . import views
from .views import ArticleView, ArticleDetailView, CommentView, CommentDetailView

urlpatterns = [
    path('', ArticleView.as_view()),
    path("<int:article_id>/", ArticleDetailView.as_view()),
    path("<int:article_id>/comment/", CommentView.as_view()),
    path("comment/<int:comment_id>/", CommentDetailView.as_view()),
]
