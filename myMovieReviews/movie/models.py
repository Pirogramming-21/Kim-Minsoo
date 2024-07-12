from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=100)
    release_year = models.CharField(max_length=10)
    director = models.CharField(max_length=50)
    stars = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    rating = models.FloatField()
    runningtime = models.IntegerField(help_text="러닝타임(분)")
    content = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)

    def get_runningtime_display(self):
        try:
            runningtime = int(self.runningtime)  # 문자열을 정수로 변환
            hours, minutes = divmod(runningtime, 60)
            if hours > 0:
                return f"{hours}시간 {minutes}분"
            else:
                return f"{minutes}분"
        except ValueError:
            return "유효하지 않은 러닝타임"  # 변환 실패 시 에러 메시지 반환