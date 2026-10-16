from . import *

# Road to Ruin

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        lieux = LieuxAmis(effect)

        def defausser(targets):
            for f in targets:
                Faces.DiscardAll([f], effect)

        def etourdir(targets):
            Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Discard a friendly LOCATION", defausser,
                                            condition=bool(lieux)
                                            ).SetTarget(Support, trait="LOCATION"),
            # « Stun your hero » : la forme HEROS seulement (TODO-QUESTION Q4).
            AbilityFactory.ForChoiceAbility("Stun your hero", etourdir,
                                            condition=joueur.IsHero()),
        )

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurVainqueur(message, effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                lambda targets: Faces.GiveStatus(targets, "Stunned", effect)
            ).SetTarget(Enemy, canbe_stunned=True),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        BoostReveleCetteCarte(),
    ]
