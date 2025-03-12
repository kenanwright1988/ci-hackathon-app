from django.shortcuts import render
from django.utils import timezone
from .models import *
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from django.utils import timezone
from .models import Challenge

def view_challenges(request):
    challenges = Challenge.objects.all()
    challenge = challenges.first() if challenges.exists() else None
    return render(request, 'view_challenges.html', {'challenge': challenge})