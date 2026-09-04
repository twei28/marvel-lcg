from . import *

# Tough Motherlover — evenement signature, x1 (n/15 = 5). CONDITION.
# Cout 1, ressource [physical].
# Action: Give your identity a tough status card. Then, if you have the Yaka
#   Arrow upgrade in your hand, draw a card.
#
# Cartes de reference :
#  - `05015` / `01083` / `as006` pour `Faces.GiveStatus(cibles, "Tough",
#    effect)`.
#  - `bt023` / `an001b` pour `initiator.DrawUp(1, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « if you have the Yaka Arrow upgrade **IN YOUR HAND** » : la MAIN, pas le
#    terrain. C'est la SEULE carte du pack qui recompense une fleche NON
#    posee, et c'est ce qui donne un interet a la garder un tour. Un
#    `LaFleche(effect)` — qui balaie le terrain — serait le contresens exact.
#  - « **Action** » nue, pas « Hero Action » : la carte se joue dans les DEUX
#    formes, ce qui est rare dans ce pack et rend le statut Tenace accessible
#    en civil, juste avant de repasser en heros.
#  - « give **your identity** a tough status card » : l'identite courante,
#    quelle que soit la forme.
#  - « draw **a** card » : une seule.


def GetAbilities() -> Sequence['Ability']:

    def tough_motherlover(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        Faces.GiveStatus([identite], "Tough", effect)

        # « in your HAND » : le terrain ne compte pas.
        for face in joueur.hand_cards.Get():
            if face.IsName(NOM_FLECHE):
                joueur.DrawUp(1, effect)
                return

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            tough_motherlover,
        ).SetPlay(),
    ]
