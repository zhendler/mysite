from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, register, LogoutView, LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', post_list, name='post_list'),
    # path('<int:post_id>/', post_detail, name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register')

]