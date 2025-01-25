import requests
import json
import time
from login import *


# Если есть текст ответа, от запускает функцию для отправки ответа на вопрос
def send_answer(from_mail: str, subject_tema: str, content_telo: str, cookie: str):
    if content_telo:
        print(f"По API ОТВЕТ id: {subject_tema} текст: '{content_telo}'")
        return answer_question(subject_tema, content_telo, cookie)  # Отправляем ответ
    else:
        print(f"По API НЕ отправляю.")
        return None  # Ничего не отправляем, если нет текста ответа


# URL для API запроса
url = "https://seller.ozon.ru/api/review/comment/create"


# Функция для отправки ответа через API
def answer_question(id: str, text: str, cookie: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru",
        "Content-Type": "application/json",
        "x-o3-app-name": "seller-ui",
        "x-o3-language": "ru",
        "x-o3-company-id": company_id,
        "x-o3-page-type": "review",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "cookie": cookie,
    }

    body = {
        "review_uuid": id,
        "text": text,
        "company_type": "seller",
        "company_id": company_id,
    }

    # Попытки отправки запроса (до 3-х раз)
    for attempt in range(3):
        try:
            response = requests.post(url, json=body, headers=headers)
            print(
                f"Запрос отправлен статус-код: {response.status_code}. Ответ json: {response.json()}"
            )
            break  # Если запрос успешен, выходим из цикла
        except requests.exceptions.RequestException as e:
            if attempt < 2:
                print(
                    f"Ошибка при отправке запроса: {e}. Повторная попытка через 10 секунд..."
                )
                time.sleep(10)  # Задержка перед повторной попыткой
            else:
                print(f"Все попытки завершились неудачно. ID вопроса = {id}")
                return "ERROR"  # Если все попытки не удались, возвращаем "ERROR"

    return "OK"
