from django.shortcuts import render

# Create your views here.



def testhelloworld(request):
    return render(request,'test.html')