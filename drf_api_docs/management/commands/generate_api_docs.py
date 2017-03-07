from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from drf_api_docs.handlers import ApiDocsHandler


class Command(BaseCommand):
    requires_model_validation = False
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('--locale', default=None, dest='locale')
        parser.add_argument('--project-name', default='The name of project', dest='project_name')

    def handle(self, *args: tuple, **options: dict):
        lang = options['locale'] or getattr(settings, 'LANGUAGE_CODE', 'en')
        project_name = options['project_name']

        handler = ApiDocsHandler(project_name=project_name)
        translation.activate(lang)
        self.stdout.write(handler.render())
