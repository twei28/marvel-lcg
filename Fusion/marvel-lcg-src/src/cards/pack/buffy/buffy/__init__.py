from cards.pack import *
# Helpers partages du set « Buffy ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
TRAIT_HELLMOUTH = "HELLMOUTH"
TRAIT_SLAYER = "SLAYER"
NOM_MR_POINTY = "Mr. Pointy"
NOM_WATCHERS_GUIDANCE = "Watcher's Guidance"
# « the Harvest » : le scan ecrit l'article en minuscule, « The Master » en majuscule. Le premier nom est cherche sous les
# deux graphies ; on filtre sur Minion parce que « Harvest » nu est deja une traitrise officielle (05029, Ms. Marvel Nemesis).
NOMS_HARVEST = ("The Harvest", "Harvest")
NOM_THE_MASTER = "The Master"


def ManigancesHellmouth() -> 'CardFinder':
    """« a HELLMOUTH side scheme » : toute manigance annexe portant le trait, joueur comme rencontre."""
    return CardFinder2(TRAIT_HELLMOUTH, SchemeSide2)


def ManigancesHellmouthEnVictoire(effect: 'Effect') -> List['CardFace']:
    """« each HELLMOUTH side scheme in the victory display » : les cartes elles-memes (le decompte est leur longueur)."""
    return list(Worlds.VictoryDisplay(effect).FindCards(ManigancesHellmouth()))


def NombreDeHellmouthEnVictoire(effect: 'Effect') -> int:
    return len(ManigancesHellmouthEnVictoire(effect))

NOM_BUFFY = "Buffy"
NOM_BUFFY_AE = "Buffy Summers"
NOM_SLAYER_SCYTHE = "Slayer Scythe"
NOM_KENDRA = "Kendra"
NOM_MODELE_REDEEMED = "buffy_redeemed_ally"  # fiche modele (cards.json) : allie SLAYER vide, ATQ/CTR 0*


def ChoisirUne(joueur: 'Player', candidats: Sequence['CardFace'], effect: 'Effect', prompt: str) -> 'CardFace|None':
    """Une seule candidate : elle part d'office ; sinon le joueur choisit (obligatoire)."""
    if not candidats:
        return None
    if len(candidats) == 1:
        return candidats[0]
    return joueur.AskChooseFace(list(candidats), effect, prompt=prompt, forced=True)

NOM_GENTLEMEN = "The Gentlemen"
# Les six cartes du deck HELLMOUTH, creees MISES DE COTE au demarrage par l'alter-ego (`BeginGameWithSetAside`). Leurs cartes liees (Prophecy
# Girl, Chosen One, Slayer Scythe, Faith allie, Angel) sont creees par leur carte hote (`desc.Linked`).
CARTES_HELLMOUTH = ["bf027", "bf028", "bf029", "bf030", "bf031", "bf032"]
NOM_HARVEST_COMPLOT = "Harvest"
