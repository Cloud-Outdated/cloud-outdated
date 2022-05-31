from django.http.response import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.generic import View

from notifications.models import Notification, NotificationPixel


class NotificationPixelView(View):
    @cache_control(must_revalidate=True, max_age=60)
    def get(self, request, notification_id):
        """Tracking pixel for when a NotificationEmail is open.

        Args:
            request (WSGIRequest): Request object.
            notification_id (str): Notification UUID.

        Returns:
            HttpResponse: Empty image.
        """

        if Notification.objects.filter(id=notification_id).exists():
            metadata = {
                "HTTP_USER_AGENT": request.META.get("HTTP_USER_AGENT"),
                "HTTP_SEC_CH_UA_PLATFORM": request.META.get("HTTP_SEC_CH_UA_PLATFORM"),
                "HTTP_SEC_CH_UA_MOBILE": request.META.get("HTTP_SEC_CH_UA_MOBILE"),
                "HTTP_SEC_CH_UA": request.META.get("HTTP_SEC_CH_UA"),
                "HTTP_ACCEPT_LANGUAGE": request.META.get("HTTP_ACCEPT_LANGUAGE"),
                "REMOTE_ADDR": request.META.get("REMOTE_ADDR"),
            }
            NotificationPixel.objects.create(
                notification=Notification(id=notification_id), metadata=metadata
            )

        # Render the pixel
        pixel_image = b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
        return HttpResponse(pixel_image, content_type="image/gif")
