from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
import requests
from django.conf import settings

### 📌 기존 API (유지) ###
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    """
    리뷰 저장 API (POST)
    네이버 API에서 가져온 책의 정보를 기반으로 리뷰를 저장
    """
    isbn = request.data.get('isbn')  # 책 ISBN 받기
    content = request.data.get('content')
    rating = request.data.get('rating')

    if not isbn or not content or not rating:
        return Response({'error': '모든 필드를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

    # 네이버 API에서 책 정보 가져오기
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["items"]:
            book_info = data["items"][0]  # 첫 번째 검색 결과 사용

            # 리뷰 저장
            review = Review.objects.create(
                user=request.user,
                book_isbn=isbn,  # 기존 book_id가 아닌 isbn 저장
                book_title=book_info['title'],
                book_author=book_info['author'],
                content=content,
                rating=rating
            )

            return Response({
                "message": "리뷰가 저장되었습니다.",
                "review": {
                    "id": review.id,
                    "book_title": review.book_title,
                    "book_author": review.book_author,
                    "content": review.content,
                    "rating": review.rating
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': '책 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': '네이버 API 호출 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_reviews(request):
    """
    전체 리뷰 목록 조회 API (GET)
    """
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

### 📌 HTML 폼 기반 리뷰 작성 ###
@login_required
def review_form(request):
    """
    HTML 기반 리뷰 작성 페이지
    """
    isbn = request.GET.get('isbn')  # GET 요청에서 isbn을 받음

    if not isbn:
        return render(request, "review/review_form.html", {"error": "잘못된 접근입니다."})

    # 네이버 API에서 책 정보 가져오기
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["items"]:
            book_info = data["items"][0]
            return render(request, "review/review_form.html", {"book": book_info})
        else:
            return render(request, "review/review_form.html", {"error": "책을 찾을 수 없습니다."})
    else:
        return render(request, "review/review_form.html", {"error": "네이버 API 호출 실패"})
