# Create your urls here.
from django.urls import path
from apps.blogs import views

app_name = "blogs"

urlpatterns = [
    path('blogs/', views.BlogsListAPIView.as_view()),

]
# urlpatterns = format_suffix_patterns(urlpatterns)
