import requests
from django.conf import settings

def get_book_recommendations(query, display=5):
    """
    네이버 API를 사용하여 입력된 키워드와 관련된 도서를 추천.
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": display}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # 네트워크 오류 발생 시 예외 발생

        data = response.json().get("items", [])
        formatted_data = [
            {
                "title": book["title"],
                "author": book.get("author", "Unknown Author"),
                "publisher": book.get("publisher", "Unknown Publisher"),
                "image": book.get("image", ""),
                "link": book.get("link", ""),
            }
            for book in data
        ]
        return formatted_data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}