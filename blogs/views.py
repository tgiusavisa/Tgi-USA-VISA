from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required

def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blogs/blog_list.html', {'posts': posts})

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm()
    return render(request, 'blogs/blog_form.html', {'form': form})