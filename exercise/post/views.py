#restapi 로 views를 짜기 위한 import

from rest_framework.response import Response
from rest_framework.decorators import api_view

#모델과 시리얼라이저 불러오기
from .models import *
from .serializers import *

from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
def profile_list_create(request):
    if request.method == 'GET' : 
        instances = Profile.objects.all()
        profile_serializer = ProfileSerializer(instances, many=True)
        data = profile_serializer.data
        return Response(data=data)
    elif request.method == 'POST':
        new_profile = ProfileSerializer(data=request.data)
        if new_profile.is_valid(raise_exception=True):
            new_profile.save()
            return Response(data=new_profile.data)

@api_view(['GET', 'POST'])
def post_list_create(request):
    if request.method == 'GET':
        instances = Post.objects.all()
        serializers = PostSerializer(instances, many=True)
        return Response(data=serializers.data)
    
    elif request.method == 'POST':
        post_serializer = PostSerializer(data=request.data)
        if post_serializer.is_valid(raise_exception=True):
            #serializer.save()를 하면 DB가 저장이 되지만, Tag필드가 비어있는 채로 저장이 된다
            post_serializer.save()
            #따라서 serializer.data 안에 담긴 id값을 통해 방금 저장한 post를 쿼리셋 형태로 불러온다.
            post = get_object_or_404(Post, id = post_serializer.data['id'])
            #tag_list 안에 해시태그들만 모아놓기
            content = request.data['content']
            words = content.split(' ')
            tag_list = []
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            #해시태그가 들어있는 리스트를 하나씩 돌면서
            for t in tag_list:
                #기존에 같은 태그가 있으면 걔를 찾아서 쓰고
                try:
                    tag = get_object_or_404(Tag, name=t)
                #없으면 태그를 새로 만든다
                except:
                    tag = Tag(name=t)
                    tag.save()
                #해당 post에 태그 추가. ManyToManyField는 add()함수를 이용해서 추가한다.
                post.tag.add(tag)
            #post저장. 위의 post_serializer.save()는 시리얼라이저를 통해 저장한 것이고
            #post.save()는 쿼리셋을 통해 저장한 것이다.
            #DB에 저장되는 형태는 같지만, 두가지 방법으로 저장할 수 있다는 것을 알아두자
            post.save()
            return Response(data=PostSerializer(post).data)

@api_view(['GET','PATCH','DELETE'])
def post_rud(request, post_id):
    instance = get_object_or_404(Post, pk=post_id)
    if request.method == 'GET':
        serializer = PostSerializer(instance)
        data = serializer.data
        writer = get_object_or_404(Profile, pk=serializer.data['writer'])
        data['writer'] = ProfileSerializer(writer).data
        return Response(data=data)
    elif request.method == 'PATCH':
        serializer = ProfileSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        instance.delete()
        data = {
            'deleted Post ID' : {post_id}
        }
        return Response(data)
    elif request.method =='PATCH':
        #PATCH 메소드를 쓰기 때문에 기존의 post db를 가져와서 요청받은 JSON 을 입힙니다. 부분 수정 가능.
        post_serializer = PostSerializer(instance=instance, data=request.data, partial=True)
        if post_serializer.is_valid(raise_exception=True):
            post_serializer.save()
            post = get_object_or_404(Post, id = post_serializer.data['id'])
            content = request.data['content']
            words = content.split(' ')
            tag_list = []
            for w in words:
                if w[0] == '#':
                    tag_list.append(w[1:])
            for t in tag_list:
                try:
                    tag = get_object_or_404(Tag, name=t)
                except:
                    tag = Tag(name=t)
                    tag.save()
                post.tag.add(tag)
            post.save()
            #응답값에 writer정보 포함(GET방식과 동일)
            serializer = PostSerializer(post)
            data = serializer.data
            writer = get_object_or_404(Profile, pk = serializer.data['writer'])
            data['writer'] = ProfileSerializer(writer).data
            return Response(data=data)