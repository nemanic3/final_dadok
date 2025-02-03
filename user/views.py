from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import UserSerializer

### ✅ 회원가입 (POST)
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 받기
            username = data.get('username')
            password = data.get('password')
            nickname = data.get('nickname')
            email = data.get('email')

            # ✅ 유효성 검사
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            if CustomUser.objects.filter(nickname=nickname).exists():
                return JsonResponse({'error': 'Nickname already exists'}, status=400)

            # ✅ 사용자 생성
            user = CustomUser.objects.create(
                username=username,
                password=make_password(password),  # 비밀번호 암호화
                nickname=nickname,
                email=email,
            )

            return JsonResponse({
                "message": "Signup successful!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "nickname": user.nickname,
                    "email": user.email,
                }
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

### ✅ 로그인 (POST) - JWT 토큰 발급
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # ✅ 사용자 인증
            user = authenticate(username=username, password=password)
            if user is None:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

            # ✅ JWT 토큰 발급
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return JsonResponse({
                "message": "Login successful!",
                "token": access_token
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

### ✅ 로그아웃 (POST) - JWT 사용 시 클라이언트에서 토큰 삭제
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({"message": "Successfully logged out."}, status=200)

### ✅ 현재 로그인한 사용자 정보 조회 (GET)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response(UserSerializer(user).data)

### ✅ 회원 탈퇴 (DELETE)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        user = request.user
        user.delete()
        return Response({"message": "Account successfully deleted."}, status=204)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
