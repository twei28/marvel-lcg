from . import *

# Ye Be Worthy — SOUTIEN d'aspect AGRESSIVITE. Aucun cout, aucune icone de
#   ressource. Setup. Max 1 per deck.
# Setup: Search your collection for an identity-specific non-permanent WEAPON
#   upgrade from an identity not in this game. Shuffle that card into your
#   deck. Discard 2 cards from your hand and remove this card from the game.
#
# CARTE DE REFERENCE
#  - `58031` Cameo, comme ses deux soeurs. Montage partage dans
#    `CapaciteCameo`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « NON-PERMANENT » EST LA SEULE CLAUSE QUI DISTINGUE CETTE CARTE DE SES
#    DEUX SOEURS, et elle est imprimee. `desc.Permanent` est une base
#    automatique du moteur : on la LIT sur le `Paper`, on ne la calcule pas.
#    Mesure sur le catalogue du 05/09/2026 : elle ecarte SIX ameliorations
#    WEAPON — `35002` et `wx002` * Wolverine's Claws, `41002a` Psi-Knife,
#    `41002b` Psi-Katana, `43002` * X-23's Claws, `nt003b` * Battle Board.
#    Toutes sont des armes de signature qui ne peuvent PAS quitter le jeu, et
#    qui rendraient donc la carte piegeuse : c'est exactement ce que la clause
#    evite.
#  ⚠ « an identity-specific ... WEAPON UPGRADE » -> type `Upgrade` ET trait
#    WEAPON ET `Class: "Hero"`. Comme pour ARMOR, le filtre `Class: "Hero"`
#    n'ecarte aucune carte sur ce trait : les deux lectures coincident.
#  « Setup » / « Max 1 per deck » -> bases automatiques, aucun script.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        CapaciteCameo('Upgrade', 'WEAPON', non_permanent=True),
    ]
