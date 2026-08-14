from . import *

# Dark Matter Conversion

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Place 1 additional threat here for each acceleration
        # token and icon in play. »
        this = effect.this.CastTo(EncounterSideScheme)
        valeur = JetonsEtIconesDAcceleration(effect)
        if valeur > 0:
            this.PlaceThreatOnSchemes([this], valeur, effect)

    return [
        # « The villain gets +2 ATK and gains retaliate 1. » Une capacite
        # constante, qui vit tant que la manigance est en jeu.
        #
        # ⚠ Rend une LISTE d'abilites : sans l'etoile, la carte se construit
        # avec une liste dans sa liste et le moteur plante des la generation —
        # et `test_cards` ne le voit pas. Troisieme fois dans cette campagne.
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Villain),
            attack=2,
            retaliate=1,
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
