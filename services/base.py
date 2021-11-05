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
    )
    # ...
}

# shorthand to be used in models for choice fields
service_choices = [
    (service_key, service_details.label)
    for service_key, service_details in services.items()
]
