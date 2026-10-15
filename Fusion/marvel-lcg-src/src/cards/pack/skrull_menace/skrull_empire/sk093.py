from . import *

# Skrullos — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Each side scheme gains the crisis icon ([crisis]).
#
# Carte(s) de reference : **`st016`** (`GiveKeywordToInPlayWhenApplyThis(..., apply=...)`) + `GainCrisis` (has_crisis.py) ; **`40109`** Pure Force pour une crise conditionnelle.
#
# ⚠ « Each side scheme » : annexes rencontre ET side schemes de joueur (`SchemeSide2`). Crise = verrou du contre sur le principal (fiche crisis.md).
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    def crise(effect: 'Effect', face: 'CardFace', diff: int) -> None:
        face.GainCrisis(diff, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=SchemeSide2), apply=crise),
    ]
