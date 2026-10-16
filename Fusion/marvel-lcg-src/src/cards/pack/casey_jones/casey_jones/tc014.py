from . import *

# Daddy Issues — OBLIGATION. 2 icones de boost (deux icones rouges lues sur le
# scan). Bandeau « CASEY JONES » (set du HEROS, donc module dans
# casey_jones/casey_jones/, PAS dans casey_jones_nemesis/ : piege bt019).
# Give to the Casey Jones player.
# Flip to alter-ego form. You cannot change forms.
# Action: Exhaust Casey Jones → remove Daddy Issues from the game.
#
# CARTES DE REFERENCE
#  - `raphael/tr013` Out of Control : meme squelette (`WhenThisObligationGiveToYou`
#    + `PlayersCannotChangeForms(NonKeyword, "AttachedPlayer")`, qui EXCLUT deja
#    l'effet de sa propre carte) ; ici l'inverse (alter-ego) et AUCUN interdit de
#    contrer / defendre.
#  - `donatello/td013` Broken Shell : `PlayerActionToRemoveThisFromGame(...)` et
#    bascule heros -> alter-ego par `ChangeToOtherIdentityForm`.
#  - `CostFunc.Exhaust("YourIdentity")` : incliner l'identite en cout.
#
# TEXTE CONTRE CODE
#  ⚠ « Flip to alter-ego form » : obligatoire a la reception, sans effet si
#    l'identite est deja en alter-ego. L'identite n'est PAS inclinee par la carte.
#  ⚠ « You cannot change forms » : les DEUX sens, tant que la carte est en jeu.
#  ⚠ « Action » (pas Hero Action ni Alter-Ego Action) : jouable dans la forme
#    imposee. « Exhaust CASEY JONES » = l'IDENTITE (cout ; un identite deja
#    inclinee ne peut pas payer).
#  ⚠ « remove Daddy Issues FROM THE GAME » : `RemoveAllFromGame`, pas la defausse.
#  ⚠ `desc.GiveTo = "Casey Jones"` : le nom de l'ALTER-EGO (identique a celui du
#    heros : « Casey Jones »).


def GetAbilities() -> Sequence['Ability']:

    def daddy_issues(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)

        joueur = message.GetGaveToPlayer()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is not None and Hero.IsType(identite):
            identite.ChangeToOtherIdentityForm(effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(daddy_issues),
        AbilityFactory.PlayersCannotChangeForms(
            AbilityType.NonKeyword,
            "AttachedPlayer",
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.Action,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
