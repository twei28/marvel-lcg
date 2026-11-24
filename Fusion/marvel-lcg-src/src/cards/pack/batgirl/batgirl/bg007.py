from . import *

# Calculated Counter — evenement, cout 2, [mental]. « Hero Interrupt: When you reveal a card from the encounter deck, cancel the effects
# of that card and discard it. If you paid for this card using only [energy] resources, remove X threat from a scheme or deal X damage
# to an enemy, where X is the number of boost icons discarded this way. »
# Cartes de reference : `01075` Black Widow (`WhenPlayerRevealCard(.., from_encounter=True)` + `CancelAllEffectsAndDiscardIt`,
# `.SetTarget("Trigger")`), `03005` Shield Block (interruption d'evenement : `.SetPlay()`). Icones de boost : `CountBoostIconsInternal()`.


def GetAbilities() -> Sequence['Ability']:

    def calculated_counter(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        joueur = JoueurDeCetteCarte(effect)
        carte = message.trigger
        x = carte.CountBoostIconsInternal() if carte is not None else 0
        message.CancelAllEffectsAndDiscardIt(effect)
        if joueur is None or x <= 0 or not SeulementPaye(effect.GetPaidResources(), Icone(effect, "Y"), effect):
            return

        def retirer_menace(targets) -> None:
            schemes = [f for f in Worlds.GetOnFieldCards(effect) if Scheme2.IsType(f) and f.threat > 0]
            cible = joueur.AskChooseFace(schemes, effect) if schemes else None
            if cible is not None:
                effect.this.CastTo(Event).RemoveThreatFromSchemes([cible], x, effect)

        def infliger(targets) -> None:
            cible = ChoisirUnEnnemi(joueur, effect)
            if cible is not None:
                effect.this.CastTo(Event).DealDamage([cible], x, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(f"Remove {x} threat from a scheme", retirer_menace).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(f"Deal {x} damage to an enemy", infliger).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "You",
            None,
            "All",
            calculated_counter,
            from_encounter=True,
        ).SetPlay()
        .SetTarget("Trigger"),
    ]
