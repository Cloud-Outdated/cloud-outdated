from core.emails import BaseEmail


class NotificationEmail(BaseEmail):
    template_name = "notification.html"
