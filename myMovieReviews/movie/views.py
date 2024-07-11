from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Review

def review_list(request):
    reviews = Review.objects.all()
    context = {
        'reviews' : reviews
    }
    return render(request, 'review_list.html', context)

def review_detail(request, pk):
    review = Review.objects.get(id=pk)
    context = {
        'review' : review   
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

def review_update(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == "POST":
        review.title = request.POST["title"]
        review.director = request.POST["director"]
        review.stars = request.POST["stars"]
        review.genre = request.POST["genre"]
        review.rating = request.POST["rating"]
        review.runningtime = request.POST["runningtime"]
        review.content = request.POST["content"]

        review.save()

        return redirect(f"/movie/detail/{pk}/")

    context = {
        "review" : review
        }
    return render(request, "review_update.html", context)

def review_delete(request, pk):
    if request.method == "POST":
        review=Review.objects.get(id=pk)
        review.delete()
    return redirect("/movie/")