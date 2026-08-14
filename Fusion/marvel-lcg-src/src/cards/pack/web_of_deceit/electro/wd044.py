from . import *

# A.I.M. Scientist (version campagne)

def GetAbilities() -> Sequence['Ability']:

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « When Defeated: Search the encounter deck and discard pile for the
        # Dark Matter Conversion side scheme and reveal it. »
        #
        # ⚠ Le LIVRET p.17 montre un autre texte (« if Dark Matter Conversion is
        # in play, place 1 threat on it »). La carte du Drive fait foi, le livret
        # est en retard : c'est deja ce que le lot 1 avait mesure sur Shocker.
        ChercherEtReveler(effect, name="Dark Matter Conversion")

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
