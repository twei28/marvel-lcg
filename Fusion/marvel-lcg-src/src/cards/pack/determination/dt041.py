from . import *

# Illegal Munitions

def GetAbilities() -> Sequence['Ability']:

    # « Restricted » est un mot-cle que le moteur lit dans le texte, comme
    # Toughness. Reste la clause propre a la carte : elle ne peut pas etre en
    # jeu tant que vous controlez un allie.
    def check_aucun_allie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        initiator = effect.GetInitiator()
        return not initiator.GetAllies()

    def illegal_munitions(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        villain = Worlds.FindVillain(effect)
        if villain:
            Faces.GiveStatus([villain], "Stunned", effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            conditions=[check_aucun_allie]
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "YourHero",
            is_basic_attack=True,
            overkill=True
        ),
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.Response,
            "You",
            Minion,
            illegal_munitions,
            conditions=[lambda effect, message:
                        message.excess_damage >= 2 and message.has_defeated_target],
        ),
    ]
