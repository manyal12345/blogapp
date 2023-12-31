from django.shortcuts import render, redirect, get_object_or_404
from app.forms import CommentForm, NewUserForm, SubscribeForm
from django.http import HttpResponseRedirect
from app.models import Comments, Post, Tag, Profile, VideoSlider, WebsiteMeta
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import login

# Create your views here.
def index(request):
    posts = Post.objects.all()
    top_post = Post.objects.all().order_by('-view_count')[0:3]
    recent_post = Post.objects.all().order_by('-last_updated')[0:3]
    featured_blog = Post.objects.filter(is_featured = True)
    subscribe_form = SubscribeForm()
    subscribe_successfully = None
    website_info = None
    video_slider = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    
    if VideoSlider.objects.all().exists():
        video_slider = VideoSlider.objects.all()

    if featured_blog:
        featured_blog = featured_blog[0]

    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            request.session['subscribed'] = True
            subscribe_successfully = 'Subscribed Successfully'
            subscribe_form = SubscribeForm()

    context = { 'posts':posts, 'top_post':top_post, 'recent_post':recent_post, 'subscribe_form':subscribe_form, 'subscribe_successfully':subscribe_successfully, 'featured_blog':featured_blog, 'website_info':website_info, 'video_slider':video_slider}
    return render(request, 'app/index.html', context)

def post_page(request, slug):
    post = Post.objects.get(slug = slug)
    comments = Comments.objects.filter(post = post, parent=None)
    form = CommentForm()
    #Bookmark Logic
    bookmarked = False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked = True
    is_bookmarked = bookmarked

    #Likes Logic
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    number_of_likes = post.number_of_likes()
    post_is_liked = liked


    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            if request.POST.get('parent'):
                #reply save
                parent = request.POST.get('parent')
                parent_obj = Comments.objects.get(id = parent)
                if parent_obj:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_obj
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))
            else:
                comment = comment_form.save(commit=False)
                postid = request.POST.get('post_id')
                post = Post.objects.get(id = postid)
                comment.post = post
                comment.save()
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug':slug}))

    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {'form':form, 'post':post, 'comments':comments, 'is_bookmarked':is_bookmarked, 'post_is_liked':post_is_liked, 'number_of_likes':number_of_likes}
    return render(request, 'app/post.html', context)

def tag_page(request, slug):
    tag =Tag.objects.get(slug=slug)
    top_post = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
    recent_post = Post.objects.filter(tags__in=[tag.id]).order_by('-last_updated')[0:3]
    tags = Tag.objects.all()

    context = {'tag':tag, 'top_post':top_post, 'recent_post':recent_post, 'tags':tags}
    return render(request, 'app/tag.html', context)

def author_page(request, slug):
    profile =Profile.objects.get(slug=slug)
    top_post = Post.objects.filter(author = profile.user).order_by('-view_count')[0:2]
    recent_post = Post.objects.filter(author = profile.user).order_by('-last_updated')[0:3]
    top_authors = User.objects.annotate(num_posts=Count('post')).order_by('-num_posts')

    context = {'profile':profile, 'top_post':top_post, 'recent_post':recent_post,'top_authors':top_authors }
    return render(request, 'app/author.html', context) 

def search_posts(request):
    search_query = ''
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains = search_query)
    context = {'posts':posts, 'search_query':search_query}
    return render(request, 'app/search.html', context) 

def about(request):
    website_info = None

    if WebsiteMeta.objects.all().exists():
        website_info = WebsiteMeta.objects.all()[0]
    context = {'website_info':website_info}
    return render(request, 'app/about.html', context) 

def register_user(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("/")

    context = {'form':form }
    return render(request, 'registration/registration.html', context) 

#Bookmark Logic
def bookmark_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

#like Logic
def like_post(request, slug):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page', args=[str(slug)]))

def all_bookmark_post(request):
    all_bookmark_post = Post.objects.filter(bookmarks = request.user)
    context = {'all_bookmark_post':all_bookmark_post}
    return render(request, 'app/all_bookmark_post.html', context)

def all_posts(request):
    all_posts = Post.objects.all()
    context = {'all_posts':all_posts}
    return render(request, 'app/all_posts.html', context)