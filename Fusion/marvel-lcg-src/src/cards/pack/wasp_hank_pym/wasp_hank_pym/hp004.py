from . import *
# Resize at Will — x3. Action : change de forme. Puis, selon la forme : GIANT -> attaque de base sans incliner ;
# TINY -> menee de base sans incliner ; alter ego -> pioche 2.
def GetAbilities() -> Sequence['Ability']:
    def resize(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        changer_de_forme(effect)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        if AlterEgo.IsType(identite):
            joueur.DrawUp(2, effect)
        elif joueur.IsInHeroForm("GIANT"):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Make a basic attack without exhausting",
                    lambda cibles: identite.BasicAttack(cibles, effect),
                ).SetTarget(Enemy),
            )
        elif joueur.IsInHeroForm("TINY"):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Make a basic thwart without exhausting",
                    lambda cibles: identite.BasicThwart(cibles, effect),
                ).SetTarget(Scheme2),
            )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            resize,
        ).SetPlay(),
    ]
