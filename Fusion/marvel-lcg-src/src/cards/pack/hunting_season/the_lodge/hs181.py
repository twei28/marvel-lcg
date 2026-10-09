from . import *

# hs181 Fresh Tracks (Experience Cost 2)
# Interrupt : quand tu contres, ce contre retire 2 menaces de plus. S'il retire la
# derniere menace d'un complot, 1 degat a un ennemi et pioche 1 carte.

def GetAbilities() -> Sequence['Ability']:

    def pister(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this
        joueur = effect.GetInitiator()
        message.RemoveAdditionalThreat(2, effect)

        def blesser(cibles: Sequence['CardFace']) -> None:
            this.DealDamage(cibles, 1, effect)

        def apres(e: 'Effect', m: 'Message.AfterUnitThwartEnd') -> None:
            if not m.remove_the_last_threat:
                return
            if Worlds.FindCardsOnField(effect, card_type=Enemy):
                joueur.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility("Deal 1 damage to an enemy", blesser).SetTarget(Enemy),
                )
            joueur.DrawUp(1, effect)

        this.effect.RegisterTemp(
            Ability(AbilityType.Temp2, Message.AfterUnitThwartEnd,
                    [lambda e, m: message in m.would_thw_messages], apres),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenUnitWouldThwart(AbilityType.Interrupt, "You", pister).SetPlay(),
    ]
