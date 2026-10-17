from . import *

# * Two-Gun Kid: Matthew Hawk

def GetAbilities() -> Sequence['Ability']:

    def two_gun_kid(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        message.AddTarget(*effect.targets)


    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.Interrupt,
            "This",
            two_gun_kid,
            is_basic_attack=True
        # CORRECTIF (16/10/2026, aspect TMNT Aggression ua022 He-Dude, reskin de cette carte) :
        # « choose 2 enemies instead of 1 » = deux ennemis DIFFERENTS. Le selecteur proposait aussi
        # l'ennemi deja vise : `AddTarget` le doublait et il encaissait l'attaque deux fois (4 degats
        # sur Rhino, 0 sur le 2e ennemi, mesure par `[ua] ua022` / temoin 56010). `exclude="Targets"`
        # (selector_filter.py) retire les cibles deja portees par l'attaque.
        ).SetTarget(Enemy, exclude="Targets"),
    ]

