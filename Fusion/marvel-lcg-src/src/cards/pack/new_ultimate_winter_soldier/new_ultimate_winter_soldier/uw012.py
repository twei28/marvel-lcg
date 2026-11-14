from . import *

# "This is Your Enemy" — amelioration signature. Cout 1, [mental].
# Hero form only. Attach to a minion.
# Hero Response: After the attached minion is defeated by Winter Soldier, Winter Soldier draws 3 cards and discards 1 card
# from his hand at random.
#
# Cartes de reference : `uw011` (meme declencheur « after the attached minion is defeated by Winter Soldier » ; ⚠ la fenetre est
# `WhenUnitBeDefeated`, pas `AfterUnitBeDefeated` : voir uw011) ; `01007`
# Spider-Tracer pour l'amelioration attachee a un sbire ; `35012`/`uw008` pour `DiscardRandomHandCards`.
#
# Mots-pieges : « draws 3 cards AND discards 1 at random » (dans cet ordre : la carte piochee peut etre tiree) ; la
# defausse au hasard est une VRAIE defausse au hasard (elle compte pour les Griffes et declenche Winter Mask / Phoenix).


def GetAbilities() -> Sequence['Ability']:

    def tue_par_le_heros(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        return MortParLeHeros(effect, message)

    def this_is_your_enemy(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = this.GetControlByPlayer()
        joueur.DrawUp(3, effect)
        joueur.DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Minion,
        ).SetPlay(hero_form_only=True),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.HeroResponse,
            "AttachedMinion",
            this_is_your_enemy,
            conditions=[tue_par_le_heros],
        ),
    ]
