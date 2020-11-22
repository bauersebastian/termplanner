from django.apps import AppConfig


class TermsConfig(AppConfig):
    name = "termplanner.terms"

    def ready(self):
        try:
            import termplanner.terms.signals  # noqa F401
        except ImportError:
            pass
