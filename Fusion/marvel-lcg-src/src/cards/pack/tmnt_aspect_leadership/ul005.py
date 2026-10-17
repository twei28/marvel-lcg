from . import *

# * Dask — ALLIE Leadership (TMNT, Inkwire), cout 3, [energy]. DIMENSION X. NEUTRINO. SOLDIER.
# THW 2* / ATQ 2* / PV 3.
# Response: After Dask enters play, look at the top 3 cards of the encounter deck. For each treachery
#   looked at this way, deal 1 damage to an enemy. Put them back in any order.
#
# MODIFIEE (derivee de `03011` Falcon) : « remove 1 threat from a scheme » -> « deal 1 damage to an
# enemy », et « Put them back in any order » ajoute. Pas d'`ability_link` : script propre.
#
# CARTES DE REFERENCE
#  - `03011` Falcon : `LookAtDeck("EncounterDeck", 3)` + compte des traitrises
#    (`Faces.FindCardSize(faces, CardFinder(card_type=Treachery))`).
#  - `06020` Heimdall : « put the others back in any order » = `PlaceOnTopInAnyOrder(faces)`.
#  - `03013` Squirrel Girl : « deal 1 damage » d'un allie = `this.DealDamage(cibles, 1, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « FOR EACH treachery » : un degat PAR traitrise, chacun vers un ennemi choisi a ce moment
#    (le meme ennemi peut etre choisi plusieurs fois ; un ennemi vaincu par le premier degat ne peut
#    plus etre choisi). OBLIGATOIRE une fois la Reponse declenchee (pas « up to »).
#  ⚠ « an enemy » : vilain ou sbire.
#  ⚠ « Put THEM back » : les 3 cartes regardees, sur le dessus du deck de rencontre, dans l'ordre choisi.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def dask(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = effect.GetInitiator()
        faces = joueur.LookAtDeck("EncounterDeck", 3, effect)
        nombre = Faces.FindCardSize(faces, CardFinder(card_type=Treachery))

        for _ in range(nombre):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 1 damage to an enemy",
                    lambda cibles: this.DealDamage(cibles, 1, effect),
                ).SetTarget(Enemy),
            )

        joueur.PlaceOnTopInAnyOrder(list(faces), effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            dask,
        ),
    ]
