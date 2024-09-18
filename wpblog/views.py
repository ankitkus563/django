from django.shortcuts import render
from django.http import HttpResponse
from .models import Category, Post, User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

def deleteuser(request,user_id):
    if request.method == "DELETE":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        
def deletepost(request,post_id):
    if request.method == "DELETE":
        user = get_object_or_404(Post, id=post_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
        