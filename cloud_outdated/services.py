from functools import reduce

from googleapiclient.discovery import build

# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/key.json"


def gcloud_sql():
    with build("sqladmin", "v1") as sqladmin:
        flags = sqladmin.flags().list().execute()
    return reduce(
        lambda a, b: set(list(a) + list(b)), [i["appliesTo"] for i in flags["items"]]
    )
