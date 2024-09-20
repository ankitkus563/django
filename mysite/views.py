from django.shortcuts import render
import json
from django.http import JsonResponse


def chat_with_gpt(request):
    user_message = request.GET.get('message', '')
    return render(request, "gpttest.html")
    


def home(request):
    # Open and read the JSON data from the file
    
    with open("C:/Users/Hp/OneDrive/Documents/djangoproject/mysite/media/MOCK_DATA.json", "r" , encoding="utf8") as data:
        json_data = data.read()

    # Convert JSON data to a Python list
    try:
        userdata_list = json.loads(json_data)  # Expecting a list
    except json.JSONDecodeError as e:
        # If JSON decoding fails, return an error response or handle it appropriately
        return render(request, 'error.html', {'error_message': "Error decoding JSON"})

    # Pass the list to the template within a context dictionary
    return render(request, 'index.html', {'userdata_list': userdata_list})



def test(request):
    c = ''
    if request.method == 'POST':
        n1 = eval(request.POST.get('number1'))
        n2 = eval(request.POST.get('number2'))
        c = n1+n2



    return render(request,'testing.html',{'c':c})