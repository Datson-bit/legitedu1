from django import forms
from .models import Comment, Reply, Subscriber


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'email', 'author']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text',  'author']


class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    subject = forms.CharField(label='Subject', max_length=200)
    message = forms.CharField(label='Your Message', widget=forms.Textarea)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False,label='Search')


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields= ['email']

