from django.shortcuts import render
from django.http import HttpResponse

from .forms import LoginForm

# Create your views here.
def index(request):
    form = LoginForm()
    return render (request, 'dashboard/index.html', {'form': form} )
