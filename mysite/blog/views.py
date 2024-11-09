from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import PostForm
from .models import Post, Author, Tag


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-added_at']

    def get_queryset(self):
        return Post.objects.all().order_by('-added_at')

class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        user = self.request.user  # Отримуємо поточного користувача
        author, created = Author.objects.get_or_create(
            user=user)  # Якщо автор існує, використовуємо його, інакше створюємо
        form.instance.author = author  # Призначаємо автора посту
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    form_class = PostForm
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author__user=self.request.user)


class AuthorPostsListView(ListView):
    model = Post
    template_name = 'blog/author_posts.html'
    context_object_name = 'posts'
    ordering = ['-added_at']

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        return Post.objects.filter(author__id=author_id).order_by('-added_at')

class TagsPostsListView(ListView):
    model = Post
    template_name = 'blog/tags_posts.html'
    context_object_name = 'posts'
    ordering = ['-added_at']

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        # Отримуємо пости з конкретним тегом за його ім'ям
        return Post.objects.filter(tags__name=tag_name).order_by('-added_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs['tag_name']
        try:
            context['tag'] = Tag.objects.get(name=tag_name)
        except Tag.DoesNotExist:
            context['tag'] = None
        return context







class LoginView(View):
    def get(self, request):
        return render(request, 'blog/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  # Перенаправлення на головну сторінку
        else:
            # Тут можна обробити помилку
            return render(request, 'blog/login.html',
                          {'error': 'Неправильний логін або пароль'})

class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('post_list')  # Перенаправлення на головну сторінку

    def get(self, request):
        return redirect('post_list')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                messages.success(request, 'Реєстрація успішна! Ви можете увійти.')
                return redirect('/')  # Заміни 'login' на свою URL-адресу для входу
            except Exception as e:
                messages.error(request, f'Помилка: {e}')
        else:
            messages.error(request, 'Паролі не співпадають!')

    return render(request, 'blog/register.html')







# Create your views here.

# def post_list(request):
#     posts = Post.objects.all().order_by('-added_at')
#     return render(request, 'blog/post_list.html', {'posts': posts})
#
#
# @login_required
# def post_detail(request, post_id):
#     post = Post.objects.get(id=post_id)
#     return render(request, 'blog/post_detail.html', {'post': post})
