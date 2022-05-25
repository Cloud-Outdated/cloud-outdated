# Generated by Django 3.2.12 on 2022-05-12 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0005_alter_subscription_service"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="service",
            field=models.CharField(
                choices=[
                    ("aws_eks", "EKS"),
                    ("gcp_gke", "GKE"),
                    ("azure_aks", "AKS"),
                    ("gcp_cloudsql_postgres", "CloudSQL Postgres"),
                    ("gcp_cloudsql_sqlserver", "CloudSQL SQL Server"),
                    ("gcp_cloudsql_mysql", "CloudSQL MySQL"),
                    ("gcp_dataproc", "Dataproc"),
                    ("gcp_dataproc_os", "Dataproc OS Images"),
                    ("gcp_memorystore_redis", "Memorystore Redis"),
                    ("aws_elasticache_redis", "ElastiCache Redis"),
                    ("aws_elasticache_memcached", "ElastiCache Memcached"),
                    ("aws_kafka", "Kafka"),
                    ("aws_es", "ElasticSearch"),
                    ("aws_opensearch", "OpenSearch"),
                    ("aws_neptune", "Neptune"),
                    ("aws_docdb", "DocumentDB"),
                    ("aws_memorydb", "MemoryDB"),
                    ("aws_rabbitmq", "RabbitMQ"),
                    ("aws_activemq", "ActiveMQ"),
                    ("aws_aurora", "Aurora MySQL (MySQL 5.6 compatible)"),
                    ("aws_aurora_mysql", "Aurora MySQL (MySQL 5.7+ compatible)"),
                    ("aws_aurora_postgres", "Aurora Postgres"),
                    ("aws_mariadb", "MariaDB"),
                    ("aws_mysql", "MySQL"),
                    ("aws_postgres", "Postgres"),
                    ("aws_oracle_ee", "Oracle EE"),
                    ("aws_oracle_ee_cdb", "Oracle EE CDB"),
                    ("aws_oracle_se2", "Oracle SE2"),
                    ("aws_oracle_se2_cdb", "Oracle SE2 CDB"),
                    ("aws_sqlserver_ee", "SQL Server EE"),
                    ("aws_sqlserver_se", "SQL Server SE"),
                    ("aws_sqlserver_ex", "SQL Server EX"),
                    ("aws_sqlserver_web", "SQL Server Web"),
                    ("azure_mariadb_server", "MariaDB Server"),
                    ("azure_postgresql_server", "PostgreSQL Server"),
                    ("azure_redis_server", "Redis Server"),
                    ("azure_mysql_server", "MySQL Server"),
                    ("azure_hdinsight", "HDInsight"),
                    ("azure_databricks", "Databricks"),
                ],
                max_length=255,
            ),
        ),
    ]
