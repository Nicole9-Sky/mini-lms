from django.shortcuts import render
from django.contrib.auth.decorators import login_required 


# Create your views here.
@login_required
def profile_view(request):
    user_profile = request.user.userprofile
    enrolled_courses = request.user.enrollment_set.all()
    
    return render(request, 'accounts/profile.html', {
        'user_profile': user_profile,
        'enrolled_courses': enrolled_courses
        })