from . import *

# * Albert — custom « Kajislav »
# Initiate Protocol — Special: Draw 1 card. After you play that card this
# round, ready Albert.
# Action: Resolve Albert's "Initiate Protocol" ability. (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def initiate_protocol(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Hero)

        # Counterpart Elimination : « You cannot resolve Albert's
        # "Initiate Protocol" ability. »
        if Worlds.FindCardsOnField(effect, name="Counterpart Elimination", card_type=Obligation):
            return

        player = effect.GetInitiator()
        drawn = player.DrawUp(1, effect)
        if not drawn:
            return
        face = drawn[0]

        def ready_albert(e2: 'Effect', m2: 'Message.AfterPlayerPlayedCard') -> None:
            Faces.ReadyAll([player.GetIdentity()], e2)

        this.effect.RegisterTemp(
            AbilityFactory.AfterPlayerPlayedCard(
                AbilityType.Temp0,
                # « You », surtout pas None : Condition.CheckWhichPlayer n'a pas
                # de return final, une regle a None y rend None — donc faux — et
                # le declencheur ne partait JAMAIS. Albert ne se redressait pas.
                'You',
                face,
                ready_albert,
            ),
            unregister_after_exec=True,
            until_round_end=True,
        )

    def resolve_protocol(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        initiator = effect.GetInitiator()
        initiator.ResolveSpecialAbility([this], effect)

    return [
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            initiate_protocol,
        ).SetName("Initiate Protocol"),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            resolve_protocol
        ).SetName("Initiate Protocol")
        .LimitOncePerRound(),
    ]
