from . import *

# Stop the Presses! 1B — 1[per_hero], cible 9[per_hero], +1[per_hero] : bases.
# Forced Response: After an enemy makes an undefended attack against you,
#   choose: • Place 2 threat here (3 threat instead in expert mode).
#   • Remove 1 stamina counter from a DAILY BUGLE support you control.
# If a DAILY BUGLE support leaves play or this stage is completed, the
#   players lose the game.
# AfterUnitAttackUnit(Enemy, Identity, is_undefended_attack=True) (60121b) ;
# la seconde branche n'est offerte que si le joueur controle un tel soutien.

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(MainScheme)
        identite = message.attacked
        joueur = identite.GetControlByPlayer()
        if joueur is None:
            return
        n = 3 if Worlds.IsExpert(effect) else 2

        def menace(targets: Sequence['CardFace']) -> None:
            this.PlaceThreatOnSchemes([this], n, effect)

        def endurance(targets: Sequence['CardFace']) -> None:
            soutiens = SoutiensDailyBugle(effect, joueur)
            if not soutiens:
                return
            cible = soutiens[0] if len(soutiens) == 1 else joueur.AskChooseFace(soutiens, effect)
            if cible is not None:
                RetirerUneEndurance(cible, effect)

        # ⚠ ForChoiceAbility n'a pas de `conditions` : `condition` est un booleen
        # evalue a la construction (juste avant le choix, ce qui suffit ici).
        a_un_soutien = bool(SoutiensDailyBugle(effect, joueur))
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(f"Place {n} threat on Stop the Presses!", menace),
            AbilityFactory.ForChoiceAbility("Remove 1 stamina counter from a Daily Bugle support you control", endurance, condition=a_un_soutien),
        )

    def perdu(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, Enemy, Identity, apres_attaque, is_undefended_attack=True),
        AbilityFactory.WhenCardLeavePlay(AbilityType.ForcedInterrupt, CardFinder(trait="DAILY BUGLE", card_type=Support), perdu),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
