from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages 



# Create your views here.
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your messages has been sent!')
            return redirect('contact')
        else:
            form = ContactForm()
            
            return render(request, 'contact/contact.html', {'form': form})
        
            
        