from . import *

# * Wolverine — ALLIE (Survivor deck, carte 5/5). Cout 0. THW 1[star]. ATK 3[star]. PV 3. RES wild.
#   SURVIVOR. X-MEN.
# Texte imprime : AUCUN (`cards_custom.json`, champ `text` vide pour `hg076`) -- une alliee totalement
# vanille, exactement comme de nombreux allies officiels sans capacite (ex. `01013` Ant-Man, `03010` Peggy
# Carter...).
#
# ---------------------------------------------------------------------------
# ETAPE 2 : CARTES DE REFERENCE
#
# - Aucune capacite a scripter : il n'existe RIEN a comparer. Confirme par relecture directe de l'entree
#   `cards_custom.json` (card_id `hg076`, `"text": ""`) ET par `commun.py` (`CARD_ID_SURVIVOR_ALLY_PAR_HEROS
#   = {..., "Wolverine": "hg076"}`, qui ne documente non plus aucune capacite pour cette carte).
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - Aucun mot-cle imprime (texte vide) : rien a ouvrir, rien a creer.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5) / ETAPE 6 (nombres)
#
# - Rien a verifier mot a mot : pas de texte. Les seules valeurs imprimees sont les stats de `desc`
#   (Cost 0, THW 1[star], ATK 3[star], HP 3, RES wild) : TOUTES lues NATIVEMENT par le moteur
#   (`can_thwart.py`/`can_attack.py` pour les etoiles de degats consequents d'Allie -- voir la note generale
#   posee dans `hg072.py`, qui s'applique aussi ici -- et `has_attribute.py` pour Cost/HP/RES). Base
#   automatique au meme titre que `Toughness`/`Restricted` (PROCESSUS-CARTE.md etape 6) : AUCUNE ligne de
#   script n'est necessaire pour que la carte soit jouable, attaque ou manigance avec ses stats imprimees --
#   `Ally.GetAbilities()` ajoute lui-meme, nativement, `CanPlayThisAllyCard`/`ThisCanAttack`/`ThisCanThwart`
#   quand aucun module ne les redefinit (`card_type/ally.py:26-29`), exactement le cas ici.
#
# ⚠ PIEGE A NE PAS COMMETTRE (lecon hg017, rappelee par la consigne de cette tache) : NE PAS ecrire de
# capacite fantome la ou le texte imprime est vide. Un fichier qui existe mais ne retourne RIEN est le
# comportement CORRECT pour une carte vanille, pas une carte « non terminee ».
#
# A CONFIRMER EN PARTIE REELLE : meme reserve que les quatre autres cartes de ce lot -- aucun cas n'a ete
# EXECUTE par moi (consigne de la tache). Pour UNE carte sans texte, le seul point qu'un cas en jeu prouve
# vraiment est que `desc.ATK`/`desc.THW` donnent bien 3/1 ET que l'etoile de degat consequent (1 dans les
# deux cas) s'applique a l'usage -- comportement du moteur, jamais specifique a ce module.


def GetAbilities() -> Sequence['Ability']:
    return []
