from cards.pack import *

################################################################################
# Capacités partagées par les deux identités de The Thing — custom
# « DesignHacker ». Le pack fournit deux couples d'identités au texte
# identique : le classique (67001a/67001b) et la variante Guardian
# (67001c/67001d, l'époque où Ben Grimm voyageait avec les Gardiens de la
# Galaxie). Les scripts des quatre faces appellent ces fabriques.
################################################################################


def AbilitesFaceHeros() -> Sequence['Ability']:
    """Give 'Er + Take That! — communes à 67001a et 67001c."""

    def give_er(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        this.DiscardTough(effect, rule=1)

    def take_that(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Hero)

        # « Your attacks deal 1 additional damage until the end of the phase. »
        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "You",
                lambda e, m: m.DealAdditionalDamage(1, e),
            ),
            unregister_after_exec=False,
            until_phase_end=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            give_er,
            conditions=[lambda effect, message: effect.this.IsTough()],
        ).SetName("Give 'Er"),

        AbilityFactory.AfterStatusDiscardFrom(
            AbilityType.Response,
            "This",
            "Tough",
            take_that,
        ).SetName("Take That!"),
    ]


def AbilitesFaceAlterEgo() -> Sequence['Ability']:
    """Ever-Lovin' Blue-Eyed Thing — commune à 67001b et 67001d.

    Aucune fabrique n'expose le message générique de soin : l'Ability est
    construite à la main sur `Message.AfterUnitHealHealth`, dont le champ
    `value` porte le nombre de points rendus.
    """

    def ever_lovin(effect: 'Effect', message: 'Message.AfterUnitHealHealth') -> None:
        this = effect.this.CastTo(AlterEgo)
        Faces.GiveStatus([this], "Tough", effect)

    return [
        Ability(
            AbilityType.Response,
            Message.AfterUnitHealHealth,
            [
                lambda effect, message:
                    effect.this == message.trigger and message.value >= 4
            ],
            ever_lovin,
            is_local=True,
        ).SetName("Ever-Lovin' Blue-Eyed Thing"),
    ]
