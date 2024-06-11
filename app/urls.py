from django.urls import path
from django.views.generic import TemplateView

from .views import Home, Blog, About, blog_tags, Scholarship, Contact, Test, blog_detail, Single, ItemListView, search

urlpatterns = [
    path("", Home, name='Home'),
    path("blog/", Blog, name='Blog'),
    path('blog/<int:pk>/',blog_detail, name='view'),
    # path('blog/<int:pk>/add_comment/', add_comment, name='add_comment'),
    # path('comment/<int:pk>/add_reply/', add_reply, name='add_reply'),
    path("about", About, name='About'),
    path("scholarship", Scholarship, name='Scholarship'),
    path("contact", Contact, name='Contact'),
    path("single", Single),
    path('filter/', ItemListView.as_view(), name='item-list'),
    path('tag/<slug:tag_slug>', blog_tags, name='tag'),
    # path("contact-test", Contact_Test, name='Contact'),
    path('success/', TemplateView.as_view(template_name='success_page.html'), name='success'),
    path('search/', search, name='search')

]