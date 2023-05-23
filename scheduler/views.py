from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Classroom , Scheduler , Sessions
from .serializers import ClassroomSerializer,SchedulerSerializer,SessionsSerializer
from document.models import Document
from document.serializers import DocumentSerializer
from subject.serializers import SubjectSerializer
import json
# Create your views here.

class createScheduler(APIView):
    def post(self,request):
    # Lấy dữ liệu 
        classroom_id = request.data.get('classroom_id')
        date = request.data.get('date')
        time_slot = request.data.get('time_slot')
        user_applied = request.data.get('user_applied')
    # Kiểm tra lớp học đã tồn tại chưa, nếu chưa thì tạo mới
        classroom,created = Classroom.objects.get_or_create(room_id=classroom_id)
    # Kiểm tra Validate
        print(Sessions.objects.filter(classroom_id=classroom.id))
        if Sessions.objects.filter(classroom_id=classroom.id, date=date).exists():
            sessions = Sessions.objects.filter(classroom_id=classroom.id, date=date)
            for session in sessions:
                for user in user_applied:
                    if user in session.user_applied:
                        return Response({'message': 'Sessions is not avaiable for user'}, status=status.HTTP_400_BAD_REQUEST)
                if session.time_slot in time_slot :
                    return Response({'message': 'Conflict '}, status=status.HTTP_400_BAD_REQUEST)
            document = Document.objects.get(id=request.data.get('documentId'))
            scheduler = Scheduler.objects.create(classroom=classroom, document=document)
            for time in time_slot:
                session = Sessions.objects.create(classroom=classroom, scheduler=scheduler, user_applied=user_applied, date=date, time_slot=time)
                session.save()
            # session = Sessions.objects.create(classroom=classroom, scheduler=scheduler, user_applied=user_applied, date=date, time_slot=time_slot)
            # session.save()
            scheduler.save()
            return Response({'message': 'Scheduler created successfully'}, status=status.HTTP_201_CREATED)
        else:
            # Tạo sessions mới
            document = Document.objects.get(id=request.data.get('documentId'))
            scheduler = Scheduler.objects.create(classroom=classroom, document=document)
            for time in time_slot:
                session = Sessions.objects.create(classroom=classroom, scheduler=scheduler, user_applied=user_applied, date=date, time_slot=time)
                session.save()
            # session = Sessions.objects.create(classroom=classroom, scheduler=scheduler, user_applied=user_applied, date=date, time_slot=time_slot)
            # session.save()
            scheduler.save()
            return Response({'message': 'Scheduler created successfully'}, status=status.HTTP_201_CREATED)
class ViewSessions(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        user_id = request.GET.get('user_id')
        classrooms = Classroom.objects.all()
        schedulers = Scheduler.objects.all()
        # document = Document.objects.all()
        try:
            sessions = Sessions.objects.filter(date__gte=start_date, date__lte=end_date, user_applied__contains = user_id)
            serializer = SessionsSerializer(sessions, many=True)
            result = []
            for s in serializer.data:
                value= json.loads(json.dumps(s))
                for c in classrooms:
                    # print(c.id)
                    if s["classroom"]==c.id:
                        value["classroom"] = ClassroomSerializer(c).data
                for sc in schedulers:
                    if s["scheduler"]==sc.id:
                        value["scheduler"] = SchedulerSerializer(sc).data
                        value["document"] = DocumentSerializer(sc.document).data
                        value["document"]["subject"] = SubjectSerializer(sc.document.subject).data
                
                
                # value["classroom"] = c.data
                result.append(value)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)