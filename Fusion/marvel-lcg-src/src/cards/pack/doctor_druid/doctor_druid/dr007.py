from . import *

# Elemental Control (x2) — EVENEMENT, cout 2, [energy]. ATTACK. SUPERPOWER.
# While this card is in your hand your attacks deal 1 additional damage.
# Hero Action (attack): Deal 4 damage to an enemy.
#
# TEXTE CONTRE CODE
#  « your attacks deal 1 additional damage » -> `attack=1` a l'identite, meme
#    lecture que le `thwart=1` de `dr005` (son jumeau cote menace).
#  ⚠ QUATRE degats pour deux ressources : c'est la carte la plus rentable du
#    deck une fois jouee, et pourtant la garder en main donne +1 a CHAQUE
#    attaque du round. Tout le pack est bati sur cet arbitrage.


def GetAbilities() -> Sequence['Ability']:

    def controle_elementaire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, 4, effect)

    return [
        # ⚠ La moitie « tant que cette carte est dans votre main » n'est PAS
        # ici : elle est portee par le HEROS (dr001a), seule facon de la faire
        # fonctionner. Raison detaillee dans `__init__.py`.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            controle_elementaire,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
