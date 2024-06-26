from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from eduweb import settings
from django.conf import settings

from .models import Blogs, Comment
from .forms import CommentForm, ReplyForm, ContactForm, SearchForm
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.core.mail import send_mail


def Home(request, ):
    latest = Blogs.objects.all().order_by('-id')[:6]
    carousel = Blogs.objects.all().order_by('-id')[:4]
    old = Blogs.objects.all()[:8]
    footer= Blogs.objects.all().order_by('-id')[:3]
    trending = Blogs.objects.all().order_by('-id')[:6]
    return render(request, 'index.html', {'carousel': carousel, 'latest': latest, 'old': old, 'footer':footer, 'trending':trending })


def blog_tags(request, tag_slug):
    tag_blogs = Blogs.objects.filter(tags__slug=tag_slug)
    return render(request, 'tag.html', {'tags': tag_blogs, 'tag_slug': tag_slug})


def search(request):
    form= SearchForm()
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Blogs.objects.filter(title__icontains=query) | Blogs.objects.filter(tags__name__icontains=query)
    return render(request, 'search.html', {'form':form, 'results': results})

def blog_detail(request, pk):
    trending= Blogs.objects.all()
    Blog = get_object_or_404(Blogs, pk=pk)

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

    return render(request, 'single.html', {'Blog': Blog, 'comments': comments, 'trending':trending, 'form': form})


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

def Test(request):
    return render(request, 'search.html')


def Blog(request):
    return render(request, 'category.html')


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
                f"{subject} from {name}",
                message,
                email,
                [settings.EMAIL_HOST_USER]
            )
            return redirect('success')
    else:
          form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def send_email(request):
    subject = 'Subject of the Email'
    message = 'This is the message body.'
    from_email = 'your-email@example.com'
    recipient_list = ['recipient@example.com']

    send_mail(subject, message, from_email, recipient_list)
    # email.attach_file('/path/to/attachment.pdf')

    send_email.send()

    # Add any necessary logic or response here


# views.py
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
