from django.contrib.auth.models import User
from fcm_django.models import FCMDevice
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book
from .serializer import BookSerializer


def create_or_update_fcm_device(request, user):
    """
    Create or update an FCMDevice object for the given user, based on the data in the
    request.

    The request should contain the following data:
    - fcm_token (string): the FCM registration token for the device
    - device_type (string): the type of device (e.g. "android", "ios")
    - device_id (string, optional): the unique ID for the device (if not provided,
      a new ID will be generated)

    If a device with the given registration token and device ID already exists, it will
    be updated with the new data. Otherwise, a new device will be created.

    Args:
        request: The HTTP request object containing the data to use for creating/updating
            the FCMDevice.
        user: The User object for the user associated with the device.
    """
    device_id = request.get("device_id", None)
    registration_id = request.get("fcm_token", None)
    device_type = request.get("device_type", None)
    print("device_id :", device_id)
    print("registration_id :", registration_id)
    print("device_type :", device_type)
    device_obj = FCMDevice.objects.filter(device_id=device_id)
    print("device_obj :", device_obj)
    device = device_obj.first()
    print("device :", device)
    if device:
        fcm_update = device_obj.update(
            registration_id=registration_id, type=device_type, user=user
        )
        print(1111111, fcm_update)
    else:
        fcm_create = FCMDevice.objects.create(
            device_id=device_id,
            registration_id=registration_id,
            type=device_type,
            user=user,
        )
        print(22222222222, fcm_create)


class UserViewset(viewsets.ViewSet):
    """
    Rider's Authentication all APIs Function are Listed here.
    """

    queryset = Book
    serializer_class = BookSerializer

    @action(detail=False, methods=["get"], url_path="create", permission_classes=[])
    def sign_in_or_create(self, request, *args, **kwargs):
        message = "Hello how are you ?"
        user = User.objects.create(
            first_name="keval1", username="keval123", email="keval132@gmail.com"
        )
        device = {
            "fcm_token": "fcmtk19125",
            "device_id": "dvctk18125",
            "device_type": "android",
        }
        create_or_update_fcm_device(device, user)
        user.save()
        return Response({"message": message}, status=status.HTTP_200_OK)
