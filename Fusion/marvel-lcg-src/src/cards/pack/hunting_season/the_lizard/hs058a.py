from . import *

# hs058a Reptile Brain Taking Over
# When Revealed : cherche Reptile Research (deck et defausse de rencontre) et le
# revele. Le passage en 2B est fait par le moteur (face A sans seuil de menace).

def GetAbilities() -> Sequence['Ability']:

    def recherche(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(
            effect, Worlds.GetFirstPlayer(effect),
            finder=CardFinder(name="Reptile Research", card_type=EncounterSideScheme,
                              check_face_fn=lambda f: not f.IsInPlay()),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, recherche),
    ]
