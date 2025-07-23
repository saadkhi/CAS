from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber

# Create your views here.

def home_view(request):
    return render(request, "website/home.html")

def resume_advisor_view(request):
    return render(request, "website/resume_advisor.html")

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Save email if not already subscribed
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                # Send confirmation email
                send_mail(
                    'CAS Subscription',
                    'You subscribed the CAS notifications',
                    '21b-066-se@students.uit.edu',
                    [email],
                    fail_silently=True,
                )
                messages.success(request, 'Subscribed successfully!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Invalid email address.')
    return redirect('/')