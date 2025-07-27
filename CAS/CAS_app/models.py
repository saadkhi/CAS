from django.db import models


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class user_form(models.Model):
    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    GPA = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    resume_pdf = models.FileField(upload_to='resumes/', blank=True, null=True)

    # Resume analysis outcome
    score = models.IntegerField(blank=True, null=True)
    suggestions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name