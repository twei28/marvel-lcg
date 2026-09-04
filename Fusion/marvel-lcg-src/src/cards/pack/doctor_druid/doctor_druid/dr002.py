from . import *

# * Doctor Strange (Stephen Strange) — ALLIE, cout 3, PV 3, THW 2* / ATK 1*.
# AVENGER. MYSTIC.
# While this card is in your hand Doctor Druid ignores the guard keyword, the
#   patrol keyword, and the crisis icon.
# Response: After Doctor Strange attacks or thwarts, return the topmost event
#   from your discard pile into your hand.
#
# CARTES DE REFERENCE
#  - `as012` (armored_spidey) pour `UnitIgnoreKeywordIcons`. ⚠ LECON PAYEE
#    LA-BAS : passer "You" sur une carte qui n'est PAS l'identite ne marche
#    pas, le moteur le traduit en "This" et compare a `effect.this`. On vise
#    donc le heros par son NOM.
#  - `friend.py` `AfterUnitUseBasicPower` pour « after ... attacks or thwarts ».
#
# TEXTE CONTRE CODE
#  « While this card is in your HAND » -> `DepuisLaMain(...)`, donc
#    `CanWorkOnlyInHand()`. C'est la moitie qui compte : jouer l'allie fait
#    PERDRE cet effet.
#  « the crisis icon » -> `crisis=True` du meme appel, pas un mot-cle separe.
#  « attacks or thwarts » -> `powers=["ATK", "THW"]`, donc les pouvoirs de
#    BASE de l'allie ; ce n'est pas « quand il inflige des degats ».
#  « the TOPMOST event » -> derniere carte posee, on parcourt a l'envers.


def GetAbilities() -> Sequence['Ability']:

    def rendre_un_evenement(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for face in reversed(list(joueur.discard_pile.Get(True))):
            if Event.IsType(face):
                Faces.ReturnToHand([face], "Owner", effect)
                return

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        *DepuisLaMain([
            AbilityFactory.UnitIgnoreKeywordIcons(
                CardFinder(name=NOM_HEROS),
                guard=True,
                patrol=True,
                crisis=True,
            ),
        ]),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            rendre_un_evenement,
            powers=["ATK", "THW"],
        ),
    ]
