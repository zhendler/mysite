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
    path('register/', register, name='register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]