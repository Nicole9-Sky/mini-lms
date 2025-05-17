from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_tutor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='courses_user_groups',  # Give it a unique name
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='courses_user'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='courses_user_permissions',  # Give it a unique name
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='courses_user'
    )
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.course.title}"

class Lesson(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    video_url = models.URLField(null=True, blank=True)
    material = models.FileField(upload_to='lesson_materials/', null=True, blank=True)
    crated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
class Comment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.student.username} on {self.lesson.title}"
    
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    

class Rating(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 7)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} rated {self.course.title} with {self.rating}"

class Bookmark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="bookmarks", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="bookmarks", null=True, blank=True)

    def __str__(self):
        if self.lesson:
            return f"{self.student.username} bookmarked {self.lesson.title}"
        return f"{self.student.username} bookmarked {self.course.title}"
    
