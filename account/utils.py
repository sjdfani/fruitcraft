from .models import Cards, CardType


def create_default_cards():
    card_exists = Cards.objects.filter(card_type=CardType.COMMON).exists()
    if not card_exists:
        for name in ['orange', 'apple', 'banana', 'carrot']:
            Cards.objects.create(
                name=name, card_type=CardType.COMMON, stage=1, max_power=400, revive_time='0:10 h', status=True
            )
