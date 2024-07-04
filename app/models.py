from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

TAG_CHOICES = [
    ('University', 'University'),
    ('Jamb', 'Jamb'),
    ('Education', 'Education'),
    ('News', 'News'),
    ('Science', 'Science'),
    ('Admission', 'Admission')

]


class Blogs(models.Model):
    img_url = models.CharField(max_length=2083, default="")
    title = models.CharField(max_length=1000)
    authour = models.CharField(max_length=500)
    desc = models.CharField(max_length=500, default="")
    authour_img = models.CharField(default="", max_length=2084)
    tags = TaggableManager()
    body = RichTextField(blank=True, null=True)
    date = models.DateField()
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blogs, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.CharField(max_length=50)
    text = models.TextField()
    email = models.EmailField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    # def get_absolute_url(self):
    #     return reverse('view', args=(str(self.slug)))

class Ad(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ads/')
    url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Subscriber(models.Model):
    email= models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  self.email
class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
