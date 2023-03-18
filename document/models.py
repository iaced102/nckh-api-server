from django.db import models
from account.models import User
from subject.models import Subject
# Create your models here.


class Document(models.Model):
    host = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='host')
    classId = models.CharField(max_length=25)
    sharePermission = models.CharField(max_length=15,default = "onlyMe")
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name='subject', null=True)
    columnDefs = models.TextField(null=True)


class SubTaskDocument(models.Model):
    student = models.ForeignKey(User, related_name="student", on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Document, related_name='owner', on_delete=models.CASCADE)
    value = models.TextField(default="")




# class scheduler(model.model):
#     classroom= ForeignKey(classroom)
#     document = ForeignKey(Document)

# class classroom(model.Model):
#     id phòng


# class sessions:
#     session = 1
#     classroom = ForeignKey(classroom)
#     scheduler = ForeignKey(scheduler, on_delete=models.CASCADE)
#     userApplyed = models.TextField() '[user_id1, user_id2]'

'''
nhằm mục đích
    - khi giảng viên đăng kí lịch thì sẽ config là đăng kí cho môn nào, chọn phòng nào, chọn tiết nào
    - việc phân chia classroom riêng ra thành 1 model sẽ giúp cho usecase là 
        - khi có 1 gv khác đăng kí cái lớp đó thì chỉ cần check thông tin của cái lớp đó
            - hoặc là lấy các session mà có phòng học 1604, tiết học 1,2,3,4 xem có ai đăng kí chưa

    - khi mà 1 user xem lịch thì mình có thể lấy các scheduler mà có host là cái user đó


    các API cần bao gồm
    -tạo lịch học 
        - mã lớp
        - địa điểm
        - thời gian (cả tiết và ngày)
        - danh sách user bị apply cái lịch này 

        - check xem cái classroom đấy đã tồn tại hay chưa, nếu chưa thì thêm vào (khi get, nếu trả ra rỗng thì tức là chưa có -> tạo)
        - check validate 
            - lấy các sessions mà có classroom là cái địa điểm đó
                (sessions.object.filter(classroom_id = mã lớp, và ngày = ngày))
            - lấy tất cả các session có tiết và ngày = ngày
            lặp qua tất cả các session này, xem có session nào mà có userApplyed  chứ một trong những danh sách user bị apply hay không
            - (check xem các tiết gửi đến có cái nào trùng không
                - nếu trùng thì response bad request
                - nếu không trùng thì tạo ra các session có mã lớp và ngày, và tiết, userApplyed = danh sách gửi đi, mặc định thêm cái user mà tạo cái scheuler này vào
        - tạo ra scheduler có classroom = id, document = mã lớp, 





    - usecase 2: xem lịch học
        - ngày bắt đầu, ngày kết thức,
        - user_Id
        
        - lấy ra các session có  ngày bắt đầu <ngày< ngày kết thúc, và có cái userapplyed chứ user_id
            session.object.filter( ngày bắt đầu <ngày< ngày kết thúc, userapplyed chứ user_id)

    - xóa: xóa cái scheuler này
'''