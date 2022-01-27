import requests
import json
from django.conf import settings
from celery import shared_task
from congrats.models import CustomUser

def sms_login():
    params = {'email': settings.SMS_EMAIL, 'password': settings.SMS_PASSWORD}
    r = requests.post('http://notify.eskiz.uz/api/auth/login', params=params)
    token = r.json()['data']['token']
    return token



def sms_refresh():
    r = requests.post('http://notify.eskiz.uz' + '/api/auth/login/',
                      {'email': settings.SMS_EMAIL, 'password': settings.SMS_PASSWORD}).json()
    token = r['data']['token']
    return token


@shared_task
def sms_send(phone_number, text):
    users = CustomUser.objects.values('phone_number')
    for user in users:
        phone_number = str(phone_number)
        phone_number.replace("+", "")
        try:
            if phone_number[0:3] == "998":
                result = requests.post(settings.SMS_BASE_URL + '/api/message/sms/send',
                                    {'mobile_phone': user.phone_number, 'message': text},
                                    headers={'Authorization': f'Bearer {settings.SMS_TOKEN}'}).json()

                return result
            else:
                payload = {
                    "message": text,
                    "to": "+" + str(phone_number),
                    "sender_id": "EduOn"
                }
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + settings.SMS_TOKEN_GLOBAL
                }
                result = requests.post('https://api.sms.to/sms/send', json.dumps(payload),
                                    headers=headers).json()
                return result

        except:
            return None
        
