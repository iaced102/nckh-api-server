from django.urls import path
from django.urls import path, include
from .views import createDocument,getListDocumentForUser,detailDocument,EditDocument

urlpatterns = [
    path('create', createDocument.as_view(), name='document-create'),
    path('getList',getListDocumentForUser.as_view(), name='document-list'),
    path('detail/<int:doc_id>',detailDocument.as_view(), name='document-detail'),
    path('document/edit/<int:doc_id>',EditDocument.as_view(), name='document-edit'),
    path('document/<int:doc_id>',detailDocument.as_view(), name='document-detail'),
    
]
