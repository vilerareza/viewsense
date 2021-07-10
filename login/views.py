from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.

def show_login(request):

    #check if logout
    try:
        status = request.GET['status']
        if status == 'logout':
            logout(request)
    
    finally:    
        try: 
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                #authenticated
                login(request, user)
                return HttpResponseRedirect('../dashboard')
                
            else:
                #not authenticated
                return render(request, 'login/index.html')
        
        except:
            #new login request
            return render(request, 'login/index.html')
        

