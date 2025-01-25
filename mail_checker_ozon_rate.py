import requests
import boto3
import imaplib
import email
from email.header import decode_header
import time
from bs4 import BeautifulSoup
from login import *
from API_send_answer import send_answer


# Читает файл с cookie из Yandex Object Storage
def read_cookie_bucket() -> str | None:
    max_attempts = 3  # Максимальное количество попыток загрузки
    delay = 1  # Задержка между попытками в секундах

    for attempt in range(max_attempts):
        try:
            # Создаем клиент для работы с S3
            s3 = boto3.client(
                "s3",
                endpoint_url="https://storage.yandexcloud.net",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=region,
            )

            # Читаем содержимое файла
            response = s3.get_object(
                Bucket=bucket_name,
                Key=file_name,
            )

            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                content = response["Body"].read().decode("utf-8")
                print(
                    f"File '{file_name}' successfully read from Yandex Object Storage."
                )
                return content  # Возвращаем содержимое файла
            else:
                print(
                    f"Failed to read file. Status code: {response['ResponseMetadata']['HTTPStatusCode']}"
                )
                print(response)
        except Exception as e:
            print(f"Error reading file: {e}")

        if attempt < max_attempts - 1:
            print(
                f"Попытка {attempt + 1} не удалась. Ждем {delay} секунд перед следующей попыткой..."
            )
            time.sleep(delay)

    print(f"Все {max_attempts} попытки чтения файла не удалась.")
    return None


# Основная функция для чтения cookie и запуска проверки почты
def mail_read() -> None:
    cookie = read_cookie_bucket()
    print(f"ПРОЧИТАЛ COOKIE")
    if cookie is not None and len(cookie) > 50:
        start_checking_mail(cookie)
    else:
        print("cookie = None или длина меньше 50. Считаю cookie некоректнымми.")


# Помечает письмо как непрочитанное
def mark_as_unread(mail: imaplib.IMAP4_SSL, num: str) -> None:
    try:
        status = mail.store(num, "+FLAGS", "\\Seen")
        if status[0] != "OK":
            print(f"Ошибка при установке флага 'Seen': {status[0]}")
            return
        status = mail.store(num, "-FLAGS", "\\Seen")
        if status[0] != "OK":
            print(f"Ошибка при сбросе флага 'Seen': {status[0]}")
        else:
            print(f"Письмо снова помечено как непрочитанное.")
    except imaplib.IMAP4.error as e:
        print(f"Ошибка IMAP: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")


# Начинает процесс отправки ответов на непрочитанные письма
def start_sending_answers(cookie: str) -> None:
    # Подключение к серверу
    print("Подключаюсь к почтовому северу.")
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(imap_username, imap_password)

    # Выбор почтового ящика (INBOX - это стандартное имя для входящих писем)
    mail.select("INBOX")

    # Поиск непрочитанных писем
    status, message_ids = mail.search(None, "UNSEEN")

    # Обработка каждого непрочитанного письма
    for num in message_ids[0].split():
        print("Начинаю обработку непрочитанных писем.")
        status, msg_parts = mail.fetch(num, "(RFC822)")
        raw_email = msg_parts[0][1]

        # Парсинг письма
        msg = email.message_from_bytes(raw_email)

        # Игнорирование ответных писем
        if msg.get_content_type() == "message/rfc822":
            continue

        # Получение отправителя
        sender = msg["Return-path"]

        # Получение темы письма
        subject = decode_header(msg["Subject"])[0][0]

        # Декодирую байтовую строку в обычную строку
        subject = subject.decode("utf-8")

        # Получение содержимого письма
        content = ""
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/html":
                content = (
                    part.get_payload(decode=True)
                    .decode(part.get_content_charset())
                    .split("\n")[0]
                    .strip()
                )
        from_mail = sender

        if from_mail == trusted_mail:
            subject_tema = subject.replace("Re: ", "")

            html_content = content

            # Функция для удаления HTML-тегов из строки
            def remove_html_tags(html_str: str) -> str:
                soup = BeautifulSoup(html_str, "html.parser")
                return soup.get_text(separator=" ", strip=True)

            # Применяю функцию ко всем элементам списка
            cleaned_content = remove_html_tags(html_content)
            content_telo = cleaned_content.split("_____")[1]

            if send_answer(from_mail, subject_tema, content_telo, cookie) == "ERROR":
                mark_as_unread(mail, num)
        else:
            print(
                f"Неподтвержденный email {from_mail}. Отправка ответа по API произведена не будет."
            )
        print("-" * 30)
        time.sleep(4)
    print("Непрочитанных писем нет. Отключаюсь от сервера.")
    print("******************STOP******************")
    mail.close()
    mail.logout()


# Запускает процесс проверки почты и отправки ответов
def start_checking_mail(cookie: str) -> None:
    print("******************START******************")
    start_sending_answers(cookie)
