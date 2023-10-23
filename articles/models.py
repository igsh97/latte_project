from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="image", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'제목 : {self.title} 내용 : {self.content}'
    

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 생성될 때 자동으로 넣어줌
    updated_at = models.DateTimeField(auto_now=True) # 수정될 때 자동으로 넣어줌
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.content}'