from django.shortcuts import render
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
        data = []
        print(subDocument)
        for doc in DocumentSerializer(document, many=True).data:
            cloneDoc = doc
            # cloneDoc.hostName = doc.host.userNameDisplay
            print(doc["host"])
            host = User.objects.get(id=doc["host"])
            print(host.userNameDisplay)
            cloneDoc["userName"] = host.userName
            cloneDoc["hostName"] = host.userNameDisplay
            data.append(cloneDoc)
        for doc in DocumentSerializer(subDocument, many=True).data:
            cloneDoc = doc
            # cloneDoc.hostName = doc.host.userNameDisplay
            print(doc["host"])
            host = User.objects.get(id=doc["host"])
            print(host.userNameDisplay)
            cloneDoc["userName"] = host.userName
            cloneDoc["hostName"] = host.userNameDisplay
            data.append(cloneDoc)
        return JsonResponse({
                'data': data,
            }, status=status.HTTP_200_OK)
        # return Response('abc abc')

class createDocument(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        # get user by userName = request.user
        user = User.objects.get(userName=request.user)

        
        document =Document.objects.create(host=user,classId=request.data["classId"],sharePermission =request.data["sharePermission"])
        document.save()
        for col in request.data['columnDefs']:
            field = col["field"]
            headerName= col["headerName"]

            if field != 'id':
                for data in request.data["rawData"]:
                    student = data["id"]
                    value = data[field]
                    print(value)    
                    subtask = SubTaskDocument.objects.create(field = field,title = headerName,student = student,owner = document,value = value)
                    subtask.save()
        list = SubTaskDocument.objects.all()
        print(list)
        return Response('asdjf;l')
# req 2:
# viết 1 api get detail của 1 cái doc
#api gửi đi phải có docID
# từ cái model subtaskdocument, lấy tất cả các bản ghi có owner_id = docID
# trả về cái thông tin của doc đó get(id=docID)
class detailDocument(APIView):
    def get(self,request,doc_id):
        document = Document.objects.get(id=doc_id)
        sub_task_documents = SubTaskDocument.objects.filter(owner_id=doc_id)
        serializer = DocumentSerializer(document)
        columnDefField = []
        columnDef = [{"field":"student","headerName":"Ma Sinh Vien"}]
        subTaskDoc = SubTaskDocumentSerializer(sub_task_documents, many=True).data
        for task in subTaskDoc:
            if task["field"] not in columnDefField:
                columnDefField.append(task["field"])
                columnDef.append({"field":task["field"],"headerName":task["title"]})
        ID = []
        rawData = []
        for task in subTaskDoc:
            if task["student"] not in ID:
                ID.append(task["student"])
                rawData.append({"ID":task["student"], task["field"]:task["value"]})
                
            else:
                index = ID.index(task["student"])
                rawData[index][task["field"]]= task["value"]
        return JsonResponse({
            "info": serializer.data,
            "columnDefs":columnDef,
            "rawData":rawData,
            "detail":SubTaskDocumentSerializer(sub_task_documents, many=True).data
        },status=status.HTTP_200_OK)


class EditDocument(APIView):
    def put(self, request, doc_id):
        document = Document.objects.get(id=doc_id)
        host = DocumentSerializer(document).data["host"]
        print(host)
        print(request.user.id)
        if host != request.user.id:
            return JsonResponse({
            "message": "permission denied"
        },status=status.HTTP_400_BAD_REQUEST)
        sub_task_documents = SubTaskDocument.objects.filter(owner_id=doc_id)
        sub_task_serializer = SubTaskDocumentSerializer(sub_task_documents, many=True)
        sub_task_data = sub_task_serializer.data
        for sub_task in sub_task_documents:
            sub_task.delete()
        for col in request.PUT.get('columnDefs', False):
            field = col["field"]
            headerName= col["headerName"]

            if field != 'id':
                for data in request.data["rawData"]:
                    student = data["id"]
                    value = data[field]
                    print(value)    
                    subtask = SubTaskDocument.objects.create(field = field,title = headerName,student = student,owner = document,value = value)
                    subtask.save()
        return JsonResponse({
            "status":"oke",
            "message": f"Deleted {len(sub_task_data)} subtasks for document with id {doc_id}."
        },status=status.HTTP_200_OK)