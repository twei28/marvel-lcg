from . import *

# * Mister Negative — custom « DesignHacker » (némésis de Cloak & Dagger)
# Forced Response: After Mister Negative attacks your hero, flip them to
#   alter-ego form.


def GetAbilities() -> Sequence['Ability']:

    def mister_negative(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        # CORRECTIF (4/8/2026) : `AfterUnitAttackUnit` expose `attacked`,
        # pas `target` (qui n'existe que sur `WhenUnitWouldAttackUnit`).
        # La carte plantait a chaque attaque de Mister Negative.
        cible = message.attacked
        player = cible.GetControlByPlayer()
        if player is None:
            return
        if player.IsHero():
            player.GetIdentity().ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            Hero,
            mister_negative,
        ),
    ]
