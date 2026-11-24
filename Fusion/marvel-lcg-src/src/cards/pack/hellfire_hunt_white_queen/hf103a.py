from . import *

# White Queen, forme A (PSIONIC), stade 3 (mode expert). « Incite 1. Steady. » + la meme Reponse forcee que les stades 1 et 2.
# Livret p. 8 : « In Stage 3A, you will see "incite 1" on White Queen, that would place threat on the main scheme when she flips back
# to the PSIONIC form everytime. » Un vilain n'est pas une carte de rencontre « revelee » : le mot-clé natif ne part pas
# (`CanIncite` n'est porte que par les cartes de rencontre non vilain) ; on le code donc ICI, a chaque retournement vers cette
# face. `desc.Incite` est volontairement ABSENT de la fiche : rien ne double l'effet.
# Cartes de reference : tk001a/tk002a Bebop (`AfterCardFlipToThisSide`), RECETTES-MOTEUR « incite » (menace sur le complot principal).


def GetAbilities() -> Sequence['Ability']:
    def retour_en_psionic(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        MenaceSurLeComplotPrincipal(effect, 1)

    return [
        ReponseForceeFormeA(),
        AbilityFactory.AfterCardFlipToThisSide(AbilityType.ForcedResponse, retour_en_psionic),
    ]
