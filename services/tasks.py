import logging
from collections import defaultdict
from functools import reduce
from os import environ
from typing import Callable, List

import boto3
import backoff
from django.conf import settings
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build
from subscriptions.models import Subscription

from services.base import Service, services
from services.email import NotificationEmail
from services.models import Version

logger = logging.getLogger(__name__)


# export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service/account/key.json"


def gcloud_sql():
    with build(
        "sqladmin",
        "v1",
    ) as sqladmin:
        flags = sqladmin.flags().list().execute()
    return list(
        reduce(
            lambda a, b: set(list(a) + list(b)),
            [i["appliesTo"] for i in flags["items"]],
        )
    )


def get_aws_session():
    # credentials used here are from zappa settings
    return boto3.session.Session()


def aws_elasticache_redis():
    """Get AWS ElastiCache Redis versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("elasticache")
    versions = client.describe_cache_engine_versions(Engine="redis")[
        "CacheEngineVersions"
    ]
    return [version["EngineVersion"] for version in versions]


def aws_elasticache_memcached():
    """Get AWS ElastiCache Memcached versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("elasticache")
    versions = client.describe_cache_engine_versions(Engine="memcached")[
        "CacheEngineVersions"
    ]
    return [version["EngineVersion"] for version in versions]


def aws_kafka():
    """Get AWS Kafka versions.

    Already filters out deprecated versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("kafka")
    versions = client.list_kafka_versions()["KafkaVersions"]
    return [
        version["Version"] for version in versions if version["Status"] != "DEPRECATED"
    ]


def aws_es():
    """Get AWS ElasticSearch versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("es")
    versions = client.list_elasticsearch_versions()["ElasticsearchVersions"]
    return [version for version in versions]


def aws_opensearch():
    """Get AWS OpenSearch versions.

    OpenSearch is a community-driven, open-source fork from the last
    ALv2 version of Elasticsearch and Kibana.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("opensearch")
    versions = client.list_versions()["Versions"]
    return [version for version in versions]


def aws_neptune():
    """Get AWS Neptune versions.

    Neptune is a fully-managed graph database service.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("neptune")
    versions = client.describe_db_engine_versions(Engine="neptune")["DBEngineVersions"]
    return [version["EngineVersion"] for version in versions]


def aws_docdb():
    """Get AWS DocDB versions.

    DocumentDB is managed Mongo compatible DB.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("docdb")
    versions = client.describe_db_engine_versions(Engine="docdb")["DBEngineVersions"]
    return [version["EngineVersion"] for version in versions]


def aws_memorydb():
    """Get AWS MemoryDB versions.

    Redis-compatible, durable, in-memory database service for ultra-fast performance.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("memorydb")
    versions = client.describe_engine_versions()["EngineVersions"]
    return [version["EngineVersion"] for version in versions]


class PollService:
    def __init__(self, service: Service, poll_fn: Callable):
        self.service = service
        self.poll_fn = poll_fn
        self.deprecated_versions = []
        self.added_versions = []

    def poll(self):
        logger.info(f"Polling service {self.service.name}")
        try:
            supported_versions = self.poll_fn()

            logger.info(
                f"Service: {self.service.name} - Supported versions {supported_versions}"
            )

            current_versions = self.get_current_versions()

            logger.info(
                f"Service: {self.service.name} - Current stored versions {current_versions}"
            )

            self.deprecated_versions = self.process_deprecated_versions(
                current_versions, supported_versions
            )

            self.added_versions = self.process_added_versions(
                current_versions, supported_versions
            )
        except:
            logger.error(
                f"Error ocurred while polling service {self.service.name}",
                exc_info=True,
            )

    def get_current_versions(self):
        return [
            v.version
            for v in Version.objects.filter(service=self.service.name, deprecated=None)
        ]

    def process_deprecated_versions(self, current_versions, supported_versions):
        # Get newly deprecated versions
        to_deprecate = set(current_versions) - set(supported_versions)

        if to_deprecate:
            Version.objects.filter(
                service=self.service.name, version__in=to_deprecate
            ).update(deprecated=True)
            logger.info(
                f"Service: {self.service.name} - These versions have been deprecated: {to_deprecate}",
            )

        return list(to_deprecate)

    def process_added_versions(self, current_versions, supported_versions):
        # Get newly added versions
        added_versions = set(supported_versions) - set(current_versions)

        if added_versions:
            Version.objects.bulk_create(
                [Version(service=self.service.name, version=v) for v in added_versions]
            )
            logger.info(
                f"Service: {self.service.name} - These versions have been added {added_versions}",
            )

        return list(added_versions)


def do_polling(executor: PollService):
    executor.poll()
    return executor


def poll_gcp():
    """Entrypoint task for all GCP services."""
    gcp_services = [
        PollService(service=services["gcp_cloud_sql"], poll_fn=gcloud_sql),
    ]

    # with multiprocessing.Pool(settings.POLLING_THREADS) as p:
    #    polled_services = p.map(do_polling, gcp_services)
    polled_services = map(do_polling, gcp_services)

    send_notifications(polled_services)


def poll_aws():
    """Entrypoint task for all AWS services."""
    aws_services = [
        PollService(
            service=services["aws_elasticache_redis"], poll_fn=aws_elasticache_redis
        ),
        PollService(
            service=services["aws_elasticache_memcached"],
            poll_fn=aws_elasticache_memcached,
        ),
        PollService(
            service=services["aws_kafka"],
            poll_fn=aws_kafka,
        ),
        PollService(
            service=services["aws_es"],
            poll_fn=aws_es,
        ),
        PollService(
            service=services["aws_opensearch"],
            poll_fn=aws_opensearch,
        ),
        PollService(
            service=services["aws_neptune"],
            poll_fn=aws_neptune,
        ),
        PollService(
            service=services["aws_docdb"],
            poll_fn=aws_docdb,
        ),
        PollService(
            service=services["aws_memorydb"],
            poll_fn=aws_memorydb,
        ),
    ]

    polled_services = map(do_polling, aws_services)

    send_notifications(polled_services)


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=settings.NOTIFICATIONS_MAX_RETRIES,
    max_time=settings.NOTIFICATIONS_MAX_TIME,
    backoff_log_level=logging.WARN,
)
def send_notifications(polled_services: List[PollService]):
    notifications = defaultdict(list)

    for ps in polled_services:
        if ps.added_versions or ps.deprecated_versions:
            notifications[ps.service.name].append(
                (ps.added_versions, ps.deprecated_versions)
            )

    subscriptions = Subscription.objects.filter(
        service__in=notifications.keys(), disabled=None
    ).prefetch_related("user")

    users_subscriptions = defaultdict(list)
    for sub in subscriptions:
        users_subscriptions[sub.user].append(
            {
                "service": sub.service,
                "added": notifications[sub.service][0],
                "deprecated": notifications[sub.service][1],
            }
        )

    for user, subs in users_subscriptions.items():
        ctx = {"subscriptions": subs}
        NotificationEmail(context=ctx).send(to=[user.email])
