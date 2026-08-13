from . import *

# * A Dangerous Game

def GetAbilities() -> Sequence['Ability']:

    def deplacer_la_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(PlayerSideScheme)

        initiator = effect.GetInitiator()
        source = effect.targets[0] if effect.targets else None
        if source is None:
            return
        voulu = initiator.DeclareNumber(0, 4)
        retire = this.RemoveThreatFromSchemes([source], voulu, effect) or 0
        if retire:
            this.PlaceThreatOnSchemes([this], retire, effect)

    def check_seize(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> bool:
        this = effect.this.CastTo(PlayerSideScheme)
        return this.threat >= 16 * Worlds.GetPlayerNumIcon(effect)

    def detonation(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        this = effect.this.CastTo(PlayerSideScheme)

        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 16 * Worlds.GetPlayerNumIcon(effect), effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deplacer_la_menace
        ).SetTarget(Scheme2, another=True),
        AbilityFactory.AfterSchemePlaceThreat(
            AbilityType.ForcedResponse,
            "This",
            detonation,
            conditions=[check_seize],
        ),
    ]
