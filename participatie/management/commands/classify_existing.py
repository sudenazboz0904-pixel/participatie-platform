import time
from collections import Counter

from django.core.management.base import BaseCommand

from participatie.models import Proposal
from participatie.services.theme_classifier import classify_theme


class Command(BaseCommand):
    help = 'Classificeer bestaande voorstellen met thema "overig" opnieuw via AI'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Toon wat er zou worden gewijzigd zonder iets op te slaan.',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        proposals = Proposal.objects.filter(theme='overig')
        total = proposals.count()

        if total == 0:
            self.stdout.write('Geen voorstellen met thema "overig" gevonden.')
            return

        mode_label = '[DRY-RUN] ' if dry_run else ''
        self.stdout.write(f'{mode_label}{total} voorstel(len) te classificeren...\n')

        theme_counter = Counter()
        fallback_count = 0

        for i, proposal in enumerate(proposals, 1):
            new_theme = classify_theme(proposal.title, proposal.description)
            short_title = proposal.title[:60]
            self.stdout.write(
                f'  [{i}/{total}] (id={proposal.pk}) "{short_title}" overig → {new_theme}'
            )

            if new_theme == 'overig':
                fallback_count += 1

            theme_counter[new_theme] += 1

            if not dry_run:
                proposal.theme = new_theme
                proposal.save(update_fields=['theme'])

            if i < total:
                time.sleep(0.5)

        self.stdout.write('')
        self.stdout.write('--- Samenvatting ---')
        self.stdout.write(f'Verwerkt:  {total}')
        for theme, count in sorted(theme_counter.items()):
            self.stdout.write(f'  {theme}: {count}')
        self.stdout.write(f'Fallbacks naar "overig": {fallback_count}')

        if dry_run:
            self.stdout.write(self.style.WARNING('\nDry-run: er is niets opgeslagen.'))
        else:
            self.stdout.write(self.style.SUCCESS('\nKlaar. Wijzigingen opgeslagen.'))
