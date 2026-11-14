from . import *

# * Meditation Atrium : SOUTIEN (LOCATION), cout 2, [physical]. Unique. Hero Class.
# Alter-Ego Action: Exhaust Meditation Atrium → search the top 3 cards of your deck for a card and add it to your hand. If it is a Mantis card, heal 1 damage from a friendly
# character. Shuffle your deck.
#
# CARTES DE REFERENCE
#  - `rc011` Officer Lewis : Action d'alter-ego d'un soutien a cout `Exhaust("This")`, `HealthUnits(.., effect)` pour le soin.
#  - `jj013` Chase Down a Lead : fouille bornee du dessus du deck + `GainCard` (le melange vient de la fouille).
#  - `mt003` Precognition (meme pack) : meme fouille, meme test « Mantis card ».
#
# TEXTE CONTRE CODE
#  « the top 3 cards » : les 3 du dessus seulement. « If IT is a Mantis card » : la carte prise. « heal 1 damage from A friendly character » : au choix, ami de n'importe quel joueur
#    (`Friend`). Alter-Ego Action : forme alter-ego seulement.
#  Chiffres : cout 2, 3 cartes, 1 soin.


def GetAbilities() -> Sequence['Ability']:

    def meditation_atrium(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        joueur = effect.GetInitiator()
        face = ChercherAuSommet(effect, joueur, 3)
        if face is not None and CarteMantis(face):
            SoignerUnAmi(effect, joueur, this, 1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            meditation_atrium,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
