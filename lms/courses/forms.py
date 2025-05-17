from django import forms 
from .models import Comment, Review, Lesson
from django.contrib.auth.models import User
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment 
        fields = ['text']
        fields = ['content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'material', 'video_url']
