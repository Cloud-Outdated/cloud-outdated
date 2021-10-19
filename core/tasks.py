import datetime
from django.conf import settings


def task_one():
    # here we can define periodic tasks
    # and call them in zappa_settings.json
    print(f"yes no maybe - {datetime.datetime.now().isoformat()}")
    print(f"settings: {settings.DEFAULT_AUTO_FIELD}")
