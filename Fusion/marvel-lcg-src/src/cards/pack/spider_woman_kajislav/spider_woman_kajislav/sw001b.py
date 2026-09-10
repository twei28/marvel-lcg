from . import *

# * Julia Carpenter — FACE ALTER-EGO. REC 3, main 6, 10 PV. CIVILIAN.
# Setup: Place 5 psionic web counters on your identity.
# Proper Relaxation — Action: Exhaust Julia Carpenter -> place 3 psionic web
#   counters on her (to a maximum of 10).
#
# ⚠⚠ C'EST LA CARTE QUI REMPLIT LE STOCK. Le pack entier se joue sur le rythme
# « Julia recharge, Spider-Woman depense » : 5 au montage, 3 par passage en
# forme civile, plafond 10.
#
# CARTES DE REFERENCE
#  - `al001b` * Alligator Loki : le Setup d'une IDENTITE passe par
#    `AbilityFactory.WhenCardSetup("This", op)` (setup.py:206), qui tourne a
#    l'etape « Capacites de mise en place des personnages », DECK DEJA
#    CONSTRUIT. ⚠ Son en-tete garde la lecon : `WhenPlayerSelectHero` se
#    declenche AVANT la creation du deck du joueur, et une premiere version
#    d'al001b y perdait sa recherche.
#  - `Faces.PlaceCountersOn(..., maximum=)` (faces.py:206) : le plafond est un
#    parametre du moteur, on ne le recalcule pas a la main.
#
# TEXTE CONTRE CODE
#  ⚠ « on your IDENTITY » (Setup) et « on HER » (Action) designent la MEME
#    carte : le stock ne se perd pas au changement de forme. Tout le pack passe
#    par `IdentiteDe`, jamais par la face courante.
#  ⚠ Le Setup N'A PAS de plafond imprime, l'Action si — mais 5 puis 3 ne
#    peuvent pas depasser 10, et `PoserDesToiles` applique le plafond aux deux
#    sans rien changer au premier.
#  ⚠ « Action », pas « Alter-Ego Action » : le texte n'a pas besoin de le
#    preciser, la carte n'existe qu'en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        PoserDesToiles(effect.GetInitiator(), 5, effect)

    def relaxation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        PoserDesToiles(effect.GetInitiator(), 3, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            relaxation,
        ).SetName("Proper Relaxation")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
