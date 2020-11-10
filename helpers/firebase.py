import firebase_admin
from django.conf import settings
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
default_app = firebase_admin.initialize_app(cred)


def send_notification(user, title, body, data={}):
    for device in user.firebase_device_tokens:
        try:
            message = messaging.Message(
                data=data,
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=device,
            )
            messaging.send(
                message=message,
                app=default_app,
            )
        except FirebaseError as e:
            if e.code in ['UNAUTHENTICATED', 'invalid-registration-token', 'registration-token-not-registered']:
                user.firebase_device_tokens.remove(device)
                user.save(update_fields=['firebase_device_tokens'])
        except ValueError as e:
            user.firebase_device_tokens.remove(device)
            user.save(update_fields=['firebase_device_tokens'])


def send_notification_to_topic(title, body, topic, data={}):

        message = messaging.Message(
            data=data,
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            topic=topic,
        )
        messaging.send(
            message=message,
            app=default_app,
        )


def subscribe_to_topic(tokens, topic):

    messaging.subscribe_to_topic(
        tokens,
        topic,
        app=default_app,
    )


def unsubscribe_from_topic(tokens, topic):

    messaging.unsubscribe_from_topic(
        tokens,
        topic,
        app=default_app,
    )
