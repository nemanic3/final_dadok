import requests
from django.conf import settings

def search_books_from_naver(query, display=10):
    """ 네이버 API를 이용한 도서 검색 """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # ✅ 응답이 정상적인지 확인
        if isinstance(data, dict) and "items" in data and data["items"]:
            return data["items"]  # ✅ 정상적인 리스트 반환
        return []  # ✅ 데이터가 없으면 빈 리스트 반환
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_book_by_isbn_from_naver(isbn):
    """ 특정 ISBN의 책 정보 조회 """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}  # ✅ ISBN 검색을 위해 "query" 사용

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        print("🔍 네이버 API ISBN 조회 응답 데이터:", data)

        if isinstance(data, dict) and "items" in data and data["items"]:
            return data["items"][0]
        return None
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}