import pandas as pd
from django.core.management.base import BaseCommand

from termplanner.terms.models import Module


class Command(BaseCommand):
    help = "Loads modules from a csv file into the database"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str)

    def handle(self, *args, **kwargs):
        path = kwargs["path"]
        # create data frame
        df = pd.read_csv(path, sep=";")

        for index, row in df.iterrows():

            Module.objects.update_or_create(
                # match by short_title of module
                short_title=row["short_title"],
                defaults=dict(
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
            self.stdout.write("Saved %s" % row["title"])
