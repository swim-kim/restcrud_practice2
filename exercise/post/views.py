#restapi 로 views를 짜기 위한 import

from rest_framework.response import Response
from rest_framework.decorators import api_view

#모델과 시리얼라이저 불러오기
from .models import *
from .serializers import *

from django.shortcuts import get_list_or_404

@api_view(['GET'])
def profile_all(request):
    instances = Profile.objects.all()
    profile_serializer = ProfileSerialier(instances, many=True)
    data = profile_serializer.data
    return Response(data=data)
    
