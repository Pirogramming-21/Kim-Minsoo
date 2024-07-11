from django.shortcuts import render, get_object_or_404, redirect
from .models import Review

def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews
    }
    return render(request, 'review_list.html', context)

def review_detail(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews
    }
    return render(request, 'review_detail.html', context)

def review_create(request):
    if request.method == "POST":
        Review.objects.create(
            title = request.POST["title"],
            director = request.POST["director"],
            stars = request.POST["stars"],
            genre = request.POST["genre"],
            rating = request.POST["rating"],
            runningtime = request.POST["runningtime"],
            content = request.POST["content"],
        )
        return redirect("/movie")
    return render(request, "review_create.html")