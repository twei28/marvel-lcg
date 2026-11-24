from . import *

# Ride Along — AMELIORATION. POWER COSMIC. Temporaire. Cout 1, ressource
# [energy]. x2 (pc011, 2 exemplaires).
#
# Texte imprime : « Temporary. Action: Choose a PLANET and a friendly
# character → that character arrives at that PLANET, then they depart.
# Discard this card. »
#
# CARTES DE REFERENCE
#  - `12003` Giant Stomp (ant_man) : `.SetTarget(...).SetTarget2(...)` pour
#    DEUX cibles de types differents, lues separement
#    (`effect.targets`/`effect.targets2`).
#  - `pc004` Nova Frankie Raye : meme sequence « arrive puis part aussitot »
#    (`ArriverA` puis `Departir`).
#  - `aa010.py` : `Faces.DiscardAll([this], effect)` pour « discard this
#    card » explicite (ameliorations ne se defaussent pas seules comme un
#    evenement).
#
# TEXTE CONTRE CODE
#  « a FRIENDLY character » : `Friend`, jamais un ennemi.
#  « that character arrives... THEN they depart » : les deux dans la meme
#    resolution, pas un aller simple.
#  « Discard this card » : toujours, meme si aucune cible valide n'a pu etre
#    choisie (le texte ne dit pas « if you do »).


def GetAbilities() -> Sequence['Ability']:

    def ride_along(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        Unused(message)
        # `effect.targets2` est une propriete A USAGE UNIQUE (chaque lecture
        # redemande/reaffirme la cible et plante au second appel, voir
        # `effect_context.py:GetTargetsInternal` -- `assert initialized_
        # targets[index] == False`) : la lire UNE SEULE FOIS, modele `12003`
        # Giant Stomp (ant_man), jamais deux fois comme dans une condition
        # ET l'operation.
        planetes = effect.targets
        personnages = effect.targets2
        if planetes and personnages:
            planete = planetes[0]
            personnage = personnages[0]
            ArriverA(effect, personnage, planete)
            Departir(effect, personnage)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            ride_along,
        ).SetTarget(card_type=Support, trait="PLANET")
        .SetTarget2(Friend),
    ]
