from mail_checker_ozon_rate import mail_read


def handler(event, context):
    return {
        "statusCode": 200,
        "body": mail_read(),
    }
