from django.core.management.base import BaseCommand
from tickets.models import Project

class Command(BaseCommand):
  def handle(self, *args, **options):
    projects = Project.objects.all()
    for project in projects:
      project.append_total_score()