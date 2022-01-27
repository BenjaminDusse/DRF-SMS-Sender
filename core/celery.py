import os
import requests
import json
from celery import Celery
from congrats.models import CustomUser
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('congrats')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
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
        
