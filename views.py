from comment.models import Comment
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from comment.serializers import CommentSerializer
from rest_framework import status
from rest_framework.views import APIView
from comment.utils import get_object
from rest_framework import generics,permissions,serializers
from rest_framework.parsers import FormParser, MultiPartParser

CREATE_SUCCESS = 'created'
UPDATE_SUCCESS = 'updated'
DELETE_SUCCESS = 'deleted'	


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
class CommentList(generics.ListCreateAPIView):
    parser_classes = (FormParser, MultiPartParser)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  
    def perform_create(self, serializer):
        serializer.save(author=self.request.user,is_approved=True)
            

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = (FormParser, MultiPartParser)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]