from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from datetime import timedelta
from .models import AddLogs, AddProjects
from .serializers import AddLogsSerializer



def downloadpage(request):
    user = request.GET.get('user')
    sevlevel = request.GET.get('sevlevel')
    time = request.GET.get('time')
    projname = request.GET.get('projname')
    logcont = request.GET.get('logcont')

    #print(user, sevlevel, time, projname, logcount)

    GeneratedString = ''

    kwargs = dict(user=user, sevlevel=sevlevel, time=time, projname=projname, logcont__contains=logcont)
    posts = AddLogs.objects.filter(**{k: v for k, v in kwargs.items() if v != '' and v != None})
    for post in posts:
        line = str(post.user) + ';' + str(post.sevlevel) + ';' + str(post.time) + ';' + str(post.projname) + ';' + str(post.logcont) + '\n'
        GeneratedString += line
        

    response = HttpResponse(GeneratedString, content_type="text/csv")
    response['Content-Disposition'] = 'inline; filename=output.csv'
    return response



class AddLogsViews(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AddLogsSerializer(data=request.data)
        if serializer.is_valid():
            user = request.data.get('user')
            sevlevel = request.data.get('sevlevel')
            time = request.data.get('time')
            projname = request.data.get('projname')
            logcont = request.data.get('logcont')
            posts = AddProjects.objects.filter(project=projname)
            print("serializer valid")
            #poglej da ni kaj none, in da projekt obstaja
            if user and sevlevel and time and projname and logcont and len(posts) != 0:
                serializer.save()
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                 return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/login/')
def overviewpage(request):
    rows = []
    user = ''
    sevlevel = ''
    time = ''
    projname = ''
    logcont = ''
    if request.method == "POST":
        user = request.POST.get('user')
        sevlevel = request.POST.get('sevlevel')
        time = request.POST.get('time')
        projname = request.POST.get('projname')
        logcont = request.POST.get('logcont')
        
        kwargs = dict(user=user, sevlevel=sevlevel, time=time, projname=projname, logcont__contains=logcont)
        posts = AddLogs.objects.filter(**{k: v for k, v in kwargs.items() if v != '' and v != None})
        for post in posts:
            row = {'user':post.user,'sevlevel':post.sevlevel,'time':post.time,'projname':post.projname,'logcont':post.logcont}
            rows.append(row)

                
    return render(request, 'logsoverview.html', {'rows': rows, 'user': user, 'sevlevel': sevlevel, 'time': time, 'projname': projname, 'logcont': logcont})


@login_required(login_url='/login/')
def addprojectpage(request):
    #podatki iz obrazca
    if request.method == "POST":
        user = request.POST.get('user')
        project = request.POST.get('project')
        description = request.POST.get('description')
        #print(user, project, description)
        
        #preglej če projekt že obstaja
        posts = AddProjects.objects.filter(project=project)
        if len(posts) != 0:
            messages.warning(request, 'Project already in database!')
        else:
            if user != '' and project != '' and description != '':
                model = AddProjects(user=user, project=project, description=description)
                model.save()
                messages.success(request, 'Project submission successful.')
            else:
                messages.warning(request, 'Please fill all of the fields!')
            
    return render(request, 'addprojects.html', {})


@login_required(login_url='/login/')
def projectoverviewpage(request):
    data = []
    if request.method == "POST":
        
        project = request.POST.get('project')
        
        if project:
            logs = AddLogs.objects.filter(projname=project)
            print(len(logs))
            #štetje logov zadnjih 24 ur
            logs24 = 0
            #zadnjih 60 min
            logs60m = 0
            #štetje stopenj resnosti
            severity = {"7": 0, "6": 0, "5": 0, "4": 0, "3": 0, "2": 0, "1": 0, "0": 0}
            for log in logs:
                severity[str(log.sevlevel)] += 1
                first = log.time 
                second = timezone.localtime() + timedelta(hours=1)
                print(second - first)
                print("NOW: " + str(second))
                if "day" not in str(second - first):
                    logs24 += 1
                if str(second - first)[0] == "0":
                    logs60m += 1
        #zapnem projekt info in statistiko
            kwargs = dict(project=project)
            posts = AddProjects.objects.filter(**{k: v for k, v in kwargs.items() if v != '' and v != None})
        #posts = AddProjects.objects.filter(project=project)
            for post in posts:
                context = {'user':post.user,'project':post.project, 'description':post.description, 'severity': severity, 'logs24': logs24, 'logs60m': logs60m}
                data.append(context)
                                    
    return render(request, 'projectoverview.html', {'data': data})

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('addprojectpage')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('addprojectpage')
        else:
            return HttpResponse('401 Unauthorized', status=401)
    return render(request, 'login.html', {})

@login_required(login_url='/login/')
def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('loginpage')
    else:
        return redirect('loginpage')
