from django.shortcuts import render, Http404
from .models import Post, PostImage, Comment, Tag, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
from . import models
from joins.forms import JoinForm
from joins.models import Join
from .forms import CommentForm
from django.db.models import Count


def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        posts = Post.objects.filter(title__icontains=q)
        context = {'query': q,
                   'posts': posts}
        template = 'blog/results.html'
    else:
        context = {}
        template = 'blog/list_posts.html'

    return render(request, template, context )

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


def list_posts(request):
    posts = Post.objects.all()

    # this method is using django forms
    # email_form = EmailForm(request.POST or None)

    comments_count = Comment.objects.all().count()
    categories = Category.objects.all()[:3]
    categories2 = Category.objects.filter(posts=posts)

    comments = Comment.objects.all()[:5]
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    email_form = JoinForm(request.POST or None)
    confirm_message = None

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # this methos is using django forms
    # if email_form.is_valid():
    #     email = email_form.cleaned_data['email']
    #     new_join, created = Join.objects.get_or_create(email=email)
    #     print new_join, created

    #this method is using model forms:

    if email_form.is_valid():
        new_join = email_form.save(commit=False)
        # email = email_form.cleaned_data['email']
        # new_join, created = Join.objects.get_or_create(email=email)
        new_join.ip_address = get_ip(request)
        new_join.save()

        confirm_message = "Thank you for subscribing"
        email_form = None

    context = {
        'posts': posts,
        'comments': comments,
        'paginator': paginator,
        'page': page,
        'email_form': email_form,
        'confirm_message': confirm_message,
        'categories': categories,
        'categories2': categories2,
        'comments_count': comments_count,



    }

    return render(request, 'blog/list_posts.html', context)


class TagDetail(generic.DetailView):
    model = models.Tag
    template_name = 'blog/tag.html'
    slug_url_kwarg = 'tag'


def single_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
        comments = Comment.objects.filter(post=post)
        comment_form = CommentForm(request.POST or None)
        categories = post.category_set.all()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()



        context = {'post': post,
                   'categories': categories,
                   'comment_form': comment_form,
                   'comments': comments,}

        return render(request, 'blog/single_post.html', context)
    except:
        raise Http404


def category_single(request, slug):

    try:
        category = Category.objects.get(slug=slug)
        context = {'category': category}
        return render(request, 'blog/category.html', context)
    except:
        raise Http404


