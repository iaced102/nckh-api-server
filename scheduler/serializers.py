from rest_framework import serializers
from .models import Classroom,Scheduler,Sessions

class SchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = ['classroom_id', 'document', 'date', 'time_slot', 'user_applied']
class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'
class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'
            
    