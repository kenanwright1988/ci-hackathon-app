from django.shortcuts import render
from django.utils import timezone
from .models import *

def view_challenges(request):
    challenge = Challenge.objects.get(published_date__lte=timezone.now(), due_date__gte=timezone.now())
    return render(request, 'view_challenges.html' , {'challenge': challenge})