from cards.pack import *

# ===========================================================================
# Helpers partages du set « Blade » (Rainy, set 165, prefixe `bl`).
#
# ⚠ LE PACK TOURNE AUTOUR DE DEUX CHOSES :
#  1. Les PIONS DE SANG (`blood`) sur l'IDENTITE : Eric Brooks les pose
#     (Serum Injection), Vampire Bite en pose, Blood Rush les depense pour
#     redresser Blade, l'obligation The Thirst les mange au debut du tour.
#     Compteur AJOUTE a l'enum `COUNTER` le 07/09/2026 (card_face.py).
#  2. Les ATTAQUES PERCANTES : Go for the Heart, Bandolier of Stakes,
#     Daywalker (pour Vampire Bite) en donnent ; Blade's Sword les renforce ;
#     et TOUT le set nemesis dit « Attacks with piercing deal double damage »
#     (modele exact : `39051` Vampire du set Horror de Mojo, que Rainy a
#     recopie). ARBITRAGE UTILISATEUR DU 07/09/2026 : les BONUS s'appliquent
#     AVANT le doublement (4 + 1 = 5, double = 10). C'est l'ordre naturel du
#     moteur : les bonus passent par `DealAdditionalDamage` (WhenUnitWouldAttack /
#     WhenUnitMakeKeyWordAttack), le doublement par `WhenRecalculateAttackDamage`,
#     envoye APRES (can_attack.py:374).
#
# ⚠ HOMONYMES : « Bandolier of Stakes » existe TROIS fois (39048 attachement
# Horror, bl007 amelioration, bl015 attachement nemesis), « Vampire » deux fois
# (39051, bl014), « Gear Up » (mk009, 40192a), « On the Hunt » (16184),
# « Blade » (21019, dt052 allies). Les seules recherches par NOM du pack visent
# « Vampire Bite » (bl010) et « Dracula » (bl001b), sans homonyme au depot.
#
# ⚠ BLOOD RUSH ET DAYWALKER partagent UNE limite « once per phase » : les deux
# Responses portent le meme `SetName(NOM_BLOOD_RUSH)` et la condition
# `BloodRushPasEncoreResolue` lit `world.stat.once_per_phase_effects` par ce
# nom. Daywalker est ecrit comme une SECONDE Response au meme declencheur
# (« After Blade uses a basic power »), a cout « take 2 damage » : c'est
# l'equivalent exact de « resolve that ability without paying its cost ».
# ===========================================================================

SET_HEROS: 'CardFace.SETNAMES' = "Blade"
TRAIT_WEAPON: 'CardFace.TRAITS' = "WEAPON"
TRAIT_VAMPIRE: 'CardFace.TRAITS' = "VAMPIRE"
COMPTEUR_SANG: 'CardFace.COUNTER' = 'blood'
COMPTEUR_SOIF: 'CardFace.COUNTER' = 'thirst'
COMPTEUR_PIEU: 'CardFace.COUNTER' = 'stake'
NOM_BLOOD_RUSH = "Blood Rush"
NOM_DAYWALKER = "Daywalker"
NOM_VAMPIRE_BITE = "Vampire Bite"
NOM_DRACULA = "Dracula"   # ⚠ sans l'etoile d'unicite (paper.py la retire)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception (lecon `Player.GetHero()`, pack lady_sif). Meme helper que
    ares, sunfire, black_cat, throg.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def IdentiteDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """L'identite (Blade OU Eric Brooks), quelle que soit la forme."""
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    return joueur.GetIdentity()


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS de Blade, ou None si le joueur est en civil (type, pas nom :
    « Blade » est aussi un allie officiel, 21019 et dt052)."""
    identite = IdentiteDuJoueur(effect, joueur)
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas."""
    return getattr(face, "bind_face", None) if face is not None else None


def PionsDeSang(identite: 'CardFace|None') -> int:
    if identite is None:
        return 0
    return int(identite.GetCounters(COMPTEUR_SANG) or 0)


def ControleDaywalker(effect: 'Effect', joueur: 'Player|None' = None) -> bool:
    """Daywalker est-il en jeu sous le controle du joueur ? (Vampire Bite lit
    « your Vampire Bite attacks gain piercing » ici.)"""
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return False
    return any(c is not None and Upgrade.IsType(c) and c.IsName(NOM_DAYWALKER)
               for c in joueur.GetControlCards())


def ArmesPretes(joueur: 'Player|None') -> List['CardFace']:
    """Les ameliorations WEAPON PRETES que le joueur controle : ce qu'on peut
    incliner pour Go for the Heart et Vampiric Reflexes."""
    if joueur is None:
        return []
    return [c for c in joueur.GetControlCards()
            if c is not None and Upgrade.IsType(c) and c.HasTrait(TRAIT_WEAPON)
            and not c.IsExhaust()]


def BloodRushPasEncoreResolue(effect: 'Effect', message: Any) -> bool:
    """La limite « once per phase » PARTAGEE entre Blood Rush (bl001a) et sa
    version Daywalker (bl009) : aucun effet nomme « Blood Rush » n'a encore
    ete enregistre cette phase (`RecordEffect`, world_stat.py:98)."""
    Unused(message)
    enregistres = getattr(effect.world.stat, "once_per_phase_effects", [])
    return not any(getattr(getattr(x, "ability", None), "name", "") == NOM_BLOOD_RUSH
                   for x in enregistres)
