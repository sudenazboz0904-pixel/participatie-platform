from django.core.management.base import BaseCommand
from participatie.models import LiveUpdate
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create live update data'

    def handle(self, *args, **options):
        LiveUpdate.objects.all().delete()

        updates = [
            ("Gesprek met inwoners over verkeersveiligheid", "GBG ging in gesprek met bewoners uit Plaswijck over onveilige verkeerssituaties rondom scholen. Signalen uit de wijk worden meegenomen in verdere uitwerking.", "gesprek"),
            ("Aandacht voor betaalbaar wonen", "Tijdens de raadsvergadering heeft GBG opnieuw aandacht gevraagd voor meer betaalbare woningen voor starters en jongeren in Gouda.", "raad"),
            ("Idee uit de stad in behandeling", "Een voorstel van inwoners voor meer groen en ontmoetingsplekken in de wijk is opgepakt en wordt verder onderzocht.", "behandeling"),
        ]

        for title, msg, status in updates:
            LiveUpdate.objects.create(
                title=title, 
                message=msg, 
                status=status, 
                is_published=True,
                created_at=timezone.now()
            )
            self.stdout.write(f"✓ {title}")

        self.stdout.write(self.style.SUCCESS(f'\nTotaal: {LiveUpdate.objects.count()} live updates!'))
