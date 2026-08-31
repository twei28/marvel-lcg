from . import *

# * Pixie (Megan Gwynn) — alliee d'aspect LEADERSHIP (carte bonus du pack).
# AERIAL. MYSTIC. X-MEN. Cout 2 / PV 2 / THW 1* / ATK 2**
# Response: After you play Pixie from your hand, add an X-MEN ally from your
#   discard pile to your hand.
#
# Cartes de reference (RECETTES) : 31022 * Spider-Man (« After you play
# Spider-Man from your hand ») → `AfterPlayerPlayedCard(..., "This", ...,
# from_hand=True)` (play.py), et 01034 Stark Tower pour la remontee
# (`Faces.ReturnToHand`). La cible passe par le selecteur
# (`from_where=["YourDiscardPile"]`).
#
# ⚠ Homonyme : 36017, alliee Leadership OFFICIELLE de la MEME classe — la
# regle d'unicite ne laisse qu'une * Pixie en jeu par table.
# ⚠ « from YOUR discard pile » : la sienne, pas celle d'un autre joueur.

def GetAbilities() -> Sequence['Ability']:

    def pixie(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        initiator = effect.GetInitiator()
        cibles = [t for t in effect.targets if t is not None]
        if cibles and initiator is not None:
            Faces.ReturnToHand(cibles, initiator, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            "This",
            pixie,
            from_hand=True,
        ).SetTarget(CardFinder(card_type=Ally, trait="X-MEN"),
                    range=(1, 1), from_where=["YourDiscardPile"]),
    ]
