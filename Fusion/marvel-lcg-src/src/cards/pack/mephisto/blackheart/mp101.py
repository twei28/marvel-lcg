from . import *

# * Blackheart — SBIRE ELITE (BRUTE, MYSTIC). PV 9, ATK 2, SCH 2, Boost 2, Toughness 1, Villainous (natifs, `desc`).
# Action : Discard a BARGAIN attachment you control -> heal 3 damage from Blackheart. If no damage was healed this way, give him a tough status card.
# [star] Boost : You may discard a BARGAIN attachment to cancel this activation. If you do, put Blackheart into play engaged with you.
#
# Cartes de reference : sl073 (boost qui annule : `message.would_atk_message.CancelThisAttack`), `Minion.EngagePlayer` (minion.py), mp008 (choix d'un pacte),
# `CostFunc.Discard(Select.From(..))` (mf013), `Faces.GiveStatus`.
# ⚠ Mots-pieges : « a BARGAIN attachment YOU CONTROL » : ceux de l'identite de CE joueur ; « If NO DAMAGE was healed » : compare les degats avant/apres (un
# Blackheart sans degats recoit Tough) ; Boost « you MAY » : facultatif ; « cancel THIS ACTIVATION » : l'attaque OU la manigance de l'ennemi qui active ; Blackheart
# arrive engage avec le joueur VISE par l'activation.


def GetAbilities() -> Sequence['Ability']:
    def soigne(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Minion)
        avant = this.sustained
        this.HealHealth(3, effect)
        if this.sustained == avant:
            Faces.GiveStatus([this], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        if joueur is None or not PactsDuJoueur(joueur):
            return

        def annule(targets: Any) -> None:
            pacte = Search.SearchForCard(effect, joueur, faces=PactsDuJoueur(joueur), not_move=True)
            if pacte is None:
                return
            Faces.DiscardAll([pacte], effect)
            # ⚠ Le Boost est retourne quand l'activation est DEJA en cours : `CancelThisAttack` (annulation avant l'attaque) ne change plus rien ;
            # on empeche tous les degats de CETTE attaque / on retire toute la menace de CETTE manigance.
            if hasattr(message, "would_atk_message"):
                message.would_atk_message.PreventDamage("All", effect)
            elif hasattr(message, "would_sch_message"):
                message.would_sch_message.GainSCHForThisScheme(-1000, effect)
            this.EngagePlayer(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Discard a BARGAIN attachment to cancel this activation and put Blackheart into play engaged with you", annule),
            forced=False,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, soigne)
        .SetCostFunc(CostFunc.Discard(Select.From(lambda effect: PactsDuJoueur(Select.GetYou(effect))))),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
