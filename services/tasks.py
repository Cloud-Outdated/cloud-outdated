import datetime
import json
import re
import sys
import traceback
from functools import reduce
from typing import Callable, List

import boto3
import dateutil.parser
import requests
import structlog
from django.conf import settings
from bs4 import BeautifulSoup
from core.util import notify_operator
from google.cloud import container_v1
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.utils import timezone

from services.base import Service, services
from services.models import Version

logger = structlog.get_logger(__name__)


def get_gcp_credentials():
    """Read GCP credentials from settings in order to use it with GCP clients."""
    gcp_credentials = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(gcp_credentials)
    return credentials


def _gcp_cloud_sql(engine):
    """Generic function to get Cloud SQL versions.

    Args:
        engine (str): Database engine.

    Returns:
        list(str): List of supported versions.
    """
    with build(
        "sqladmin",
        "v1",
        credentials=get_gcp_credentials(),
    ) as sqladmin:
        flags = sqladmin.flags().list().execute()
    return [
        v
        for v in reduce(
            lambda a, b: set(list(a) + list(b)),
            [i["appliesTo"] for i in flags["items"]],
        )
        if str(v).lower().startswith(str(engine).lower())
    ]


def gcp_cloudsql_postgres():
    """Get GCP CloudSQL Postgres versions.

    Returns:
        list[str] of supported versions
    """
    return _gcp_cloud_sql("postgres")


def gcp_cloudsql_sqlserver():
    """Get GCP CloudSQL SQL Server versions.

    Returns:
        list[str] of supported versions
    """
    return _gcp_cloud_sql("sqlserver")


def gcp_cloudsql_mysql():
    """Get GCP MySQL Server versions.

    Returns:
        list[str] of supported versions
    """
    return _gcp_cloud_sql("mysql")


def gcp_gke():
    """Get GCP GKE master node supported versions.

    Returns:
        list(str): List of supported versions
    """
    client = container_v1.ClusterManagerClient(credentials=get_gcp_credentials())
    result = client.get_server_config(zone="europe-central2")
    return result.valid_master_versions


def gcp_dataproc_os():
    """Get GCP Dataproc OS images compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://cloud.google.com/dataproc/docs/concepts/versioning/overview"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="how_versioning_works")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            if version:
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure Dataproc OS images versions not found")
    return supported_versions


def gcp_dataproc():
    """Get GCP Dataproc compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions"
    )
    final_supported_versions = []
    soup = BeautifulSoup(page.content, "html.parser")
    images = {"debian": 6, "ubuntu": 4, "rocky linux": 4}
    for image, offset in images.items():
        supported_versions = []
        server_version_table = soup.find(id=f"{image.replace(' ', '_')}_images")
        for _ in range(offset):
            server_version_table = server_version_table.nextSibling
        for child in server_version_table.findChildren("tr"):
            data = child.findChildren("td")
            if data:
                version = str(data[0].text.strip())
                if version:
                    supported_versions.append(version)
        if supported_versions == []:
            raise ScrappingError("GCP Dataproc versions not found")
        final_supported_versions += supported_versions
    return final_supported_versions


def gcp_memorystore_redis():
    """Get GCP Memorystore for Redis compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://cloud.google.com/memorystore/docs/redis/supported-versions"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="current_versions")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[1].text.strip())
            if version:
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure Memorystore for Redis versions not found")
    return supported_versions


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


def aws_rabbitmq():
    """Get AWS RabbitMQ versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("mq")
    engines = client.describe_broker_engine_types(EngineType="rabbitmq")[
        "BrokerEngineTypes"
    ]
    versions = []
    for engine in engines:
        if engine["EngineType"] == "RABBITMQ":
            versions += [version["Name"] for version in engine["EngineVersions"]]
    return versions


def aws_activemq():
    """Get AWS ActiveMQ versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("mq")
    engines = client.describe_broker_engine_types(EngineType="activemq")[
        "BrokerEngineTypes"
    ]
    versions = []
    for engine in engines:
        if engine["EngineType"] == "ACTIVEMQ":
            versions += [version["Name"] for version in engine["EngineVersions"]]
    return versions


def _aws_rds(engine):
    """Generic function to get RDS versions.

    Returns:
        list[str] of supported versions
    """
    client = get_aws_session().client("rds")
    versions = client.describe_db_engine_versions(Engine=engine)["DBEngineVersions"]
    return [version["EngineVersion"] for version in versions]


def aws_aurora():
    """Get AWS Aurora for MySQL 5.6 compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("aurora")


