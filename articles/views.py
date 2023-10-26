from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework import status

from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, CommentCreateSerializer, CommentSerializer

import requests
import json
import urllib
from PIL import Image




class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        

class ArticleDetailView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(pk=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    def put(self, request, article_id):
        article = Article.objects.get(pk=article_id)

        if article.user != request.user:
            return Response(status=403)

        serializer = ArticleSerializer(article, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, article_id):
        if not request.user.is_authenticated:
            return Response(status=401)
        article = Article.objects.get(pk=article_id)
        if article.user != request.user:
            return Response({ "권한이 없습니다."}, status=403)
        else:
            article.delete()
            return Response({"삭제되었습니다."}, status=204)
    

class CommentView(APIView):
    def post(self, request, article_id):
        serializer = CommentSerializer(data=request.data)   
        if serializer.is_valid():
            serializer.save(article_id=article_id, user=request.user) 
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def get(self, request, article_id):
        comments = Comment.objects.filter(article_id=article_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    
class CommentDetailView(APIView):
    def put(self, request,  comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN) 
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.user != request.user:
            return Response("권한이없습니다.", status=status.HTTP_403_FORBIDDEN) 
        
        comment.delete()
        return Response({"삭제되었습니다."}, status=204)
    
# 이미지 생성
class GenerateImage(APIView):
    def post(self, request):

        
        REST_API_KEY = '893e71a3d65fcf61c29ffc9af35f4e42'

        prompt = request.data.get('prompt', 'dog by gogh')
        negative_prompt = request.data.get('negative_prompt', 'ugly face,low quality,low contrast,draft,amateur,cut off,cropped,frame')
       
        response = self.generate_image(prompt, negative_prompt, REST_API_KEY)

        
        images = response.get("images", [])

        if not images:
            return Response({'error': 'Image generation failed'}, status=status.HTTP_400_BAD_REQUEST)

        
        image_url = images[0].get("image")

        
        image_response = self.fetch_image(image_url)
        return image_response

    def generate_image(self, prompt, negative_prompt, api_key):
        r = requests.post(
            'https://api.kakaobrain.com/v2/inference/karlo/t2i',
            json={
                'prompt': prompt,
                'negative_prompt': negative_prompt
            },
            headers={
                'Authorization': f'KakaoAK {api_key}',
                'Content-Type': 'application/json'
            }
        )

        
        response = json.loads(r.content)
        return response

    def fetch_image(self, image_url):
       
        image = Image.open(urllib.request.urlopen(image_url))
        save_path = './media/image/generate_image.png'  # 저장하려는 경로로 변경
        image.save(save_path, 'PNG') 

        
        image_response = Response()
        image_response['Content-Type'] = 'image/png'
        image_response['Content-Disposition'] = 'inline; filename=image.png'
        image_response.content = image.tobytes()

        return image_response
        