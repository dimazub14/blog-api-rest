# Create your urls here.
from django.urls import path
from apps.blog.views import BlogView
app_name = "blogs"

urlpatterns = [
    path('blogs/', BlogView.as_view()),
    path('blogs/<int:pk>', BlogView.as_view()),
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
