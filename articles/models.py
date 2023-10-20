# from django.db import models


# # Create your models here.
# class Articles(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     image = models.ImageField(upload_to='post/', null=True, blank=True)
#     created_at = models.DateField(auto_now_add=True) # 생성할때만 추가
#     updated_at = models.DateField(auto_now=True) # 세이브할때마다 갱신
    
#     def __str__(self): # admin페이지에서 타이틀해야함
#         return str(self.title)
    