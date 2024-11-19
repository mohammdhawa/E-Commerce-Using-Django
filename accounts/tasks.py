from celery import shared_task
from django.core.mail import send_mail
import time


@shared_task
def execute_something():
    for x in range(20):
        print(x)
        time.sleep(1)

# Send email
@shared_task
def send_activation_code(username, code, email):
    print("\n\n*********************** Task ***********************\n\n")
    send_mail(
        "Account Activation",
        f"Welcome {username} \nUse this code {code} to activate your account.",
        "ismekbektop@gmail.com",
        [email],
        fail_silently=False,
    )