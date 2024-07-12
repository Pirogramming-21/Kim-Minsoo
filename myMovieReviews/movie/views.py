from django.shortcuts import render, redirect
from .models import Review

def review_list(request):
    sort_by = request.GET.get('sort', 'title')  # 기본 정렬은 제목순
    
    if sort_by == 'rating':
        reviews = Review.objects.all().order_by('-rating')  # 별점 높은 순
    elif sort_by == 'runningtime':
        reviews = Review.objects.all().order_by('runningtime')  # 상영 시간 짧은 순
    else:
        reviews = Review.objects.all().order_by('title')  # 제목 오름차순
    
    context = {
        'reviews': reviews,
        'current_sort': sort_by
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
            release_year = request.POST["release_year"],
            director = request.POST["director"],
            stars = request.POST["stars"],
            genre = request.POST["genre"],
            rating = float(request.POST["rating"]),  # float으로 변환
            runningtime = int(request.POST["runningtime"]),  # int로 변환
            content = request.POST["content"],
            poster = request.FILES.get("poster")
        )
        return redirect("/movie")
    return render(request, "review_create.html")

def review_update(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == "POST":
        review.title = request.POST["title"]
        review.release_year = request.POST["release_year"]
        review.director = request.POST["director"]
        review.stars = request.POST["stars"]
        review.genre = request.POST["genre"]
        review.rating = float(request.POST["rating"])  # float으로 변환
        review.runningtime = int(request.POST["runningtime"])  # int로 변환
        review.content = request.POST["content"]  # int 변환 제거
        
        if "poster" in request.FILES:  # 새 포스터 이미지가 업로드된 경우
            review.poster = request.FILES["poster"]

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