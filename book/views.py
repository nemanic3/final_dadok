import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def search_books(request):
    """
    - 네이버 API를 이용한 도서 검색
    - GET 요청에서 'query' 파라미터를 받아 검색 수행
    """
    query = request.GET.get("query", "")
    if not query:
        return render(request, "book/search.html", {"error": "검색어를 입력하세요."})

    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": 10}  # 최대 10개 검색 결과 반환

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return render(request, "book/search.html", {"books": data["items"]})
    else:
        return render(request, "book/search.html", {"error": "네이버 API 호출 실패"})


@api_view(['GET'])
def get_book_by_isbn(request, isbn):
    """
    - 리뷰 작성 시 특정 책의 정보를 네이버 API에서 가져옴
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}  # ISBN을 이용한 검색

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["items"]:
            return JsonResponse(data["items"][0])  # 첫 번째 검색 결과 반환
        else:
            return JsonResponse({"error": "책을 찾을 수 없습니다."}, status=404)
    else:
        return JsonResponse({"error": "네이버 API 호출 실패"}, status=500)