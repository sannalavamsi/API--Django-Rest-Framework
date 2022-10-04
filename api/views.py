
from django.shortcuts import render,get_object_or_404
from .models import Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from rest_framework.views import APIView
from rest_framework import status,viewsets
# Create your views here.

# Function based views
@api_view(['GET'])
def apiOverview(request):
    api_ulrs ={
        'List' : 'task-list/',
        'Detail View' : '/task-detail/<str:pk>/',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>/',
        'Delete' : '/task-delete/<str:pk>/',
    }
    return Response(api_ulrs)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks,many=False)
    return Response(serializer.data)


@api_view(['POST'])
def taskCreate(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def taskUpdate(request,pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def taskDelete(request,pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return Response("Item is sussessfully deleted")

## class based APIView 
# drowback is custom method can not be built like passward change, reset password ,
# forget password,resend password, login , verify password
# so we use 
class TaskViewList(APIView):
    def get(self,request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks,many=True)

        return Response({
            'status' : True,
            'message' : 'task fetched',
            'data' : serializer.data
        })

    def post(self,request):
        try:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : True,
                    'message' : 'task fetched',
                    'data' : serializer.data
                })
            #return Response({'status' : False,'message' : 'invalid data','data' : serializer.errors})
        except Exception as e:
            print(e)
        return Response({
            'status' : False,
            'message' : 'Invalid Data',
        })

# with primary key 
class TaskViewDetail(APIView):
    def get(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task,many=False)
        return Response(serializer.data)


    def delete(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        task.delete()
        return Response({'message' : 'Task Deleted successfully'},status=status.HTTP_204_NO_CONTENT)

    
    def put(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk, format=None):
        task = Task.objects.get(pk=pk)
        serializer = TaskSerializer(task,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ModelViewSet
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    task = Task.objects.all()
    
    