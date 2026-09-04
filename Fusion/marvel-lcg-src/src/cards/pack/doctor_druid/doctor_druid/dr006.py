from . import *

# Awaken Nature (x2) — EVENEMENT, cout 3, [physical].
# ATTACK. SUPERPOWER. THWART.
# While this card is in your hand Doctor Druid gains retaliate 1.
# Hero Action (attack/thwart): Deal 1 damage to each enemy and remove 1 threat
#   from each scheme.
#
# TEXTE CONTRE CODE
#  « DOCTOR DRUID gains retaliate 1 » -> nomme, donc `CardFinder(name=...)` et
#    non « chaque personnage » : contraste imprime avec `dr008`, qui dit bien
#    « each character you control ».
#  « EACH enemy » / « EACH scheme » -> tout le terrain, vilains ET sbires,
#    manigance principale ET annexes. Aucune cible a choisir, donc pas de
#    `SetTarget`.
#  « (attack/thwart) » -> DEUX libelles sur le meme `SetLabel`, comme nt002.


def GetAbilities() -> Sequence['Ability']:

    # ⚠ `RemoveThreatFromSchemes` et NON `RemoveThreat`, qui n'existe pas :
    # « 'Event' object has no attribute 'RemoveThreat' », exception AVALEE.
    # Sorti par l'autoplay, jamais par les cas — ils s'arretaient avant.
    def eveiller_la_nature(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        ennemis = list(Worlds.GetOnFieldEnemies(effect))
        if ennemis:
            this.DealDamage(ennemis, 1, effect)
        manigances = list(Worlds.FindCardsOnField(effect, card_type=Scheme2))
        if manigances:
            this.RemoveThreatFromSchemes(manigances, 1, effect)

    return [
        # ⚠ La moitie « tant que cette carte est dans votre main » n'est PAS
        # ici : elle est portee par le HEROS (dr001a), seule facon de la faire
        # fonctionner. Raison detaillee dans `__init__.py`.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            eveiller_la_nature,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
