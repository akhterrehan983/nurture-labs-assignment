from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt,datetime
from . serializers import *
import requests
from .models import *   
@api_view(['POST'])
def userRegistration(request):
    serialized = UserRegistrationSerializer(data=request.data)
    if serialized.is_valid():
        name = request.data["name"]
        email = request.data["email"]
        serialized.save()
        u = user.objects.get(email=email)
        id = u.id
        payload = {
            'id':u.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        return Response({'JWT Authentication Token':token,'User id':u.id},status=status.HTTP_200_OK)
    else:
        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def userLogin(request):
    if "email" not in request.data:
        return Response({"email field is missing"},status=status.HTTP_400_BAD_REQUEST)
    if "password" not in request.data:
        return Response({"password field is missing"},status=status.HTTP_400_BAD_REQUEST)
    email = request.data["email"]
    password = request.data["password"]
    try:
        u = user.objects.get(email=email,password=password)
        id = u.id
        payload = {
            'id':u.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')
        return Response({'JWT Authentication Token':token,'User id':u.id},status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def addAdvisor(request):
    serializer = addAdvisorSearializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getAdvisor(request,id=None):
    try:
        u = user.objects.get(id=id)
        z = advisor.objects.all()
        x = addAdvisorSearializer(z,many=True)
        return Response(x.data,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','POST'])
def bookAdvisor(request,userId=None,advisorId=None):
    l = callsBooked.objects.all()
    flagUserId = True
    flagAdvisorId = True
    if request.method in ['GET','POST']:
        try:
            userObj = user.objects.get(id=userId)
            try:
                advisorObj = advisor.objects.get(id=advisorId)
                if request.method == 'GET':
                    return Response("User Id and Advisor Id are correct!!!",status=status.HTTP_200_OK)
            except:
                flagAdvisorId = False
                return Response("Wrong Advisor Id!!!",status=status.HTTP_401_UNAUTHORIZED)
        except:
            flagUserId = False
            return Response("Wrong User Id!!!",status=status.HTTP_401_UNAUTHORIZED)
  
    if "dateTime" not in request.data:
        return Response("dateTime field is missing",status=status.HTTP_400_BAD_REQUEST)
    elif request.data["dateTime"] >= datetime.datetime.now():
        dateTime = request.data["dateTime"]
        d = dateTimeSerializer(data=request.data)
        if d.is_valid():
            obj = callsBooked(dateTime=dateTime,adv=advisorObj)
            obj.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response("Wrong dateTime format!!! It should be yy-mm-dd HH:MM",status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("datetime must be greater than the current dateTime!!!",status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def getBookedCalls(request,userId=None):
    try:
        user.objects.get(id=userId)
        adv = advisor.objects.all()
        cbooked = callsBooked.objects.all()
        d = {}
        for i in adv:
            d[i.id] = [i.name,i.photo.url]
        res = []
        for i in cbooked:
            if i.adv.id in d:
                info = d[i.adv.id]
                res.append({"Advisor Id":i.adv.id,"Advisor Name":info[0],"Advisor Profile Pic":info[1],"Booking Time":i.dateTime,"Booking Id":i.id})
        return Response(res,status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)