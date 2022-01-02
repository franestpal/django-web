from django.shortcuts import render, get_object_or_404
from .models import Post, Category


# Create your views here.

def blog(request):
    posts = Post.objects.all()
    return render(request, "blog/food-category.html", {'posts':posts})


def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, "blog/category.html", {'category':category})


def post(request, title): 
    post = get_object_or_404(Post, id=title)
    return render(request, "blog/recetas2.html", {'post':post})

    






