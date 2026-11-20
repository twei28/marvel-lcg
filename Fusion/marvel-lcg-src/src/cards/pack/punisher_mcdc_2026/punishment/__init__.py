from ..commun import *
from cards.pack.fne import RetournerLAttachement
from ..punishers_hit_list import CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER, TrouverPunisher as _TrouverPunisherHL

# Set Punishment (pack MC×DC 2026) : le Punisher, vilain final du scenario 3 « One Last Kill ».
#
# Vocabulaire du set :
#  - « Punisher » : le vilain `Punisher` (pu086a..pu087b), le « vilain actif ».
#  - « the TARGETED villain » : le vilain SOUS-FIFRE (Jigsaw ou Hobgoblin) qui porte In the Crosshairs (pu092 : +5 PV par
#    joueur, trait TARGETED, insensible aux cartes joueur, sa defaite = defaite des joueurs).
#  - Target Lock (pu091a FOCUSED / pu091b DISTRACTED) : attachement recto-verso pose sur Punisher.
#
# Briques moteur utilisees (docs/reference/RECETTES-MOTEUR.md §15-16) : `Enemy.AttackCharacter` (un ennemi attaque un
# ennemi ou un allie ; `players_may_defend`, `overkill_to`, `give_boost`), `Villains` (plusieurs vilains en jeu, un seul
# « le vilain »), `AbilityFactory.CannotBeAffectedByPlayerCards`.

NOM_CIBLE_ATTACHEMENT = "Target Lock"
FOCUSED = "pu091a"
DISTRACTED = "pu091b"
# « Punisher cannot attack this minion » : Rachel (pu098 et pu108 de Hit List), Microchip (pu097).
CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER_PU = tuple(CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER) + ("pu097", "pu098")


def Punisher(effect: 'Effect') -> 'Villain|None':
    for v in Worlds.GetVillains(effect):
        if v.paper.name.strip("* ") == "Punisher":
            return v
    return None


def VilainCible(effect: 'Effect') -> 'Villain|None':
    """« the TARGETED villain » : le vilain qui porte le trait TARGETED (In the Crosshairs)."""
    for v in Worlds.GetVillains(effect):
        if v.HasTrait("TARGETED"):
            return v
    return None


def TargetLockEnJeu(effect: 'Effect') -> 'Attachment|None':
    return Worlds.FindCardOnField(effect, name=NOM_CIBLE_ATTACHEMENT, card_type=Attachment)


def RetournerTargetLockVersDistracted(effect: 'Effect') -> None:
    """« Flip Target Lock to its DISTRACTED side » : sans effet s'il l'est deja ou n'est pas en jeu."""
    lock = TargetLockEnJeu(effect)
    if lock is not None and lock.paper.card_id == FOCUSED:
        RetournerLAttachement(lock, effect, call_reveal=False)


def RetournerTargetLockVersFocused(effect: 'Effect') -> None:
    lock = TargetLockEnJeu(effect)
    if lock is not None and lock.paper.card_id == DISTRACTED:
        RetournerLAttachement(lock, effect, call_reveal=False)


def CiblesDePunisher(effect: 'Effect', punisher: 'Enemy') -> List['Enemy']:
    """Les ennemis que Punisher peut attaquer : sbires (sauf ceux qu'il ne peut pas attaquer) et le vilain cible ; jamais
    lui-meme."""
    return [e for e in Worlds.GetOnFieldEnemies(effect)
            if e is not punisher and e.paper.card_id not in CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER_PU]


def LePlusFaible(effect: 'Effect', cibles: Sequence['Enemy']) -> 'Enemy|None':
    """L'ennemi aux PV restants les plus bas ; a egalite le premier joueur choisit."""
    if not cibles:
        return None
    mini = min(e.health for e in cibles)
    ex_aequo = [e for e in cibles if e.health == mini]
    if len(ex_aequo) == 1:
        return ex_aequo[0]
    return Worlds.GetFirstPlayer(effect).AskChooseFace(ex_aequo, effect)


def PunisherAttaque(effect: 'Effect', punisher: 'Enemy', cible: 'CardFace', **options: Any):
    """Une attaque de Punisher contre un ENNEMI ou un allie : les joueurs peuvent defendre n'importe quelle attaque
    (pu090b « Players may defend any attack, even ones targeting enemies »), et l'exces d'un coup `overkill` sur un sbire va
    au vilain cible (pu093)."""
    cible_exces = VilainCible(effect)
    options.setdefault('players_may_defend', True)
    if cible_exces is not None:
        options.setdefault('overkill_to', cible_exces)
    return punisher.CastTo(Enemy).AttackCharacter(cible, effect, **options)


def DonnerUneCarteBoostFaceCachee(effect: 'Effect', cible: 'CardFace|None', n: int=1) -> None:
    if cible is not None:
        Faces.GiveFacedownBoostCards([cible], n, effect)
