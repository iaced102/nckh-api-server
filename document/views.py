from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializers import DocumentSerializer
from rest_framework.response import Response
from rest_framework import status
from account.models import User,createAccount
from document.models import Document,SubTaskDocument
from rest_framework import permissions
from django.db.models import Q
from django.http import JsonResponse
from .serializers import DocumentSerializer, SubTaskDocumentSerializer
from subject.models import Subject
from scheduler.models import Scheduler,Sessions
from scheduler.serializers import SessionsSerializer


from rest_framework.views import APIView
# Create your views here.
from rest_framework.authentication import SessionAuthentication


# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         pass

class getListDocumentForUser(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        user = User.objects.get(userName=request.user)
        is_staff = request.user.is_staff
        print(user.is_staff)
        if is_staff:
            subDocument = Document.objects.filter( sharePermission__in=['staff_only', 'all'])
        else:
            subDocument = Document.objects.filter( sharePermission='all')
        # check xem thằng user này có phải là staff hay không
        #nếu thằng này là staff thì sẽ lấy host_id=user, perrmission = staffonly, permission = all
        # nếu thằng này không phải staff thì sẽ lấy host_id = user permission = all 
        document = Document.objects.filter(host_id=user)
        #   
        id = []
        data = []
        for doc in DocumentSerializer(document, many=True).data:
            if doc['id'] not in id:
                id.append(doc['id'])
                cloneDoc = doc
                host = User.objects.get(id=doc["host"])
                cloneDoc["userName"] = host.userName
                cloneDoc["hostName"] = host.userNameDisplay
                cloneDoc.pop('columnDefs')
                data.append(cloneDoc)
        for doc in DocumentSerializer(subDocument, many=True).data:
            if doc['id'] not in id:
                id.append(doc['id'])
                cloneDoc = doc
                host = User.objects.get(id=doc["host"])
                cloneDoc["userName"] = host.userName
                cloneDoc["hostName"] = host.userNameDisplay
                cloneDoc.pop('columnDefs')
                data.append(cloneDoc)
        for doc in data:
            subjectId = doc["subject"]
            try:
                subject = Subject.objects.get(id = subjectId)
                doc["subject"] = getattr(subject, subject._meta.get_field("name").attname)
            except Subject.DoesNotExist:
                subject = None
                doc["subject"] = ""
            # subject = Subject.objects.get(id = subjectId)
            # print(subject)
            
        return JsonResponse({
                'data': data,
            }, status=status.HTTP_200_OK)
        # return Response('abc abc')

class createDocument(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # get user by userName = request.user
        user = User.objects.get(userName=request.user)
        sharePermission = request.data["sharePermission"]
        if  sharePermission =="":
            sharePermission = "onlyMe"
        subject = Subject.objects.get(id=request.data["subjectId"])
        document =Document.objects.create(host=user,sharePermission =sharePermission, columnDefs='''{"columnDefs":'''+json.dumps(request.data["columnDefs"])+'}',classId = request.data.get('classId'), subject=subject)
        document.save()
        for col in request.data['rawData']:
            createAccount(col["id"], col["userNameDisplay"])
            user = User.objects.get(userName=col["id"])
            subTask = SubTaskDocument.objects.create(student = user, owner = document, value = col)
        return Response('asdjf;l')
class detailDocument(APIView):
    def get(self,request,doc_id):
        document = Document.objects.get(id=doc_id)
        sub_task_documents = SubTaskDocument.objects.filter(owner_id=doc_id)
        serializer = DocumentSerializer(document)
        columnDef = json.loads(serializer.data["columnDefs"].replace("'",'"'))
        subTaskDoc = SubTaskDocumentSerializer(sub_task_documents, many=True).data
        rawData = []
        for task in subTaskDoc:
            rawData.append(json.loads(task['value'].replace("'",'"')))
        scheduler = Scheduler.objects.filter(document_id =doc_id)
        session = []
        for s in scheduler:
            se = Sessions.objects.filter(scheduler_id=s.id)
            for ses in se:
                session.append(SessionsSerializer(ses).data)
        return JsonResponse({
            "scheduler":list(scheduler.values()),
            "session":session,
            "info": serializer.data,
            "columnDefs":columnDef['columnDefs'],
            "rawData":rawData,
            "detail":SubTaskDocumentSerializer(sub_task_documents, many=True).data
        },status=status.HTTP_200_OK)


class EditDocument(APIView):
    def put(self, request, doc_id):
        document = Document.objects.get(id=doc_id)
        host = DocumentSerializer(document).data["host"]
        if host != request.user.id:
            return JsonResponse({
            "message": "permission denied"
        },status=status.HTTP_400_BAD_REQUEST)
        sub_task_documents = SubTaskDocument.objects.filter(owner_id=doc_id)
        sub_task_serializer = SubTaskDocumentSerializer(sub_task_documents, many=True)
        sub_task_data = sub_task_serializer.data
        document.columnDefs ='''{"columnDefs":'''+json.dumps(request.data["columnDefs"])+'}'
        document.save()
        for raw in request.data["rawData"]:
            createAccount(raw["id"], raw["userNameDisplay"])
            user = User.objects.get(userName=raw["id"])
            sub_task = SubTaskDocument.objects.filter(owner_id=doc_id,student_id=user.id)
            if len(sub_task)==0:
                subTask = SubTaskDocument.objects.create(student = user, owner = document, value = raw)
                subTask.save()
            else:
                subTask = SubTaskDocument.objects.get(owner_id=doc_id,student_id=user.id)
                subTask.value = raw
                subTask.save()
            
        return JsonResponse({
            "status":"oke",
            "message": f"Deleted {len(sub_task_data)} subtasks for document with id {doc_id}."
        },status=status.HTTP_200_OK)
    
