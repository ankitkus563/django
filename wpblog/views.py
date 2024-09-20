from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Post, User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import os
import json
from django.conf import settings


# Create your views here.
def category(request):
    if request.method == 'POST':
        catname = request.POST.get("catname")
        description = request.POST.get("description")
        
        # Create a new Category instance
        category = Category(name=catname, description=description)
        
        # Optionally set the slug if you have some logic to generate it
        category.slug = catname.lower().replace(' ', '-')
        
        # Save the instance to the database
        category.save()
    categories = Category.objects.all()

    return render(request, 'category.html',{"categories":categories})

def post(request):
    if request.method =="POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")  # Get the category ID from the dropdown
        category = Category.objects.get(id=category_id)  # Fetch the category object
        post = Post(title=title, content=content, category=category)
        post.save()
    categories = Category.objects.all()  # Get all categories
    posts = Post.objects.all()
    
    return render(request, 'post.html', {"posts": posts, "categories": categories})


def home(request):
    
    posts = Post.objects.all()
    
    return render(request,'home.html',{"posts":posts})


def users(request):
    
    if request.method =="POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        email = request.POST.get("email")
        user = User(name=name, username=username, email=email)
        user.save()
    users = User.objects.all()   
    return render(request,'user.html',{"users":users})

def deleteuser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        items = data.get('items', []) 
        users_to_delete = User.objects.filter(id__in=items)
        users_to_delete.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
def deletepost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        items = data.get('items', []) 
        # Perform bulk deletion
        posts_to_delete = Post.objects.filter(id__in=items)
        deleted_count, _ = posts_to_delete.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        

def deletecategory(request,category_id):
    if request.method == "DELETE":
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({'message': 'Category deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def settingspage(request):

    return render(request, 'settings.html')




def importsettings(request):
    print("Request method:", request.method)
    if request.method == "POST":
        item_type = request.POST.get("item_type")
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Check if the uploaded file is a JSON file
            if not uploaded_file.name.endswith('.json'):
                return HttpResponse("Invalid file type. Please upload a JSON file.")

            # Ensure the media directory exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            try:
                with open(file_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                # Optional: You can read and validate the JSON file here
                with open(file_path, 'r',encoding='utf-8') as json_file:
                    if item_type == "users":
                      json_data = json.load(json_file)
                      for data in json_data:
                        email = data["email"]
                        username = email.split('@')[0]
                        name = f"{data['first_name']} {data['last_name']}"
                        user = User(name=name, username=username, email=email)
                        user.save()
                    elif item_type == "posts":
                      json_data = json.load(json_file)
                      for data in json_data:
                        title = data["title"]
                        post = data["post"]
                        newpost = Post(title=title, content=post)
                        newpost.save()

                       # This will raise an error if the JSON is invalid
                                     

                return render(request, 'settings.html', {'message': "File uploaded and saved successfully!"})
            except json.JSONDecodeError:
                return HttpResponse("Error: The uploaded file is not a valid JSON.")
            except Exception as e:
                return HttpResponse(f"Error saving file: {e}")
        else:
            return HttpResponse("No file uploaded.")
    return render(request, 'settings.html')  # Adjust the template as needed

def postview(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request,"postview.html",{"post":post})


def editpost(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    categories = Category.objects.all()
    return render(request,"editpost.html",{"post":post,"categories":categories})


def savepost(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        post.category = category
        post.save()
    return render(request,"postview.html",{"post":post})


def edituser(request,user_id):
    user = get_object_or_404(User, id=user_id)
    users = User.objects.all()
    if request.method == "POST":
        user.name = request.POST.get('name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('/users')
    return render(request,"edituser.html",{"users": users, "iuser": user})