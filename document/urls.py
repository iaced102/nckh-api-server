from django.urls import path
from django.urls import path, include
from .views import createDocument,getListDocumentForUser,detailDocument

urlpatterns = [
    path('create', createDocument.as_view(), name='document-create'),
    path('getList',getListDocumentForUser.as_view(), name='document-list'),
    path('document/<int:doc_id>/',detailDocument.as_view(), name='document-detail'),
]
