from cards.pack.conan.conan import *

# Grapple on the Glacier (x2) — traitrise du set nemesis (4/5, 5/5). Boost x2.
# When Revealed: Search the encounter deck and discard pile for a GIANT minion
#   and put it into play engaged with you. Otherwise, take 4 damage.
#
# CARTES DE REFERENCE
#  - fouille pioche + defausse de rencontre : 01114 Klaw
#    (`Search.EncounterCard(effect, include_discard_pile=True, ...)`).
#  - « put it into play engaged with you » : `face.PutIntoPlay(joueur, effect)`
#    (helper `PutThisIntoPlay`, cards/pack/__init__.py), qui engage le sbire
#    avec ce joueur SANS le reveler (pas de When Revealed).
#
# TEXTE CONTRE CODE
#  « a GIANT minion » : trait GIANT (Hrothgar, Hymdul, ou tout autre geant du deck).
#  « Otherwise » : seulement si AUCUN geant n'a ete trouve.


def GetAbilities() -> Sequence['Ability']:

    def grapple(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        if not isinstance(joueur, Player):
            return
        geant = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            trait="GIANT",
            card_type=Minion,
        )
        if geant is not None:
            geant.PutIntoPlay(joueur, effect)
        else:
            this.DealDamage([joueur.GetIdentity()], 4, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            grapple,
        ),
    ]
