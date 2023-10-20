# from django.shortcuts import render

# # Create your views here.


# class ArticleView(APIView):
#     def get(self, request):
#         articles = Articles.objects.all()
#         serializer = ArticleListSerializer(articles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
        
#     def post(self, request): # 게시글 작성
#         serializer = ArticleCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             print(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)