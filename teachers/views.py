from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework import viewsets
# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework import permissions
from teachers.models import Teacher, Subject
from teachers.serializers import TeacherSerializer
import requests
import pandas as pd
import os
from teachers.TeacherData import TeacherData
from django.contrib.auth import authenticate, logout, login
from .forms import TeacherForm
from django.views.generic import ListView, View

class TeacherViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

def home_page(request):
    login = False
    if request.user.is_authenticated:
        login = True
    teachers = list()
    response = requests.get('http://localhost:8000/directory/teachers/')
    teachers_list_json = response.json()
    for t in teachers_list_json:
        subjects_obj = t['subjects']
        for s in subjects_obj:
            t_data = TeacherData(
                first_name=t['first_name'],
                last_name=t['last_name'],
                email=t['email'],
                phone_number=t['phone_number'],
                room_number=t['room_number'],
                picture=t['profile_picture'],
                subject=s['name'],
            )
            teachers.append(t_data)
    context = {"teachers": teachers, "login": login}

    return render(request, 'teachers/index.html', context)


def teacher_profile(request, email):
    login = False
    if request.user.is_authenticated:
        login = True
    teacher = Teacher.objects.filter(email=email)[0]
    context = {"teacher": teacher, "login": login}
    return render(request, 'teachers/teacherproflie.html', context)

def load_importer(request):
    login = False
    if request.user.is_authenticated:
        login = True
    if not login:
        return redirect('/directory/home')
    return render(request, 'teachers/importer.html',{"login": login})

def process_import(request):
    data = request.POST
    if data is not None:
        uploaded_file = request.FILES['csv_file']
        if not uploaded_file.name.endswith('.csv'):
            return render(request, 'teachers/importer.html',
                    {"vaildate": "Uplaod vaild file"})
        df = pd.read_csv(uploaded_file)
        df = df.fillna('')
        #importing logic
        for index, row in df.iterrows():
            first_name = row['First Name']
            last_name = row['Last Name']
            pic = row['Profile picture']
            print('yamini  {}'.format(pic))
            if pic == '' or pic is None:
                pic = 'placeholder.jpg'
            email = row['Email Address']
            phone = row['Phone Number']
            room = row['Room Number']
            subjects = row['Subjects taught']
            teach = Teacher()
            teach.first_name = first_name
            teach.last_name = last_name
            teach.profile_picture = pic
            teach.email = email
            teach.phone_number = phone
            teach.room_number = room
            teach.save()
            subject_objs = list()
            if 5 > len(subjects.split(',')) > 0:
                for sub in subjects.split(','):
                    fetch_list = Subject.objects.filter(name=sub)
                    if len(fetch_list) > 0:
                        s_obj = fetch_list[0]
                        subject_objs.append(s_obj)
                    else:
                        s_obj = Subject()
                        s_obj.name = sub
                        s_obj.save()
                        subject_objs.append(s_obj)
                teach.subjects.set(subject_objs)
        #importing logic ends
        response = redirect("/directory/home")
        return response
    else:
        return render(request, 'teachers/loginPage.html', {"csv_file": data["csv_file"],"vaildate": "User Not Authenticated"})

