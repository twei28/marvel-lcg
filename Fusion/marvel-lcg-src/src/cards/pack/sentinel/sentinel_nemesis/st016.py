from . import *

# Rogue Asset — MANIGANCE ANNEXE NEMESIS, 3 menaces de depart, 3 icones de
# boost.
# [[COMPONENT]] upgrades ([[INTACT]] side up), and [[TECH]] upgrades gain the
#   [[HACKED]] trait.
#
# Cartes de reference :
#  - `04092` Super Absorbing Power : donner des TRAITS depuis une carte en jeu,
#    `GiveKeywordToInPlayWhenApplyThis(..., apply=...)` avec `GainTraits`.
#  - `03025` Honorary Avenger pour la forme simple `trait=`.
#
# ⚠ MOT-CLE DE LIAISON DU PACK. Trois cartes nemesis (`st017` Disabled,
# `st018` Viral Assault, `st019` Hostile Override) ne font RIEN tant que cette
# manigance n'est pas en jeu : c'est elle qui cree les ameliorations HACKED.
# Deux d'entre elles vont d'ailleurs la CHERCHER quand elles n'en trouvent pas.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - DEUX familles distinctes : les Component **face INTACT** d'une part, les
#    ameliorations **TECH** d'autre part. Un Component DETRUIT n'est plus
#    HACKED — retourner une piece la « desinfecte », et c'est une vraie
#    decision de jeu.
#  - Les trois Component intacts portent DEJA le trait TECH : ils entrent par
#    les deux portes, sans double comptage possible (un trait est present ou
#    non).
#  - Le trait vaut pour les ameliorations de TOUS les joueurs, pas seulement
#    celles de Sentinel : la manigance ne dit pas « you control ».


def GetAbilities() -> Sequence['Ability']:

    def pirater(effect: 'Effect', face: 'CardFace', diff: int) -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        face.GainTraits(diff, [TRAIT_HACKED], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Upgrade, trait=TRAIT_INTACT),
            apply=pirater,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Upgrade, trait="TECH"),
            apply=pirater,
        ),
    ]
