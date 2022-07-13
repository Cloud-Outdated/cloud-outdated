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
        label: value displayed to the end user
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
        source_url: URL that points to the source of truth
    """

    platform: Platform
    name: str  # eks - what is stored in db
    name_alternatives: list  # [Elastic Kubernetes Service, AWS Kubernetes]
    label: Optional[str] = None  # what is display to the user
    public: bool = True
    source_url: str = ""  # URL that points to the source of truth

    def __post_init__(self):
        if self.label is None:
            self.label = self.name

    @property
    def name_clean(self):
        """Name as required to boast SEO. Using dashes instead of underscores."""
        return self.name.replace("_", "-")


services = {
    "aws_eks": Service(
        platform=aws,
        name="aws_eks",
        label="EKS",
        name_alternatives=["Elastic Kubernetes Service"],
        public=True,
        source_url="https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html",
    ),
    "gcp_gke": Service(
        platform=gcp,
        name="gcp_gke",
        label="GKE",
        name_alternatives=["Google Kubernetes Engine"],
        public=True,
    ),
    "azure_aks": Service(
        platform=azure,
        name="azure_aks",
        label="AKS",
        name_alternatives=["Azure Kubernetes Service"],
        public=True,
        source_url="https://docs.microsoft.com/en-us/azure/aks/supported-kubernetes-versions",
    ),
    "gcp_cloudsql_postgres": Service(
        platform=gcp,
        name="gcp_cloudsql_postgres",
        label="CloudSQL Postgres",
        name_alternatives=["PostgreSQL", "Postgres"],
    ),
    "gcp_cloudsql_sqlserver": Service(
        platform=gcp,
        name="gcp_cloudsql_sqlserver",
        label="CloudSQL SQL Server",
        name_alternatives=["SQL Server", "MSSQL"],
    ),
    "gcp_cloudsql_mysql": Service(
        platform=gcp,
        name="gcp_cloudsql_mysql",
        label="CloudSQL MySQL",
        name_alternatives=["MySQL"],
    ),
    "gcp_dataproc": Service(
        platform=gcp,
        name="gcp_dataproc",
        label="Dataproc",
        name_alternatives=["Dataproc"],
        source_url="https://cloud.google.com/dataproc/docs/concepts/versioning/dataproc-versions",
    ),
    "gcp_dataproc_os": Service(
        platform=gcp,
        name="gcp_dataproc_os",
        label="Dataproc OS Images",
        name_alternatives=["Dataproc OS Images", "Dataproc OS"],
        source_url="https://cloud.google.com/dataproc/docs/concepts/versioning/overview",
    ),
    "gcp_memorystore_redis": Service(
        platform=gcp,
        name="gcp_memorystore_redis",
        label="Memorystore Redis",
        name_alternatives=["GCP Redis", "Redis"],
        source_url="https://cloud.google.com/memorystore/docs/redis/supported-versions",
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
    "aws_lambda_nodejs": Service(
        platform=aws,
        name="aws_lambda_nodejs",
        label="AWS Lambda Node.js",
        name_alternatives=["Nodejs lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "aws_lambda_python": Service(
        platform=aws,
        name="aws_lambda_python",
        label="AWS Lambda Python",
        name_alternatives=["Python lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "aws_lambda_ruby": Service(
        platform=aws,
        name="aws_lambda_ruby",
        label="AWS Lambda Ruby",
        name_alternatives=["Ruby lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "aws_lambda_java": Service(
        platform=aws,
        name="aws_lambda_java",
        label="AWS Lambda Java",
        name_alternatives=["Java lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "aws_lambda_go": Service(
        platform=aws,
        name="aws_lambda_go",
        label="AWS Lambda Go",
        name_alternatives=["Go lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "aws_lambda_dotnet": Service(
        platform=aws,
        name="aws_lambda_dotnet",
        label="AWS Lambda .NET",
        name_alternatives=["Dotnet lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "aws_lambda_custom": Service(
        platform=aws,
        name="aws_lambda_custom",
        label="AWS Lambda Custom",
        name_alternatives=["Custom lambda"],
        source_url="https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html",
    ),
    "azure_mariadb_server": Service(
        platform=azure,
        name="azure_mariadb_server",
        label="MariaDB Server",
        name_alternatives=["MariaDB", "Azure MariaDB"],
        source_url="https://docs.microsoft.com/en-us/rest/api/mariadb/servers/create",
    ),
    "azure_postgresql_server": Service(
        platform=azure,
        name="azure_postgresql_server",
        label="PostgreSQL Server",
        name_alternatives=["Postgres", "Azure PostgreSQL", "Azure Postgres"],
        source_url="https://docs.microsoft.com/en-us/azure/postgresql/concepts-version-policy",
    ),
    "azure_redis_server": Service(
        platform=azure,
        name="azure_redis_server",
        label="Redis Server",
        name_alternatives=["Redis", "Azure Redis"],
        source_url="https://docs.microsoft.com/en-us/rest/api/redis/redis/update",
    ),
    "azure_mysql_server": Service(
        platform=azure,
        name="azure_mysql_server",
        label="MySQL Server",
        name_alternatives=["MySQL", "Azure MySQL"],
        source_url="https://docs.microsoft.com/en-us/azure/mysql/concepts-version-policy",
    ),
    "azure_hdinsight": Service(
        platform=azure,
        name="azure_hdinsight",
        label="HDInsight",
        name_alternatives=["HDInsight"],
        source_url="https://docs.microsoft.com/en-us/azure/hdinsight/hdinsight-component-versioning",
    ),
    "azure_databricks": Service(
        platform=azure,
        name="azure_databricks",
        label="Databricks",
        name_alternatives=["Databricks"],
        source_url="https://docs.microsoft.com/en-us/azure/databricks/release-notes/runtime/releases",
    ),
}

# shorthand to be used in models for choice fields
service_choices = [
    (service_key, service_details.label)
    for service_key, service_details in services.items()
]
