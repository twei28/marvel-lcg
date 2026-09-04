from . import *

# Mystical Protection (x2) — EVENEMENT, cout 1, [physical]. SUPERPOWER.
# While this card is in your hand, each character you control gains stalwart.
# Hero Interrupt: When an encounter card would be revealed, discard it
#   instead. If there is no boost icon on that card, give a friendly character
#   a tough status card.
#
# CARTES DE REFERENCE
#  - `reveal.py` `WhenCardWouldReveal` + `message.SetBeInstead(effect)` pour
#    « discard it INSTEAD ».
#
# TEXTE CONTRE CODE
#  « EACH CHARACTER you control » -> `Friend` + `control_by="You"`, donc les
#    ALLIES aussi. Contraste imprime avec `dr006`, qui nomme le seul heros.
#  « If there is NO boost icon » -> on lit les icones de boost de la carte
#    ANNULEE. Une traitrise a 0 boost donne donc Tenace, une carte a boost
#    non.
#  ⚠ MOT-PIEGE MAJEUR : c'est une HERO INTERRUPT, pas une Action. Elle n'est
#    donc PAS rejouable par `dr001a` Druidic Ritual, qui ne prend que
#    « Action » et « Hero Action ». Seul evenement du set dans ce cas.


def GetAbilities() -> Sequence['Ability']:

    def protection_mystique(effect: 'Effect', message: 'Message.WhenCardWouldReveal') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        carte = getattr(message, "which_card", None) or getattr(message, "card", None)
        message.SetBeInstead(effect)
        if carte is not None:
            Faces.DiscardAll([carte], effect)

        boosts = int(getattr(carte, "boost", 0) or 0) if carte is not None else 0
        if boosts > 0:
            return

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)

    return [
        # ⚠ La moitie « tant que cette carte est dans votre main » n'est PAS
        # ici : elle est portee par le HEROS (dr001a), seule facon de la faire
        # fonctionner. Raison detaillee dans `__init__.py`.
        AbilityFactory.WhenCardWouldReveal(
            AbilityType.HeroInterrupt,
            "You",
            None,
            protection_mystique,
        ).SetPlay(),
    ]
