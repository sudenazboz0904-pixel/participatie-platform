import logging
import os

import anthropic

logger = logging.getLogger(__name__)

THEMES = [
    'veiligheid',
    'verkeer',
    'groen',
    'wonen',
    'onderwijs',
    'zorg',
    'cultuur',
    'overig',
]

_SYSTEM_PROMPT = (
    "Je bent een classificatiesysteem voor een gemeentelijk participatieplatform in Gouda. "
    "Classificeer het voorstel in precies één van de onderstaande thema's. "
    "Antwoord met alleen de sleutelwaarde in lowercase, niets anders.\n\n"
    "Beschikbare thema's:\n"
    "- veiligheid: Veiligheid (incl. verlichting, criminaliteitspreventie, verkeersveiligheid)\n"
    "- verkeer: Verkeer & Mobiliteit (incl. fietspaden, parkeren, openbaar vervoer)\n"
    "- groen: Groen & Duurzaamheid (incl. parken, bomen, duurzame energie, klimaat)\n"
    "- wonen: Wonen (incl. woningbouw, renovatie, huisvesting)\n"
    "- onderwijs: Onderwijs & Jeugd (incl. scholen, speelplekken, speeltuinen, jongerenwerk, kinderopvang)\n"
    "- zorg: Zorg & Welzijn (incl. ouderenzorg, gehandicaptenondersteuning, buurtcentra, mantelzorg)\n"
    "- cultuur: Cultuur & Sport (incl. sportcomplexen, sportvelden, evenementen, erfgoed, musea)\n"
    "- overig: Overig (alleen als geen enkel ander thema past)\n"
)


def classify_theme(title: str, description: str) -> str:
    """Geeft één thema-sleutel terug op basis van titel en beschrijving.
    Valt terug op 'overig' bij elke fout of onverwachte uitvoer.
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key or api_key == 'jouw-api-key-hier':
        logger.warning('ANTHROPIC_API_KEY niet ingesteld, thema wordt overig')
        return 'overig'

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=20,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    'role': 'user',
                    'content': f'Titel: {title}\n\nBeschrijving: {description}',
                }
            ],
        )
        result = message.content[0].text.strip().lower()
        if result in THEMES:
            return result
        logger.warning('Claude gaf onbekend thema "%s" terug, terugval op overig', result)
        return 'overig'
    except Exception as exc:
        logger.error('Themaclassificatie mislukt: %s', exc)
        return 'overig'
