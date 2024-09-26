from django.shortcuts import render,redirect
import json
from django.http import JsonResponse




def chat_with_gpt(request):
    user_message = request.GET.get('message', '')
    return render(request, "gpttest.html")
    


def home(request):
    # Open and read the JSON data from the

    return redirect("/home")



def test(request):
    c = ''
    if request.method == 'POST':
        n1 = eval(request.POST.get('number1'))
        n2 = eval(request.POST.get('number2'))
        c = n1+n2



    return render(request,'testing.html',{'c':c})
