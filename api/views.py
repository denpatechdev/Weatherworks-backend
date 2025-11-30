from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app.models import Comment, Like
from api import tools

# Create your views here.
@api_view(['GET'])
def get_comments(req, area: str) -> Response:
    comments = Comment.objects.filter(area=area)
    comments_arr = []
    for c in comments:
        comments_arr.append({
            'id': c.pk,
            'area': c.area,
            'contents': c.contents,
            'ip': c.ip,
            'likes': Like.objects.filter(comment=c).count()
        })
    return Response({'comments': comments_arr})

@api_view(['POST'])
def create_comment(req, area: str) -> Response:
    if area is None or len(area) < 1:
        return Response({'message': 'Area field is empty or null'}, status=status.HTTP_400_BAD_REQUEST)
    contents = req.data.get('contents')
    if contents is None or len(contents) < 1:
        return Response({'message': 'Contents field is empty or null.'}, status=status.HTTP_400_BAD_REQUEST)
    ip = tools.get_ip(req)
    comment = Comment.objects.create(area=area, contents=contents, ip=ip)
    return Response({
        'id': comment.pk,
        'area': area,
        'contents': contents,
        'ip': ip,
        'likes': 0
    })

@api_view(['DELETE'])
def delete_comment(req, comment_id: int) -> Response:
    user: User = req.user
    if user.is_authenticated and (user.is_staff or user.is_superuser):
        if comment := Comment.objects.filter(pk=comment_id):
            deleted_comment_data = {}
            deleted_comment_data['area'] = comment[0].area
            deleted_comment_data['contents'] = comment[0].contents
            deleted_comment_data['ip'] = comment[0].ip
            comment[0].delete()
            return Response(deleted_comment_data)
        else:
            return Response({'message': 'Comment not found'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'You do not have authorization to delete comments.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
def like_comment(req, comment_id: int) -> Response:

    ip = tools.get_ip(req)
    comment = Comment.objects.get(pk=comment_id) if Comment.objects.filter(pk=comment_id).exists() else None
    if req.method == 'POST':
        if not comment:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Like.objects.filter(comment=comment, ip=ip).exists():
            like = Like.objects.create(comment=comment, ip=ip)
            return Response({
                'id': like.pk,
                'ip': ip,
                'comment': comment.pk
            })
        else:
            return Response({'message': 'Comment already liked.'}, status=status.HTTP_400_BAD_REQUEST)
    elif req.method == 'DELETE':
        if not comment:
            return Response({'message': 'Comment not found.'}, status=status.HTTP_400_BAD_REQUEST)
        if Like.objects.filter(comment=comment, ip=ip).exists():
            like = Like.objects.get(comment=comment, ip=ip)
            deleted_like_data = {
                'id': like.pk,
                'ip': like.ip,
                'comment': comment.pk
            }
            Like.objects.get(comment=comment, ip=ip).delete()
            return Response(deleted_like_data)
        else:
            return Response({'message': 'Comment already not liked.'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response()

@api_view(['POST'])
def register_user(req):
    username = req.data.get('username')
    email = req.data.get('email')
    password = req.data.get('password')

    if User.objects.filter(username=username):
        return Response({'message': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    if user:
        login(req, user)
        return Response({'message': f'User {username} successfully registered.'})
    else:
        return Response({'message': f'An error occured during registration'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(req):
    username = req.data.get('username')
    password = req.data.get('password')

    user = authenticate(req, username=username, password=password)

    if user is not None:
        login(req, user)
        return Response({'message': f'Succesfully logged in as {username}.'})
    else:
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)