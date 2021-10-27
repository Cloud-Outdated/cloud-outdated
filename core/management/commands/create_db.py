from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Creates the initial database"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting db creation"))

        dbname = settings.DATABASES["default"]["NAME"]
        user = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        port = settings.DATABASES["default"]["PORT"]

        self.stdout.write(self.style.NOTICE(f"dbname: {dbname}"))
        self.stdout.write(self.style.NOTICE(f"user: {user}"))
        self.stdout.write(self.style.NOTICE(f"host: {host}"))
        self.stdout.write(self.style.NOTICE(f"port: {port}"))

        con = None
        con = connect(dbname=dbname, user=user, host=host, password=password, port=port)
        
        self.stdout.write(self.style.NOTICE(con.status))
        
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute("CREATE DATABASE " + dbname)
        cur.close()
        con.close()

        self.stdout.write(self.style.SUCCESS("All Done"))
