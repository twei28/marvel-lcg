from . import *

# Triggered Transformation

def GetAbilities() -> Sequence['Ability']:

    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        CompleterHonte(effect)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        heros_pret = Hero.IsType(identite) and identite.IsReady()

        def epuiser(cibles):
            Faces.ExhaustAll([joueur.GetHero()], effect)

        def manigancer(cibles):
            v = Vilain(effect)
            if v is not None:
                v.CastTo(Enemy).DoSchemes(joueur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust your hero", epuiser, condition=heros_pret),
            AbilityFactory.ForChoiceAbility("The villain schemes", manigancer),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        PlacerHonte(effect, 1)

    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
