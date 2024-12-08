from django.db import models
from apps.devtools.models import DevTool
from PIL import Image

class Idea(models.Model):
    TOOL_CHOICES = [
    ('Django', 'Django'),
    ('Flask', 'Flask'),
    ('React', 'React'),
    ('Vue.js', 'Vue.js'),
    ('Angular', 'Angular'),
    ('Node.js', 'Node.js'),
]

    name = models.CharField(max_length=200, verbose_name="아이디어명")
    image = models.ImageField(upload_to='idea_images/', verbose_name="이미지")
    description = models.TextField(verbose_name="아이디어 설명")
    interest = models.IntegerField(default=0, verbose_name="아이디어 관심도")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록 시간")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 시간")
    starred = models.BooleanField(default=False, verbose_name="찜하기")
    # DevTool과의 연결을 위한 ForeignKey 추가
    devtool = models.ForeignKey(DevTool, on_delete=models.SET_NULL, null=True, blank=True, related_name='ideas')
    expected_tools = models.CharField(
        max_length=20,
        choices=TOOL_CHOICES,
        default='django',
        verbose_name="예상 개발툴"
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)  # 이미지 열기
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)  # 원하는 크기로 조절
            img.thumbnail(output_size)
            img.save(self.image.path)