def aws_aurora_mysql():
    """Get AWS Aurora for MySQL 5.7+ compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("aurora-mysql")


def aws_aurora_postgres():
    """Get AWS Aurora Postgres compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("aurora-postgresql")


def aws_mariadb():
    """Get AWS MariaDB compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("mariadb")


def aws_mysql():
    """Get AWS MySQL compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("mysql")


def aws_postgres():
    """Get AWS Postgres compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("postgres")


def aws_oracle_ee():
    """Get AWS Oracle Enterprise Edition compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("oracle-ee")


def aws_oracle_ee_cdb():
    """Get AWS Oracle Enterprise Edition compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("oracle-ee-cdb")


def aws_oracle_se2():
    """Get AWS Oracle Standard Edition Two compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("oracle-se2")


def aws_oracle_se2_cdb():
    """Get AWS Oracle Standard Edition Two Container Database compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("oracle-se2-cdb")


def aws_sqlserver_ee():
    """Get AWS SQL Server Enterprise Edition compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("sqlserver-ee")


def aws_sqlserver_se():
    """Get AWS SQL Server Enterprise Edition compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("sqlserver-se")


def aws_sqlserver_ex():
    """Get AWS SQL Server Express Edition compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("sqlserver-ex")


def aws_sqlserver_web():
    """Get AWS SQL Server Web Edition compatible versions.

    Returns:
        list[str] of supported versions
    """
    return _aws_rds("sqlserver-web")


def aws_eks():
    """Get AWS EKS compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="kubernetes-release-calendar")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            eos_date = str(data[3].text.strip())
            if (
                version
                and eos_date
                and dateutil.parser.parse(eos_date).timestamp()
                > datetime.datetime.now().timestamp()
            ):
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("AWS EKS versions not found")
    return supported_versions


class ScrappingError(Exception):
    pass


def azure_mariadb_server():
    """Get Azure MariaDB server compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.microsoft.com/en-us/rest/api/mariadb/servers/create"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="serverversion")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure MariaDB Server versions not found")
    return supported_versions


def azure_postgresql_server():
    """Get Azure PostgreSQL server compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.microsoft.com/en-us/azure/postgresql/concepts-version-policy"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="supported--postgresql-versions")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            if "retired" not in version.lower():
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure PostgreSQL Server versions not found")
    return supported_versions


def azure_redis_server():
    """Get Azure Redis server compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get("https://docs.microsoft.com/en-us/rest/api/redis/redis/update")
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="request-body")
    server_version_table = server_version_title.nextSibling.nextSibling
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if not data:
            continue
        prop = str(data[0].text.strip())
        if prop != "properties.redisVersion":
            continue
        value = str(data[2].text.strip())
        matched = re.search("\([0-9]+(,\s?[0-9]+)*\)", value)
        return [
            v.strip() for v in value[matched.start() + 1 : matched.end() - 1].split(",")
        ]
    raise ScrappingError("Azure Redis version not found")


def azure_mysql_server():
    """Get Azure MySQL server compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.microsoft.com/en-us/azure/mysql/concepts-version-policy"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="supported-mysql-versions")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[1].text.strip())
            if "retired" not in version.lower():
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure MySQL Server versions not found")
    return supported_versions


def azure_aks():
    """Get Azure Kubernetes compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.microsoft.com/en-us/azure/aks/supported-kubernetes-versions"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="aks-kubernetes-release-calendar")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            if not version.lower().endswith("*"):
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure Kubernetes versions not found")
    return supported_versions


