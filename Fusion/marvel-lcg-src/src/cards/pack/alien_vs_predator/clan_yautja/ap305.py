from . import *

# The Hunt Begins — MANIGANCE ANNEXE. Menace 5 (fixe). Boost 2.
# Allies cannot defend against enemy attacks.
# Forced Response: After a [[YAUTJA]] enemy attacks, give it a tough status card.
# When Defeated: Stun or confuse an enemy.
#
# Cartes de reference : `UnitCannotDefend(Ally, Enemy, cannot_trigger_defense_ability=True)` (27152) ; « After X attacks » :
#   `AfterUnitAttackEnd(ForcedResponse, ..)` ; « When Defeated » d'une manigance : `WhenSchemeBeDefeated(WhenDefeated, "This")` (tk).
#
# ⚠ Mots-pieges : « ALLIES cannot defend » (le heros, si) ; « a YAUTJA ENEMY » : mechant ou sbire YAUTJA ; « stun OR confuse AN enemy » :
#   le joueur qui la vainc choisit l'ennemi ET l'etat.


def GetAbilities() -> Sequence['Ability']:

    def tenace(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        if message.trigger.IsInPlay():
            Faces.GiveStatus([message.trigger], "Tough", effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = getattr(message, "defeating_player", None)
        if not Player.IsType(joueur):
            joueur = Worlds.GetFirstPlayer(effect)
        ennemis = list(Worlds.GetOnFieldEnemies(effect))
        if not ennemis:
            return
        cible = joueur.AskChooseFace(ennemis, effect, prompt="Stun or confuse an enemy") or ennemis[0]
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Stun", lambda targets: Faces.GiveStatus([cible], "Stunned", effect)),
            AbilityFactory.ForChoiceAbility("Confuse", lambda targets: Faces.GiveStatus([cible], "Confused", effect)),
        )

    return [
        *AbilityFactory.UnitCannotDefend(Ally, Enemy, cannot_trigger_defense_ability=True),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, CardFinder(card_type=Enemy, trait="YAUTJA"), tenace),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
