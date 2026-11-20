from ..commun import *

# Set Punisher's Hit List (pack MC×DC 2026) : Punisher y est un sbire ELITE (pu107) dont l'aptitude « Punishment »
# est appelee par presque toutes les cartes du set.
#
# « Punishment — Special : Punisher attacks the minion with the fewest remaining hit points with +2 ATK. Ignore "Boost"
#   abilities for this attack. If the attack defeats that minion, repeat this ability. »
#
# Cartes de reference : `Enemy.AttackCharacter` (brique commune du 20/10/2026, `additional_attack`, `if_this_defeat_unit`) ;
# `ignore_boost_abilities` ajoute le 21/10/2026 (AttackProperty + AttackCharacter, via `WouldAttack.IgnoreBoost`).
#
# ⚠ « the minion with the FEWEST remaining HP » : un sbire (jamais Punisher lui-meme, jamais le vilain) ; a egalite le
# PREMIER JOUEUR choisit (la RR ne tranche pas autrement) ; « Punisher cannot attack this minion » (Rachel Cole-Alves,
# pu108) retire le sbire de la liste ; « ignore Boost abilities » : les icones de boost comptent, pas le texte ; « if the
# attack defeats that minion, REPEAT » : tant qu'un sbire tombe et qu'il reste une cible ; aucune cible = pas « able ».

CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER = ("pu108",)


def TrouverPunisher(effect: 'Effect') -> 'Enemy|None':
    """Punisher EN JEU (sbire elite pu107, ou le vilain du scenario 3)."""
    return Worlds.FindCardOnField(effect, name="Punisher", card_type=Enemy)


def Punishment(effect: 'Effect', punisher: 'Enemy|None'=None) -> bool:
    """Resout « Punishment ». Rend True si Punisher a pu attaquer au moins une fois."""
    punisher = punisher or TrouverPunisher(effect)
    if punisher is None or not punisher.IsInPlay():
        return False
    attaque = False
    premier = Worlds.GetFirstPlayer(effect)
    while punisher.IsInPlay() and not effect.world.is_game_over:
        cibles = [m for m in Worlds.GetOnFieldMinions(effect)
                  if m is not punisher and m.paper.card_id not in CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER]
        if not cibles:
            break
        mini = min(m.health for m in cibles)
        ex_aequo = [m for m in cibles if m.health == mini]
        cible = ex_aequo[0] if len(ex_aequo) == 1 else premier.AskChooseFace(ex_aequo, effect)
        if cible is None:
            break
        vaincu = []
        punisher.CastTo(Enemy).AttackCharacter(
            cible, effect,
            additional_attack=2,
            ignore_boost_abilities=True,
            if_this_defeat_unit=lambda u: vaincu.append(u),
        )
        attaque = True
        if not vaincu:
            break
    return attaque


def AjouterUnCompteurALaListe(effect: 'Effect') -> None:
    liste = Worlds.FindCardOnField(effect, name="Punisher's Hit List")
    if liste is not None:
        Faces.PlaceCountersOn([liste], 1, 'counter', effect)
