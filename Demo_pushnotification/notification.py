import json
import logging

import requests
from django.db import models
from django.utils import timezone
from fcm_django.models import FCMDevice
from firebase_admin import messaging

logger = logging.getLogger(__name__)


def send_notification(
    title, description, users_list, notification_data, is_not_translated=False
):
    """
    Sends a push notification to the devices associated with the given users.

    Args:
        title (str): The title of the notification.
        description (str): The description or message of the notification.
        users_list (List[User]): A list of user objects for whom the notification is intended.
        notification_data (dict): Additional data to include with the notification.
        is_not_translated (bool): If True, the notification will be sent in the user's preferred language.

    Returns:
        None.
    """
    messages = []
    try:
        # Step 1: Retrieve device tokens for the users
        device_token_list = (
            FCMDevice.objects.filter(
                user__id__in=users_list,
            )
            .exclude(
                models.Q(registration_id__isnull=True)
                | models.Q(registration_id="null"),
            )
            .values_list("registration_id", flat=True)
        )

        notifications = []
        for device_token in device_token_list:
            image = notification_data.get("details")
            # Step 2: Handle translation if required
            translated_title = title
            translated_description = description
            body_notification_value = {"body": translated_description}
            stringified_notification_data = {
                key: str(value) for key, value in notification_data.items()
            }

            if image:
                body_notification_value["image"] = image
            # Step 3: Prepare the FCM message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=translated_title,
                    body=str(translated_description),
                ),
                data=stringified_notification_data,
                token=device_token,
                android=messaging.AndroidConfig(priority="high"),
            )
            messages.append(message)

            notification_title = title
            notification_description = description
            notification_body = notification_data
            # Get all the users with the given ids
            if fcm_obj := FCMDevice.objects.filter(
                registration_id=device_token
            ).first():
                # Create NotificationDetails objects for each user

                notifications.append(
                    Notification(
                        user=fcm_obj.user,
                        title=notification_title,
                        type=notification_data.get("type"),
                        description=notification_description,
                        body=notification_body,
                    )
                )

        if messages:
            response = messaging.send_each(messages)
            logger.info(
                f"Successfully sent {response.success_count} messages, {response.failure_count} failures"
            )
            if response.failure_count > 0:
                for resp in response.responses:
                    if not resp.success:
                        logger.error(f"Error sending message: {resp.exception}")

        # Step 5: Insert the Notification objects into the database
        if notifications:
            Notification.objects.bulk_create(notifications)

    except Exception as e:
        logger.error(f"{e}", exc_info=True)
