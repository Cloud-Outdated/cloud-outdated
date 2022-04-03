from core.emails import BaseEmail


class NotificationEmail(BaseEmail):
    template_name = "notification.html"
    subject_suffix = "New service versions updates"
