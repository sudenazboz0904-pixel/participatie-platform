from django.core.management.base import BaseCommand
from participatie.models import Proposal
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create proposal data for Gouda neighborhoods'

    def handle(self, *args, **options):
        # Verwijder oude
        Proposal.objects.all().delete()

        voorstellen = [
            ("Parkeergarage in Binnenstad", "De Binnenstad heeft veel drukte. Een moderne ondergrondse parkeergarage zou bezoekers helpen.", 28),
            ("Speeltuin renovatie in Korte Akkeren", "Kinderen in Korte Akkeren hebben een veilige, moderne speelplek nodig.", 24),
            ("Fietspaden uitbreiden in Kort Haarlem", "Kort Haarlem groeit. Bredere fietspaden zijn nodig.", 20),
            ("Groenzone in Goverwelle", "Goverwelle mist groen. Meer bomen en parken.", 16),
            ("Buurtcentrum Oosterwei", "Oosterwei verdient een modern buurtcentrum.", 22),
            ("Speelplein verbeteren in Bloemendaal", "Het speelplein in Bloemendaal is verouderd.", 18),
            ("Wandelpad aanleggen in Plaswijck", "Plaswijck heeft een mooi pad langs het water nodig.", 25),
            ("Busstation moderniseren in Stolwijkersluis", "Modernisering van het busstation.", 14),
            ("Sportcomplex uitbreiden in Westergouwe", "Westergouwe heeft meer sportfaciliteiten nodig.", 26),
        ]

        for title, desc, votes in voorstellen:
            Proposal.objects.create(title=title, description=desc, votes=votes, created_at=timezone.now())
            self.stdout.write(f"✓ {title}")

        self.stdout.write(self.style.SUCCESS(f'\nTotaal: {Proposal.objects.count()} voorstellen!'))