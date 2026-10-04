from . import *

# Crimson Bands of Cyttorak

def GetAbilities() -> Sequence['Ability']:

    def crimson_bands_of_cyttorak(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        Faces.GiveStatus(effect.targets, "Stunned", effect)

        this.DealDamage(effect.targets, 7, effect)
        PlaceThisCardInInvocationDeckDiscardPile(this, effect)

    return [
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            crimson_bands_of_cyttorak
        # « Stun AN enemy » : une cible, obligatoire. `range=(0, 1)` ouvrait l'ecran
        # de choix avec « 0/1 selectionnee(s) » et son bouton de confirmation
        # ACTIF : valider sans cliquer l'ennemi resolvait le sort a vide, qui
        # partait quand meme a la defausse (signalement n°51, 04/10/2026).
        ).SetTarget(Enemy)
        .NoOutOfPlayLimit(),
    ]

