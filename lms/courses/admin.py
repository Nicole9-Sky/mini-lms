from django.contrib import admin
from .models import User, Course, Lesson, Enrollment, Comment, Rating, Bookmark, Category

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Bookmark)
