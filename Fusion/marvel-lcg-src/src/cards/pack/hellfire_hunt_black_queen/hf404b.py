from . import *

# Throne of the Hellfire Club (1B). « Forced Interrupt : When Darkhold Dwarf enters the discard pile, advance to stage 2A. »
# « When Completed : Give Selene a tough status card. If Beneath the Sun environment is in play, remove 2[per_hero] time counters from it. »
# Cartes de reference : sk066 Paibok (`WhenCardWouldDiscard`/`WhenCardWouldMoveToArea` sur une AUTRE carte), 50087b (`this.Advance("2A")`),
# hf104b (White Queen : `WhenMainSchemeStageCompleted`).


def GetAbilities() -> Sequence['Ability']:
    def le_dwarf_est_defausse(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        this = effect.this.CastTo(MainScheme)
        if this.IsInPlay():
            this.Advance("2A", effect)

    def terminee(effect: 'Effect', message: 'Message.WhenMainSchemeStageCompleted') -> None:
        selene = Selene(effect)
        if selene is not None:
            Faces.GiveStatus([selene], "Tough", effect)
        if EstLeJour(effect):
            RetirerDuTemps(effect, Temps(effect), 2 * Worlds.GetPlayerNumIcon(effect))

    return [
        AbilityFactory.WhenCardWouldMoveToArea(AbilityType.ForcedInterrupt, CardFinder(name=NOM_DWARF), le_dwarf_est_defausse, into_discard_pile=True),
        AbilityFactory.WhenMainSchemeStageCompleted(AbilityType.ForcedInterrupt, "This", terminee),
    ]
