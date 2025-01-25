company_id = "123456"  # id компании, можно посмотреть на странице компании (например https://www.ozon.ru/seller/ooo-mebelnaya-fabrika-volzhanka-1234/products/?miniapp=seller_1234 - id компании 1234)
bucket_name = "name"  # Название бакета
file_name = "name.txt"  # Название файла с куки в бакете
AWS_ACCESS_KEY_ID = "key-id"  # key id для доступа в бакет
AWS_SECRET_ACCESS_KEY = "key"  # key для доступа в бакет
region = "region"  # регион, обычно "ru-central1"
imap_server = "imap.mail.ru"
imap_username = (
    "example1@mail.ru"  # Почта, которую необходимо проверять на входящие письма
)
imap_password = "password"  # Пароль от почты для сторонних приложений
trusted_mail = "<example2@mail.ru>"  # Почта, с которой будут поступать письма, при заполнении переменной важно соблюдать регистр символов. Т.к. могут возникать ошибки <exaMple2@mail.ru> не то же самое, что <eXample2@mail.ru>
