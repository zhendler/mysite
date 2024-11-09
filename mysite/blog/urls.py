from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, register, LogoutView, LoginView, \
    AuthorPostsListView, TagsPostsListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', post_list, name='post_list'),
    # path('<int:post_id>/', post_detail, name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('author/<int:author_id>/', AuthorPostsListView.as_view(), name='author_posts'),
    path('tags/<str:tag_name>/', TagsPostsListView.as_view(), name='tags_posts'),


    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register')

]