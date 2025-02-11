from axes.signals import user_login_failed  # Use user_login_failed signal
from django_otp.plugins.otp_totp.models import TOTPDevice
from twilio.rest import Client
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser
from monitoring.models import User as MonitoringUser
from monitoring.models import User
from axes.models import AccessAttempt
from django.template.loader import render_to_string


@receiver(user_login_failed)
def send_confirmation_email(sender, request, credentials, **kwargs):
    # Check if the failed attempts reached 5
    failed_attempts = AccessAttempt.objects.filter(username=credentials.get('username')).count()

    if failed_attempts >= 5:
        # Send email to the user for device confirmation
        user = MonitoringUser.objects.filter(username=credentials.get('username')).first()
        if user:
            send_device_confirmation_email(user)

def send_device_confirmation_email(user):
    subject = "Is this your device?"
    message = render_to_string('monitoring/confirmation_email.html', {
        'user': user,
        'email': user.email,
    })
    send_mail(
        subject,
        message,
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
