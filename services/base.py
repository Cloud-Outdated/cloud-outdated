# this lives somewhere in services/base.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Platform:
    """Cloud platform.

    Think AWS, GCP, ...

    Attributes:
        name: name of the platform
        name_alternatives: list of alternative names; platform full name etc.
        lable: value displayed to the end user
    """

    name: str
    name_alternatives: list
    label: Optional[str] = None


aws = Platform("aws", ["Amazon Web Services"], "AWS")
gcp = Platform("gcp", ["Google Cloud", "Google Cloud Platform"], "GCP")
azure = Platform("azure", ["Azure", "Microsoft Azure"], "Azure")


@dataclass
class Service:
    """Individual service on a cloud platform.

    Think EKS, Postgres, ...

    Attributes:
        platform: which platform this service belongs to
        name: name of the service
        name_alternatives: list of alternative names; service full name etc.
        lable: value displayed to the end user, name is used if not set
    """

    platform: Platform
    name: str  # eks - what is stored in db
    name_alternatives: list  # [Elastic Kubernetes Service, AWS Kubernetes]
    label: Optional[str] = None  # what is display to the user

    def __post_init__(self):
        if self.label is None:
            self.label = self.name


services = {
    "eks": Service(
        platform=aws,
        name="eks",
        label="EKS",
        name_alternatives=["Elastic Kubernetes Service"],
    ),
    "gke": Service(
        platform=gcp,
        name="gke",
        label="GKE",
        name_alternatives=["Google Kubernetes Engine"],
    ),
    "aks": Service(
        platform=azure,
        name="aks",
        label="AKS",
        name_alternatives=["Azure Kubernetes Service"],
    ),
    "gcp_cloud_sql": Service(
        platform=gcp,
        name="gcp_cloud_sql",
        label="Cloud SQL",
        name_alternatives=["PostgreSQL", "MySQL", "SQL Server", "MSSQL"],
    ),
    "aws_elasticache_redis": Service(
        platform=aws,
        name="aws_elasticache_redis",
        label="ElastiCache Redis",
        name_alternatives=[
            "Redis",
            "AWS Redis",
        ],
    ),
    "aws_elasticache_memcached": Service(
        platform=aws,
        name="aws_elasticache_memcached",
        label="ElastiCache Memcached",
        name_alternatives=[
            "Memcached",
            "AWS Memcached",
        ],
    ),
    "aws_kafka": Service(
        platform=aws,
        name="aws_kafka",
        label="Kafka",
        name_alternatives=[
            "Kafka",
            "AWS Kafka",
        ],
    ),
    "aws_es": Service(
        platform=aws,
        name="aws_es",
        label="ElasticSearch",
        name_alternatives=[
            "AWS ES",
            "AWS ElasticSearch",
        ],
    ),
    "aws_opensearch": Service(
        platform=aws,
        name="aws_opensearch",
        label="OpenSearch",
        name_alternatives=[
            "OpenSearch",
            "AWS OpenSearch",
            "ElastiSearch fork",
        ],
    ),
    "aws_neptune": Service(
        platform=aws,
        name="aws_neptune",
        label="Neptune",
        name_alternatives=[
            "Neptune",
            "AWS Neptune",
            "Graph Database",
        ],
    ),
    "aws_docdb": Service(
        platform=aws,
        name="aws_docdb",
        label="DocumentDB",
        name_alternatives=[
            "DocumentDB",
            "AWS DocumentDB",
            "DocDB",
            "AWS DocDB",
            "Mongo compatible",
        ],
    ),
    # ...
}

# shorthand to be used in models for choice fields
service_choices = [
    (service_key, service_details.label)
    for service_key, service_details in services.items()
]
