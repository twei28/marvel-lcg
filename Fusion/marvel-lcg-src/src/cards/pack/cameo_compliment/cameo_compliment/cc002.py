from . import *

# New Suit? — SOUTIEN d'aspect PROTECTION. Aucun cout, aucune icone de
#   ressource. Setup. Max 1 per deck.
# Setup: Search your collection for an identity-specific ARMOR upgrade from an
#   identity not in this game. Shuffle that card into your deck. Discard 2
#   cards from your hand and remove this card from the game.
#
# CARTE DE REFERENCE
#  - `58031` Cameo, comme ses deux soeurs. Montage partage dans
#    `CapaciteCameo`.
#
# TEXTE CONTRE CODE
#  ⚠ « an identity-specific ARMOR UPGRADE » -> type `Upgrade` ET trait ARMOR
#    ET `Class: "Hero"`. Sur ce trait-la, mesure faite, le filtre
#    `Class: "Hero"` n'ecarte AUCUNE carte du catalogue : les deux lectures
#    coincident, et il est garde pour que les trois cartes du set repondent a
#    la meme definition.
#  ⚠ PAS de clause « non-permanent » ici, contrairement a `cc003`. C'est
#    imprime, et ce n'est pas un oubli de l'auteur : une armure permanente
#    comme `* Iron Man's Armor` reste une cible legitime, la carte ne cherche
#    pas a garantir qu'on pourra la defausser.
#  « Setup » / « Max 1 per deck » -> bases automatiques, aucun script.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        CapaciteCameo('Upgrade', 'ARMOR'),
    ]
