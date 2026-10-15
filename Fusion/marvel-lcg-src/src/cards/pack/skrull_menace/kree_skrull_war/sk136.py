from . import *

# * Bel-Dann — SBIRE (Kree-Skrull War). ELITE. KREE. SCH 1, ATK 3, 4 PV, 2 icones Y.
# When Revealed: Search the encounter deck and discard pile for Raksor and put
#   him into play engaged with you.
#
# Cartes de reference :
#  - **`sk112`** Outnumbered (Skrull Society) / **`27141`** : `Search.EncounterCard(
#    include_discard_pile=True, name=...)` (melange natif) ; `sk083a` : `PutIntoPlay(
#    joueur)` = sbire mis en jeu ENGAGE avec ce joueur.
#  - **`04077`** Absorbing Man : meme esprit (fouille deck + defausse d'une carte
#    nommee).
#
# ⚠ Mots-pieges : « put him INTO PLAY » (pas « reveal » : les When Revealed de Raksor
# ne partent pas, sinon boucle infinie Bel-Dann <-> Raksor) ; « engaged with YOU »
# (le joueur a qui la carte est revelee) ; « encounter deck AND discard pile » ;
# Raksor deja en jeu / absent : rien. La version « alternative » (stats a droite)
# est la meme carte (decision de l'inventaire du 15/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def renfort(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        MettreEnJeuEngage(effect, message.GetToPlayer(), "Raksor")

    return [
        AbilityFactory.WhenThisRevealed(None, renfort),
    ]
