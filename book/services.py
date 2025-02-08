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
        return data.get("items", [])
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_book_by_isbn_from_naver(isbn):
    """ 네이버 API에서 특정 ISBN으로 책 정보 조회 """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [None])[0]
    except requests.exceptions.RequestException as e:
        return None