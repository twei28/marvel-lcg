from core import *
from game.card.face import *
from game.ability import *
from game.ability.factory import *
from game.message import *

# ⚠ Import EXPLICITE, et non via `from game.card.face import *` : `Minion` vit
# dans `card_type/`, que `face/__init__.py` n'exporte pas. C'est la difference
# avec `scheme_player.py`, dont la base `SchemeSide2` vit dans `face/base/` et
# arrive donc par l'etoile. Sans cette ligne : `NameError: name 'Minion' is not
# defined`, au chargement du moteur, avant toute partie.
from game.card.face.card_type.minion import Minion

# EXTENSION (01/09/2026, pack custom alligator_loki) : LE SBIRE DE JOUEUR.
#
# Type de carte defini par l'auteur du pack (Ripper3) sur l'encart « PLAYER
# MINIONS » livre avec Alligator Loki :
#
#   « Player minions are played in the same manner as player side schemes. To
#     play a player minion, pay the printed cost. When a player minion is
#     played or revealed, it always engages its owner. When a player minion
#     would be discarded from play, place it in its owner's discard pile,
#     unless denoted otherwise with Victory X. »
#
# Une seule carte l'utilise pour l'instant : al002 « Throg », un sbire a 4 PV
# que le joueur pose devant lui pour que son propre heros le morde (al002 donne
# `overkill` a l'attaque d'Alligator Loki, et sa defaite retire 3 menaces).
#
# ⚠ POURQUOI ON HERITE DE `Minion` ET NON D'UN NOUVEAU TRONC. Le depot appelle
# `Minion.IsType(face)` a plus de deux cents endroits : engagement, attaque,
# Guard, Patrol, overkill, cartes qui cherchent « un sbire ». Un type parallele
# aurait fait de Throg un objet que rien ne reconnait. En heritant, il EST un
# sbire pour tout le moteur, et `ClassCard` lui ajoute ce qui manque a un sbire
# de rencontre : un cout, une icone de ressource, une classe d'aspect, une
# limite par deck.
#
# `PlayerCard` et `EncounterCard` sont deux marqueurs de meme forme
# (`CanSurge, CanAccelerationToken, CardFace`, tous deux `pass`), la double
# ascendance se resout donc sans conflit.
#
# ⚠ Le modele est `PlayerSideScheme` (scheme_player.py), que l'encart cite
# nommement : meme montage, une classe courte qui ajoute la capacite « je suis
# jouable depuis la main » si la carte n'en declare pas deja une.

@final
class PlayerMinion(Minion, ClassCard, FinalType):

    # ⚠ `Minion` est un type FINAL : `Minion.IsType` compare le type EXACT et
    # l'heritage seul ne suffit pas (card_face.py, `IsType`). Sans cette
    # declaration, aucun des « Minion.IsType » du moteur ne reconnaissait
    # Throg, et `HasGuard.GainGuard` assertait a son entree en jeu (constate
    # au harnais le 01/09/2026, cas « al002 Throg — overkill »).
    also_final_types = (Minion,)

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []
        if not self.ability.Find(func_name="Play"):
            abilities.append(
                AbilityFactory.CanPlayThisMinionCard()
            )
        return abilities + super().GetAbilities()
