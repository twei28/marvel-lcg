from . import *

# * The Gentlemen — SBIRE (MYSTIC), Linked (Hush). SCH 2, ATQ 2, PV 4, boost 2.
# While the Gentlemen are engaged with you, you cannot request "Action" abilities from other players.
# When Revealed: You are confused. If you were already confused, discard a support you control.
#
# CARTES DE REFERENCE
#  - `01112` False Alarm : `identity.IsConfused()` puis `Faces.GiveStatus([identity], "Confused", effect)`.
#  - `44032` The Merc with the Mouth / `27153` : `PlayersCannotTriggerAbility(<joueur>, <type d'abilite>, on_which_card=..)`.
#
# TEXTE CONTRE CODE
#  « you were ALREADY confused » -> l'etat est lu AVANT de confondre. « discard a SUPPORT you control » -> un soutien au choix du joueur.
#  « request "Action" abilities from other players » -> `PlayersCannotTriggerAbility("EngagedPlayer", AbilityType.Action, ..)` sur les cartes
#    controlees par un AUTRE joueur. ⚠ lecture : « request » = declencher, par un effet « any player may trigger » ; seul, sans effet.


def GetAbilities() -> Sequence['Ability']:

    def gentlemen(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        etait_confus = identite.IsConfused()
        Faces.GiveStatus([identite], "Confused", effect)
        if etait_confus:
            joueur.DiscardControlCards(effect, support=True)

    def carte_d_un_autre(effect: 'Effect', message: 'Message.CheckEffectCondition') -> bool:
        proprietaire = message.check_effect.this.GetControlByPlayer()
        return proprietaire is not None and proprietaire != message.check_effect.initiator

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            gentlemen,
        ),
        AbilityFactory.PlayersCannotTriggerAbility(
            "EngagedPlayer",
            AbilityType.Action,
            conditions=[carte_d_un_autre],
        ),
    ]
