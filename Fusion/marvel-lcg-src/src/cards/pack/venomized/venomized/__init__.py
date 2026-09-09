from cards.pack import *

# ===========================================================================
# Helpers partages de l'aspect VENOMIZED (ekAugust, set 168, prefixe `vz`).
#
# ⚠ CE N'EST PAS UN PACK DE HEROS : c'est un SIXIEME ASPECT de deckbuilding
# (noir), 35 cartes d'aspect plus le set « Venomized Weakness » (2 cartes).
# Aucune identite, aucune obligation, aucun set nemesis. `PROCESSUS-HEROS.md`
# ne s'applique donc pas : c'est `PROCESSUS-CARTE.md`, 37 fois.
# Precedent structurel : `cameo_compliment` (3 cartes d'aspect, set 162) et
# `determination` (aspect entier, set 118).
#
# ⚠ LES HUIT EVENEMENTS « SYMBIOTIC » SONT DES JUMEAUX DE CARTES OFFICIELLES.
# L'insert le dit : « versions symbiote de cartes d'aspect deja dans votre
# collection », meme texte, meme cout, meme ressource ; seuls le TITRE et le
# trait [[SYMBIOTE]] changent, ce qui les rend cumulables avec l'original.
# Chaque module cite son original et en reprend le corps SANS LE REECRIRE :
#   vz016 <- 10014 Drop Kick        vz020 <- 38016 Not Today!
#   vz017 <- 01060 For Justice!     vz021 <- 28014 One by One
#   vz018 <- 29017 Go All Out       vz022 <- 13033 Perseverance
#   vz019 <- 15013 Multitasking     vz023 <- 23017 Sneak Attack
#
# ⚠ HOMONYME A NE PAS CONFONDRE : `vz015` s'appelle « Stronger Together »
# comme l'officielle `58019` (Protection), et n'a RIEN a voir avec elle.
# L'officielle reduit des degats subis par un allie ; celle-ci redresse deux
# personnages. Meme nom, deux cartes.
# ===========================================================================

# Le nom de l'aspect tel qu'il est ecrit dans `desc.Class` et dans les deux
# `Literal` de `card_player.py`. Ecrit une fois : six cartes le relisent.
VENOMIZED = "Venomized"

# Le trait que l'aspect distribue, et que sept cartes interrogent.
SYMBIOTE = "SYMBIOTE"


def EstUneCarteVenomized(face: 'CardFace') -> bool:
    """« a Venomized (black) card ».

    L'aspect d'une carte joueur se lit dans `desc.Class`, ou les classes
    multiples sont separees par des points-virgules (voir `cameo_compliment`,
    `EstSpecifiqueAUneIdentite`). On teste donc l'appartenance a la liste, et
    non une sous-chaine : sinon « Venomized » se trouverait dans n'importe
    quelle classe future qui le contiendrait.

    Relu par vz002 Codex, vz006 Venom, vz012 Forceful Bonding, vz027 The Power
    of the Bond et vz029 Doctor Steven.
    """
    if face is None:
        return False
    classes = (face.paper.desc.get("Class") or "").split(";")
    return VENOMIZED in [c.strip() for c in classes]


def PorteLeTraitSymbiote(face: 'CardFace') -> bool:
    """« a SYMBIOTE card ».

    ⚠ On lit les traits de la FACE en jeu (`face.traits`) et non ceux imprimes
    sur le papier : une carte peut gagner un trait en cours de partie, et le
    texte dit « a SYMBIOTE card », pas « a card printed with ».
    """
    if face is None:
        return False
    return face.HasTrait(SYMBIOTE)
