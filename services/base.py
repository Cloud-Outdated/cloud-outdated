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
        public: service is visible to the users in the UI and is used in notifications
    """

    platform: Platform
    name: str  # eks - what is stored in db
    name_alternatives: list  # [Elastic Kubernetes Service, AWS Kubernetes]
    label: Optional[str] = None  # what is display to the user
    public: bool = True

    def __post_init__(self):
        if self.label is None:
            self.label = self.name


services = {
    "eks": Service(
        platform=aws,
        name="eks",
        label="EKS",
        name_alternatives=["Elastic Kubernetes Service"],
        public=False,
    ),
    "gke": Service(
        platform=gcp,
        name="gke",
        label="GKE",
        name_alternatives=["Google Kubernetes Engine"],
        public=False,
    ),
    "aks": Service(
        platform=azure,
        name="aks",
        label="AKS",
        name_alternatives=["Azure Kubernetes Service"],
        public=False,
    ),
    "gcp_cloudsql_postgres": Service(
        platform=gcp,
        name="gcp_cloudsql_postgres",
        label="GCP CloudSQL Postgres",
        name_alternatives=["PostgreSQL", "Postgres"],
    ),
    "gcp_cloudsql_sqlserver": Service(
        platform=gcp,
        name="gcp_cloudsql_sqlserver",
        label="GCP CloudSQL SQL Server",
        name_alternatives=["SQL Server", "MSSQL"],
    ),
    "gcp_cloudsql_mysql": Service(
        platform=gcp,
        name="gcp_cloudsql_mysql",
        label="GCP CloudSQL MySQL",
        name_alternatives=["MySQL"],
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
            "Mongo-compatible",
        ],
    ),
    "aws_memorydb": Service(
        platform=aws,
        name="aws_memorydb",
        label="MemoryDB",
        name_alternatives=[
            "MemoryDb",
            "AWS MemoryDb",
            "Redis-compatible",
        ],
    ),
    "aws_rabbitmq": Service(
        platform=aws,
        name="aws_rabbitmq",
        label="RabbitMQ",
        name_alternatives=[
            "RabbitMQ",
            "AWS RabbitMQ",
            "AWS RabbitMQ message broker",
        ],
    ),
    "aws_activemq": Service(
        platform=aws,
        name="aws_activemq",
        label="ActiveMQ",
        name_alternatives=[
            "ActiveMQ",
            "AWS ActiveMQ",
            "AWS ActiveMQ message broker",
            "Apache ActiveMQ",
        ],
    ),
    "aws_aurora": Service(
        platform=aws,
        name="aws_aurora",
        label="Aurora MySQL (MySQL 5.6 compatible)",
        name_alternatives=[
            "Aurora MySQL 5.6-compatible",
            "AWS Aurora",
            "AWS Aurora MySQL",
            "AWS Aurora MySQL 5.6",
        ],
    ),
    "aws_aurora_mysql": Service(
        platform=aws,
        name="aws_aurora_mysql",
        label="Aurora MySQL (MySQL 5.7+ compatible)",
        name_alternatives=[
            "Aurora MySQL 5.7+ compatible",
            "AWS Aurora MySQL 5.7",
            "AWS Aurora MySQL 8.0",
        ],
    ),
    "aws_aurora_postgres": Service(
        platform=aws,
        name="aws_aurora_postgres",
        label="Aurora Postgres",
        name_alternatives=[
            "Aurora Postgres",
            "Aurora PostgreSQL",
            "AWS Aurora Postgres",
            "AWS Aurora PostgreSQL",
        ],
    ),
    "aws_mariadb": Service(
        platform=aws,
        name="aws_mariadb",
        label="MariaDB",
        name_alternatives=[
            "MariaDB",
            "AWS MariaDB",
        ],
    ),
    "aws_mysql": Service(
        platform=aws,
        name="aws_mysql",
        label="MySQL",
        name_alternatives=[
            "MySQL",
            "AWS MySQL",
        ],
    ),
    "aws_postgres": Service(
        platform=aws,
        name="aws_postgres",
        label="Postgres",
        name_alternatives=[
            "Postgres",
            "PostgreSQL",
            "AWS Postgres",
            "AWS PostgreSQL",
        ],
    ),
    "aws_oracle_ee": Service(
        platform=aws,
        name="aws_oracle_ee",
        label="Oracle EE",
        name_alternatives=[
            "Oracle Enterprise Edition",
            "AWS Oracle EE",
            "AWS Oracle Enterprise Edition",
        ],
    ),
    "aws_oracle_ee_cdb": Service(
        platform=aws,
        name="aws_oracle_ee_cdb",
        label="Oracle EE CDB",
        name_alternatives=[
            "Oracle Enterprise Edition Container Database",
            "AWS Oracle EE CDB",
            "AWS Oracle Enterprise Edition Container Database",
        ],
    ),
    "aws_oracle_se2": Service(
        platform=aws,
        name="aws_oracle_se2",
        label="Oracle SE2",
        name_alternatives=[
            "Oracle Standard Edition Two",
            "AWS Oracle SE2 CDB",
            "AWS Oracle Standard Edition Two",
        ],
    ),
    "aws_oracle_se2_cdb": Service(
        platform=aws,
        name="aws_oracle_se2_cdb",
        label="Oracle SE2 CDB",
        name_alternatives=[
            "Oracle Standard Edition Two Container Database",
            "AWS Oracle SE2 CDB",
            "AWS Oracle Standard Edition Two Container Database",
        ],
    ),
    "aws_sqlserver_ee": Service(
        platform=aws,
        name="aws_sqlserver_ee",
        label="SQL Server EE",
        name_alternatives=[
            "SQL Server Enterprise Edition",
            "AWS SQL Server EE",
            "Microsoft SQL Server EE",
            "Microsoft SQL Server Enterprise Edition",
        ],
    ),
    "aws_sqlserver_se": Service(
        platform=aws,
        name="aws_sqlserver_se",
        label="SQL Server SE",
        name_alternatives=[
            "SQL Server Standard Edition",
            "AWS SQL Server SE",
            "Microsoft SQL Server SE",
            "Microsoft SQL Server Standard Edition",
        ],
    ),
    "aws_sqlserver_ex": Service(
        platform=aws,
        name="aws_sqlserver_ex",
        label="SQL Server EX",
        name_alternatives=[
            "SQL Server Express Edition",
            "AWS SQL Server EX",
            "Microsoft SQL Server EX",
            "Microsoft SQL Server Express Edition",
        ],
    ),
    "aws_sqlserver_web": Service(
        platform=aws,
        name="aws_sqlserver_web",
        label="SQL Server Web",
        name_alternatives=[
            "SQL Server Web Edition",
            "AWS SQL Server Web",
            "Microsoft SQL Server Web",
            "Microsoft SQL Server Web Edition",
        ],
    ),
    "azure_mariadb_server": Service(
        platform=azure,
        name="azure_mariadb_server",
        label="MariaDB Server",
        name_alternatives=["MariaDB", "Azure MariaDB"],
    ),
    "azure_postgresql_server": Service(
        platform=azure,
        name="azure_postgresql_server",
        label="PostgreSQL Server",
        name_alternatives=["Postgres", "Azure PostgreSQL", "Azure Postgres"],
    ),
    "azure_redis_server": Service(
        platform=azure,
        name="azure_redis_server",
        label="Redis Server",
        name_alternatives=["Redis", "Azure Redis"],
    ),
    "azure_mysql_server": Service(
        platform=azure,
        name="azure_mysql_server",
        label="MySQL Server",
        name_alternatives=["MySQL", "Azure MySQL"],
    ),
    "azure_hdinsight": Service(
        platform=azure,
        name="azure_hdinsight",
        label="Azure HDInsight",
        name_alternatives=["HDInsight"],
    ),
    "azure_databricks": Service(
        platform=azure,
        name="azure_databricks",
        label="Azure Databricks",
        name_alternatives=["Databricks"],
    )
    # ...
}

# shorthand to be used in models for choice fields
service_choices = [
    (service_key, service_details.label)
    for service_key, service_details in services.items()
]
