import random

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from eduweb import settings
from django.conf import settings

from .models import Blogs, Comment, Ad
from .forms import CommentForm, ReplyForm, ContactForm, SearchForm, SubscriptionForm
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.core.mail import send_mail
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage


def get_random_add():
    ads= Ad.objects.all()
    if ads.exists():
        return random.choice(ads)
    return None



def Home(request, ):
    latest = Blogs.objects.all().order_by('-id')[:6].annotate(num_comments=Count('comments'))
    carousel = Blogs.objects.all().order_by('-id')[:4].annotate(num_comments=Count('comments'))
    old = Blogs.objects.all()[:8].annotate(num_comments=Count('comments'))
    footer= Blogs.objects.all().order_by('-id')[:3].annotate(num_comments=Count('comments'))
    trending = Blogs.objects.all().order_by('-id')[:6].annotate(num_comments=Count('comments'))
    ad= get_random_add()

    return render(request, 'index.html', {'carousel': carousel, 'latest': latest, 'old': old, 'footer':footer, 'trending':trending, 'ad':ad })


def blog_tags(request, tag_slug):
    tag_blogs = Blogs.objects.filter(tags__slug=tag_slug)
    return render(request, 'tag.html', {'tags': tag_blogs, 'tag_slug': tag_slug})


def search(request):
    query= request.GET.get('query')
    # form= SearchForm()
    results = []
    if query:
        # form = SearchForm(request.GET)
        # if form.is_valid():
        #     query = form.cleaned_data['query']
            results = Blogs.objects.filter(title__icontains=query) | Blogs.objects.filter(tags__name__icontains=query)
    return render(request, 'search.html', {'query':query, 'results': results})

def blog_detail(request, pk):
    trending = Blogs.objects.all().order_by('-id')[:6]
    Blog = get_object_or_404(Blogs, pk=pk)
    num_comments = Blog.comments.count()
    ad= get_random_add()

    if not hasattr(Blog, 'view_count'):
        Blog = Blogs.objects.get(pk=pk)

    Blog.view_count += 1
    Blog.save()

    comments = Comment.objects.filter(blog=Blog)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = Blog
            comment.save()
            return redirect('view', pk=pk)
    else:
        form=CommentForm()

    return render(request, 'single.html', {'Blog': Blog, 'comments': comments, 'trending':trending, 'ad':ad, 'form': form, 'num_comments':num_comments})


#
# def add_comment(request, pk):
#     Blog = Blogs.objects.get(pk)
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             # comment.author = request.user
#             comment.post = Blog
#             comment.save()
#     return redirect('view',pk)
#
# def add_reply(request, pk):
#     comment = Comment.objects.get(pk=pk)
#     if request.method == 'POST':
#         reply_form = ReplyForm(request.POST)
#         if reply_form.is_valid():
#             reply = reply_form.save(commit=False)
#             reply.author = request.user
#             reply.comment = comment
#             reply.save()
#     return redirect('view', pk=comment.blog.pk)


def Blog(request):
    post = Blogs.objects.all().order_by('-id')[:].annotate(num_comments=Count('comments'))
    paginator = Paginator(post, 10)
    page = request.GET.get('page')
    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'post': paginated_posts})


def About(request):
    return render(request, 'About.html')


def Scholarship(request):
    return render(request, 'scholarship.html')


def Single(request):
    return render(request, 'single.html')


def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email=  form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject,
                f"Message from {name} <{email}>: \n\n{message}",
                settings.EMAIL_HOST_USER,
                ['semescot@gmail.com'],
                # fail_silently= False
            )
            return redirect('success')
    else:
          form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def subscribe(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for subscribing')
            return redirect('Home')
        else:
            messages.error(request, "There was an error with your subscription")
    else:
        form = SubscriptionForm()
    return render(request,'subscribe.html', {'form':form})

from django.core.mail import send_mail

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save()
            send_mail(
                'LEGIT EDU: Subscription Confirmation',
                'Thank you for subscribing to our newsletter!',
                'semescot@gmail.com',
                [subscriber.email],
                fail_silently=False,
            )
            messages.success(request, 'Thank you for subscribing!')
            return redirect('home')
        else:
            messages.error(request, 'There was an error with your subscription.')
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})
#
# def send_email(request):
#     subject = 'Subject of the Email'
#     message = 'This is the message body.'
#     from_email = 'your-email@example.com'
#     recipient_list = ['recipient@example.com']
#
#     send_mail(subject, message, from_email, recipient_list)
#     # email.attach_file('/path/to/attachment.pdf')
#
#     send_email.send()
#
#     # Add any necessary logic or response here


# views.py TESTING
from django.views.generic import ListView
from .models import Item


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = Item.objects.all()
        keyword = self.request.GET.get('keyword')
        category = self.request.GET.get('category')

        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        if category:
            queryset = queryset.filter(category=category)

        return queryset
