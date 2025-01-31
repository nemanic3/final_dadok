from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
from .models import CustomUser
from .serializers import UserSerializer  # ✅ 시리얼라이저 추가


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            student_id = request.POST.get('student_id')

            # 유효성 검사
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if CustomUser.objects.filter(nickname=nickname).exists():
                return JsonResponse({'error': 'Nickname already exists'}, status=400)
            if CustomUser.objects.filter(student_id=student_id).exists():
                return JsonResponse({'error': 'Student ID already exists'}, status=400)

            # 사용자 생성
            user = CustomUser.objects.create(
                username=username,
                password=make_password(password),  # 비밀번호 암호화
                nickname=nickname,
                email=email,
                student_id=student_id
            )

            return render(request, 'user/signup_success.html', {'user': user})  # ✅ JSON 반환
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        return render(request, 'user/signup.html')


def signup_success(request):
    return render(request, 'user/signup_success.html')


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # 사용자 인증
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            login(request, user)  # ✅ Django 세션 로그인

            # JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return render(request, 'user/login_success.html',{
                "token": access_token
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'user/login.html')

def login_success(request):
    return render(request, 'user/login_success.html')

def logout_user(request):
    logout(request)
    return redirect('/')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response(UserSerializer(user).data)  # ✅ 시리얼라이저 활용



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        user = request.user
        user.delete()  # 현재 로그인된 사용자를 삭제
        return Response({"message": "Account successfully deleted."}, status=204)
    except Exception as e:
        return Response({"error": str(e)}, status=400)



@login_required
def my_page(request):
    return render(request, 'user/mypage.html', {'user': request.user})


def home(request):
    return render(request, 'home.html')
