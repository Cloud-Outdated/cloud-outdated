import datetime
from django.conf import settings


def task_one():
    # here we can define periodic tasks
    # and call them in zappa_settings.json
    print(f"test event printout - {datetime.datetime.now().isoformat()}")
