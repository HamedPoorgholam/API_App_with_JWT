from django.http import JsonResponse,Http404
from rest_framework.decorators  import api_view
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from api import serializers
from .permisions import IsSuperUserOrReadOnly, IsUserTask
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api import permisions


# we nead python -m pip install django-cors-headers for front and back cominucate
#INSTALLED_APPS = ["corsheaders"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAdminUser] 



# Using generic class-bassed views

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsUserTask]

@api_view(['POST'])
def Registraion(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            user=serializer.save()
            data['massage']="Registeraion Was Successfull!"
            data['token']=Token.objects.get(user=user).key

        return Response(data)    

# Using viewset

class TaskViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
    def retrieve(self, request, pk=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)    


#Function Base API-viwes!!!!!!!!

# @api_view(['GET','POST'])
# def task_list(request, format = None):


#     if request.method == 'GET':
#             tasks = Task.objects.all()
#             serializer = TaskSerializer(tasks, many=True)
#             return Response(serializer.data)
#     elif request.method == 'POST':  
#             serializer = TaskSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)  
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

# @api_view(['GET','PUT','DELETE'])
# def task_detail(request, pk):

#     try:
#         task = Task.objects.get(id=pk)
#     except Task.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = TaskSerializer(instance=task,data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         task.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)        


# Using APIView Class

# class TaskList(APIView):

#     def get(self, request, fromat = None):
#         tasks = Task.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

#     def post(self, request, format = None):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

# class TaskDetail(APIView):
#     def get_object(self, pk):
#         try:
#              return Task.objects.get(pk=pk)
#         except Task.DoesNotExist: 
#              raise Http404  

#     def get(self, request, pk, fromat = None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)

#     def put(self, request, pk, format = None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_204_NO_CONTENT)   
    
#     def delete(self,  request, pk, fromat = None):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# Using mixins

# class TaskList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class TaskDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)        






