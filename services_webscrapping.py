import datetime
import re

import dateutil.parser
import requests
from bs4 import BeautifulSoup


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


def main():
    print(
        azure_mariadb_server(),
        azure_postgresql_server(),
        azure_redis_server(),
        azure_mysql_server(),
        azure_aks(),
        azure_hdinsight(),
        azure_databricks(),
        gcp_dataproc(),
        gcp_dataproc_os(),
        gcp_memorystore_redis(),
        aws_eks(),
    )


if __name__ == "__main__":
    main()