def azure_hdinsight():
    """Get Azure HDInsight compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-component-versioning"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(id="supported-hdinsight-versions")
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure HDInsight versions not found")
    return supported_versions


def azure_databricks():
    """Get Azure Databricks compatible versions.

    Returns:
        list[str]: supported versions
    """

    page = requests.get(
        "https://docs.microsoft.com/en-us/azure/databricks/release-notes/runtime/releases"
    )
    soup = BeautifulSoup(page.content, "html.parser")
    server_version_title = soup.find(
        id="--supported-databricks-runtime-releases-and-support-schedule"
    )
    server_version_table = (
        server_version_title.nextSibling.nextSibling.nextSibling.nextSibling
    )
    supported_versions = []
    for child in server_version_table.findChildren("tr"):
        data = child.findChildren("td")
        if data:
            version = str(data[0].text.strip())
            if version:
                supported_versions.append(version)
    if supported_versions == []:
        raise ScrappingError("Azure Databricks versions not found")
    return supported_versions


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
        except Exception as e:
            error_message = f"Error occurred while polling service {self.service.name}"
            notify_operator(
                f"{error_message}:\n {type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e.__str__()}"
            )
            logger.error(error_message, exc_info=True)

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
            ).update(deprecated=timezone.now())
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
    logger.info("Starting polling GCP")

    gcp_services = [
        PollService(service=services["gcp_gke"], poll_fn=gcp_gke),
        PollService(
            service=services["gcp_cloudsql_postgres"], poll_fn=gcp_cloudsql_postgres
        ),
        PollService(
            service=services["gcp_cloudsql_sqlserver"], poll_fn=gcp_cloudsql_sqlserver
        ),
        PollService(service=services["gcp_cloudsql_mysql"], poll_fn=gcp_cloudsql_mysql),
        PollService(service=services["gcp_dataproc"], poll_fn=gcp_dataproc),
        PollService(service=services["gcp_dataproc_os"], poll_fn=gcp_dataproc_os),
        PollService(
            service=services["gcp_memorystore_redis"], poll_fn=gcp_memorystore_redis
        ),
    ]

    for service in gcp_services:
        do_polling(service)

    logger.info("Finished polling GCP")


def poll_aws():
    """Entrypoint task for all AWS services."""
    logger.info("Starting polling AWS")

    aws_services = [
        PollService(service=services["aws_eks"], poll_fn=aws_eks),
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
        PollService(
            service=services["aws_rabbitmq"],
            poll_fn=aws_rabbitmq,
        ),
        PollService(
            service=services["aws_activemq"],
            poll_fn=aws_activemq,
        ),
        PollService(
            service=services["aws_aurora"],
            poll_fn=aws_aurora,
        ),
        PollService(
            service=services["aws_aurora_mysql"],
            poll_fn=aws_aurora_mysql,
        ),
        PollService(
            service=services["aws_aurora_postgres"],
            poll_fn=aws_aurora_postgres,
        ),
        PollService(
            service=services["aws_mariadb"],
            poll_fn=aws_mariadb,
        ),
        PollService(
            service=services["aws_mysql"],
            poll_fn=aws_mysql,
        ),
        PollService(
            service=services["aws_postgres"],
            poll_fn=aws_postgres,
        ),
        PollService(
            service=services["aws_oracle_ee"],
            poll_fn=aws_oracle_ee,
        ),
        PollService(
            service=services["aws_oracle_ee_cdb"],
            poll_fn=aws_oracle_ee_cdb,
        ),
        PollService(
            service=services["aws_oracle_se2"],
            poll_fn=aws_oracle_se2,
        ),
        PollService(
            service=services["aws_oracle_se2_cdb"],
            poll_fn=aws_oracle_se2_cdb,
        ),
        PollService(
            service=services["aws_sqlserver_ee"],
            poll_fn=aws_sqlserver_ee,
        ),
        PollService(
            service=services["aws_sqlserver_se"],
            poll_fn=aws_sqlserver_se,
        ),
        PollService(
            service=services["aws_sqlserver_ex"],
            poll_fn=aws_sqlserver_ex,
        ),
        PollService(
            service=services["aws_sqlserver_web"],
            poll_fn=aws_sqlserver_web,
        ),
    ]

    for service in aws_services:
        do_polling(service)

    logger.info("Finished polling AWS")


def poll_azure():
    """Entrypoint task for all Azure services."""
    logger.info("Starting polling Azure")

    azure_services = [
        PollService(
            service=services["azure_mariadb_server"], poll_fn=azure_mariadb_server
        ),
        PollService(
            service=services["azure_postgresql_server"], poll_fn=azure_postgresql_server
        ),
        PollService(service=services["azure_redis_server"], poll_fn=azure_redis_server),
        PollService(service=services["azure_mysql_server"], poll_fn=azure_mysql_server),
        PollService(service=services["azure_aks"], poll_fn=azure_aks),
        PollService(service=services["azure_hdinsight"], poll_fn=azure_hdinsight),
        PollService(service=services["azure_databricks"], poll_fn=azure_databricks),
    ]

    for service in azure_services:
        do_polling(service)

    logger.info("Finished polling Azure")
