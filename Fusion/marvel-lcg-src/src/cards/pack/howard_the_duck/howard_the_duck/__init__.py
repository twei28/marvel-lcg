from cards.pack import *

# ===========================================================================
# Pack HOWARD THE DUCK — contenu custom de RyCoRan (Marvel Champions Custom
# Project), reproduit a l'identique. Set 128, prefixe `hd`.
#
# Mecanique centrale : Howard joue LUI-MEME ses trois manigances annexes
# (hd010 Trapped, hd011 In a World, hd012 He Never Made — `PlayerSideScheme`,
# `Victory: "0"`), les vainc, et une fois dans la ZONE DE VICTOIRE elles lui
# donnent un bonus permanent (+1 ATK / +1 DEF / +1 THW). Plusieurs cartes
# comptent ensuite ce que contient cette zone.
#
# DEUX PORTEES DIFFERENTES, a ne jamais confondre (piege `each` du tableau de
# PROCESSUS-CARTE) :
#   - « for each SIDE SCHEME in the victory display » (hd005/hd006 Quack
#     Attack, hd007/hd008 Fowl Play) : TOUTES les manigances annexes, y
#     compris celles du vilain -> `NombreDeManigancesEnVictoire`.
#   - « for each HOWARD THE DUCK side scheme in the victory display » (hd002
#     Man-Thing) : seulement les siennes -> `NombreDeManigancesHowardEnVictoire`.
#     Le set_name « Howard the Duck » exclut « Howard the Duck Nemesis », qui
#     est un set_name DIFFERENT. Lecture confirmee par hd021 (Waddle it Be?),
#     qui remelange « all Howard the Duck side schemes » de la zone de
#     victoire DANS VOTRE DECK : seules des cartes joueur peuvent y aller.
#
# Modele officiel de tout ce bloc : le pack Cable (`next_evol/cable`), meme
# archetype « manigances annexes joueur en zone de victoire » —
# 40003/40004/40005/40011 pour le decompte
# (`Worlds.VictoryDisplay(effect).FindCardSize(CardFinder(card_type=
# SchemeSide2))`) et 40006 Technovirus Purge pour le bonus permanent accorde
# depuis la zone de victoire (`works_in_the_victory_display=True`).
#
# Traits DUCK / ELDER / VAMPIRE : ajoutes a TRAITS dans
# `game/card/face/card_face.py` (correctif de ce pack).
# ===========================================================================

# PIEGE : le « * » imprime devant un nom UNIQUE n'appartient PAS au nom.
# `cards/paper.py:45-46` le retire (`is_unique = name.startswith("* ")` puis
# `name = name.lstrip("* ")`) : un `CardFinder(name="* Howard the Duck")` ne
# trouverait JAMAIS rien, en silence. Les trois noms ci-dessous sont uniques
# dans les 5168 cartes du depot (verifie), contrairement a « Collector »
# (hd023) qui collisionne avec le vilain officiel gmw 16070-16081 — raison
# d'etre de hd024 Hellcow, et raison pour laquelle AUCUN script de ce pack ne
# cherche « Collector » par son nom.
NOM_HOWARD_HEROS = "Howard the Duck"
NOM_HOWARD_ALTER_EGO = "Howard Duckson"
NOM_MAN_THING = "Man-Thing"

SET_HOWARD = "Howard the Duck"


def NombreDeManigancesEnVictoire(effect: 'Effect') -> int:
    """« for each side scheme in the victory display » — TOUTES les manigances
    annexes, joueur comme rencontre.

    Modele exact : next_evol/cable/40003.py (Mind Scan) et 40005/40011.
    """
    return Worlds.VictoryDisplay(effect).FindCardSize(CardFinder(card_type=SchemeSide2))


def NombreDeManigancesHowardEnVictoire(effect: 'Effect') -> int:
    """« for each Howard the Duck side scheme in the victory display » — les
    SIENNES seulement (hd010/hd011/hd012), pas celles de son set nemesis
    (set_name « Howard the Duck Nemesis », distinct).
    """
    return Worlds.VictoryDisplay(effect).FindCardSize(
        CardFinder(card_type=SchemeSide2, set_name=SET_HOWARD)
    )


def ManigancesHowardEnVictoire(effect: 'Effect') -> List['CardFace']:
    """Les cartes elles-memes, pour hd021 qui doit les remelanger."""
    return list(Worlds.VictoryDisplay(effect).FindCards(
        CardFinder(card_type=SchemeSide2, set_name=SET_HOWARD)
    ))


def BonusDepuisLaZoneDeVictoire(**kwargs: Any) -> Sequence['Ability']:
    """« While <cette manigance> is in the victory display, Howard the Duck
    gets +1 <stat>. »

    Modele exact : next_evol/cable/40006.py (Technovirus Purge), meme couple
    `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...),
    works_in_the_victory_display=True, ...)`. Le garde-fou est dans
    `environment_helper.py:85` : la capacite ne s'applique QUE si la carte
    porteuse est dans la zone de victoire.
    """
    return AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
        CardFinder(name=NOM_HOWARD_HEROS),
        works_in_the_victory_display=True,
        **kwargs,
    )
