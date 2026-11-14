from .commun import *

# It's a Trap! (defi 3, p281, ID 6141) : En Sabah Nur (Age of Apocalypse), sets Arcade et Galactic Artifacts. Difficulte 3.
# Regles speciales : (1) « All encounter side schemes gain incite 1, [crisis] and [acceleration] » ; (2) « The villain gains steady » ; (3) complot en 2A.
#
# Cartes de reference : aos/black_widow/50075 (`GiveKeywordToInPlayWhenApplyThis(EncounterCard, incite=1)`), skrull_menace/skrull_empire/sk093 (crise par `apply` +
# `GainCrisis`), sm/guerrilla_tactics/27143 (`acceleration_icon=1`), 2412 (complot en 2A).
# Decisions de l'utilisateur (19/10/2026) : les deux icones sont Crise et Acceleration (le site ecrit a tort « amplify »).


def GetAbilities() -> Sequence['Ability']:

    def crise(effect: 'Effect', face: 'CardFace', diff: int) -> None:
        face.GainCrisis(diff, effect)

    def de_rencontre(effect: 'Effect', face: 'CardFace') -> int:
        # « encounter side schemes » : pas les annexes de joueur
        return 1 if EncounterCard.IsType(face) else 0

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=SchemeSide2), incite=1, acceleration_icon=1, apply=crise, get_new_value=de_rencontre),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Villain, steady=1),
        ComplotEn2A(),
    ]
