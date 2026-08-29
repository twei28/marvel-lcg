from . import *

# Joys of Life
# Alliance.
# Action: Choose:
# • Exhaust a [[Civilian]] alter-ego → ready a hero or ally.
# • Exhaust a hero or ally → ready a [[Civilian]] alter-ego.
#
# Les deux options sont EXCLUSIVES et chacune lie le type de la carte epuisee a
# celui de la carte degagee. L'ancienne version fusionnait les deux reservoirs,
# ce qui autorisait « epuiser un heros puis degager un heros ». Elle appelait en
# plus `.Exhaust()` / `.Ready()` sur une face, qui n'existent pas : le moteur
# passe par `Faces.ExhaustAll` / `Faces.ReadyAll`.

ALTER_EGO_CIVIL = CardFinder(card_type=AlterEgo, trait='CIVILIAN')
HEROS_OU_ALLIE = CardFinder(card_type=Hero) | CardFinder(card_type=Ally)


def GetAbilities() -> Sequence['Ability']:

    def option(epuiser_finder: 'CardFinder', degager_finder: 'CardFinder', libelle: str):
        def action(cibles: Sequence['CardFace']):
            if not cibles:
                return
            effet = action.effet
            Faces.ExhaustAll(list(cibles), effet)
            joueur = effet.GetInitiator()

            def degager(a_degager: Sequence['CardFace']):
                Faces.ReadyAll(list(a_degager), effet)

            joueur.ChooseAbilities(
                effet,
                AbilityFactory.ForChoiceAbility(libelle, degager)
                .SetTarget(degager_finder, range=(1, 1)),
            )
        return action

    def joys_of_life(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()

        a = option(ALTER_EGO_CIVIL, HEROS_OU_ALLIE, 'Degager un heros ou un allie')
        b = option(HEROS_OU_ALLIE, ALTER_EGO_CIVIL, 'Degager un alter-ego Civilian')
        a.effet = effect
        b.effet = effect

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                'Epuiser un alter-ego Civilian pour degager un heros ou un allie', a)
            .SetTarget(ALTER_EGO_CIVIL, range=(1, 1)),
            AbilityFactory.ForChoiceAbility(
                'Epuiser un heros ou un allie pour degager un alter-ego Civilian', b)
            .SetTarget(HEROS_OU_ALLIE, range=(1, 1)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, joys_of_life).SetPlay(),
    ]
