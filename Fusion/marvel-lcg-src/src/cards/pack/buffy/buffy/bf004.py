from . import *

# Bring on the Night — EVENEMENT, cout 2, [mental]. x2.
# Hero Interrupt: When an encounter card is revealed from the encounter deck, cancel all of its effects and discard it.
# Deal damage to an enemy or remove threat from a scheme equal to the number of HELLMOUTH side schemes in the victory display.
#
# CARTES DE REFERENCE
#  - `09007` Protective Ward : `WhenPlayerRevealCard(HeroInterrupt, "AnyPlayer", <type>, "All", op, from_encounter=True).SetPlay()` +
#    `message.CancelAllEffectsAndDiscardIt(effect)`.
#  - `01075` Black Widow : meme fabrique avec `None` comme type de carte (« a card », pas seulement une traitrise).
#  - `01xxx`/`wsp/13013` : `initiator.ChooseAbilities(effect, ForChoiceAbility(.., fn).SetTarget(..))` pour « X or Y ».
#
# TEXTE CONTRE CODE
#  « an encounter card » -> TOUT type de carte (sbire, traitrise, manigance...), pas seulement les traitrises de Protective Ward.
#  « cancel all of its effects and discard it » -> `CancelAllEffectsAndDiscardIt`, AVANT le choix.
#  « equal to the number of HELLMOUTH side schemes in the victory display » -> le nombre est lu a la resolution. A zero, la
#    carte annule quand meme la revelation mais n'inflige ni ne retire rien.
#  « deal damage to an enemy OR remove threat from a scheme » -> UN seul des deux, au choix.


def GetAbilities() -> Sequence['Ability']:

    def bring_on_the_night(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        nombre = NombreDeHellmouthEnVictoire(effect)

        message.CancelAllEffectsAndDiscardIt(effect)

        if nombre <= 0 or joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal damage to an enemy",
                lambda targets:
                    this.DealDamage(targets, nombre, effect),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove threat from a scheme",
                lambda targets:
                    this.RemoveThreatFromSchemes(targets, nombre, effect),
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            None,
            "All",
            bring_on_the_night,
            from_encounter=True,
        ).SetPlay(),
    ]
