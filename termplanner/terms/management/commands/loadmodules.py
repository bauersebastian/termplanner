import pandas as pd
from django.core.management.base import BaseCommand

from termplanner.terms.models import Module
from termplanner.users.models import User


class Command(BaseCommand):
    help = "Loads modules from a csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        # create data frame
        df = pd.read_csv(path, sep=";")

        for index, row in df.iterrows():
            # clean dirty data
            # try:
            #    value = int(row["capacity"])
            # except ValueError:
            #    row["capacity"] = 0

            # clean dirty data in fee
            # if row["fee"] != True or row["fee"] != False or row["fee"] != None:
            #    row["fee"] = None

            Module.objects.update_or_create(
                # currently no ids for updates in file available
                # id=row["@id"],
                # osm_type=row["@type"],
                defaults=dict(
                    created_by=User.objects.get(pk=1),
                    title=row["title"],
                    short_title=row["short_title"],
                    description=row["description"],
                    host=row["host"],
                    quota_economics=row["quota_economics"],
                    quota_cs=row["quota_cs"],
                    quota_is=row["quota_is"],
                    quota_key_competence=row["quota_key_competence"],
                    ects=row["ects"],
                    term=row["term"],
                ),
            )
