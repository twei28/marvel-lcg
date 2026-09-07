from cards.pack import *

# ===========================================================================
# Helpers partages du set « Ares » (Rainy, set 164, prefixe `ar`).
#
# ⚠ LE PACK EST LA BRIQUE 6 POUSSEE LOIN : trois ameliorations JOUEUR se posent
# sur un ENNEMI (ar006 Feint, ar008 Reeling, ar009 Sundered, « Max 1 per
# enemy » = desc MaxPerUnit), et le reste du kit les LIT : ar004 Ares' Axe
# compte les ameliorations attachees a la cible, ar007 God of War en pose une
# depuis le deck quand un sbire entre en jeu, ar005 Ares' Battle Helm et ar008
# Reeling travaillent sur les DEGATS EXCEDENTAIRES (modeles `ss012` Mark of
# Kaine et `gmw/16045` Follow Through).
#
# ⚠⚠ LES DEUX FACES DE L'IDENTITE PORTENT LE MEME NOM, « Ares », comme Beta Ray
# Bill. Et « * Ares » est DEJA `59036`, un sbire du set Hercules Nemesis, « God
# of War » DEJA `59040`. Aucune carte du pack ne cherche par le NOM : l'identite
# se retrouve par le TYPE (`Hero`), les cartes par card_id ou par trait.
#
# ⚠ MOT-CLE MAISON `seek` : fiche `docs/reference/mots-cles/seek.md`, creee pour
# ce pack. Lecture retenue depuis beta_ray_bill : chercher dans la zone nommee,
# rien de plus.
#
# ⚠ ARBITRAGES UTILISATEUR DU 07/09/2026 (PROCESSUS-CARTE etape 3) :
#  - ar007 God of War : « play it on that minion » = la carte est JOUEE, son
#    cout est PAYE (un TACTIC d'aspect emprunte coute son prix, l'obligation
#    ar010 s'applique). Feint/Reeling/Sundered coutent 0.
#  - ar013 Aegis Breastplate : les degats HORS attaque sont absorbes aussi et
#    renvoyes a l'IDENTITE du joueur a l'origine de l'effet.
#  - ar003 To Battle! : « Choose two of the following » = deux options
#    DIFFERENTES.
# ===========================================================================

SET_HEROS: 'CardFace.SETNAMES' = "Ares"
TRAIT_TACTIC: 'CardFace.TRAITS' = "TACTIC"
TRAIT_WEAPON: 'CardFace.TRAITS' = "WEAPON"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception (lecon `Player.GetHero()`, pack lady_sif). Meme helper que
    sunfire, black_cat, throg.
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


def HerosDuJoueur(effect: 'Effect', joueur: 'Player|None' = None) -> 'CardFace|None':
    """La face HEROS d'Ares, ou None si le joueur est en civil.

    ⚠ LE FILTRE EST LE TYPE, JAMAIS LE NOM : les deux faces s'appellent Ares,
    et `59036` * Ares est un SBIRE du set Hercules Nemesis.
    """
    if joueur is None:
        joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    Accesseur SUR, a employer partout a la place de `GetBindFace()`. Modele
    blink, yondu, sunfire : les trois autres packs de la brique 6.
    """
    return getattr(face, "bind_face", None) if face is not None else None


def AmeliorationsAttacheesA(face: 'CardFace|None') -> List['CardFace']:
    """Les AMELIORATIONS (type Upgrade) posees sur cette carte.

    ⚠ « upgrade » est un TYPE de carte joueur : un attachement de RENCONTRE
    (type Attachment, par exemple ar013 Aegis Breastplate) n'en est pas un et
    ne compte pas pour Ares' Axe. `GetAttachedUpgrades` ne rend que les
    ameliorations, c'est exactement le filtre voulu (modele `60008`
    Cross-Examination : `len(target.GetAttachedUpgrades())`).
    """
    if face is None:
        return []
    return [u for u in list(face.GetAttachedUpgrades()) if u is not None]


def EstUneAmeliorationTactic(face: 'CardFace|None') -> bool:
    """Une AMELIORATION portant le trait TACTIC (Feint, Reeling, Sundered, ou
    une amelioration d'aspect empruntee par Lord of War)."""
    return (face is not None and Upgrade.IsType(face)
            and face.HasTrait(TRAIT_TACTIC))


def PeutSAttacherA(effect: 'Effect', amelioration: 'CardFace', cible: 'CardFace') -> bool:
    """« a TACTIC upgrade that CAN BE ATTACHED to that minion ».

    On pose au moteur la question qu'il se pose lui-meme avant toute attache :
    `Message.CheckIfFaceCanAttachTo` (sender.py:205), le message qu'ecoute
    `ThisCannotHaveCardsAttached` et notre `ar012` Athena (« cannot have TACTIC
    upgrades attached »). Puis la regle « Max 1 per enemy » (desc MaxPerUnit),
    lue a la main : un second Feint sur le meme ennemi n'est pas legal.
    """
    if amelioration is None or cible is None:
        return False
    question = Message.CheckIfFaceCanAttachTo(amelioration, cible, effect)
    question.Send()
    if not question.can_attach_to:
        return False
    max_par_unite = getattr(amelioration, "max_per_unit", None)
    if max_par_unite:
        memes = [u for u in AmeliorationsAttacheesA(cible) if u.IsName(amelioration.name)]
        if len(memes) >= int(max_par_unite):
            return False
    return True


def EnnemisEnJeu(effect: 'Effect') -> List['CardFace']:
    return [e for e in Worlds.GetOnFieldEnemies(effect) if e is not None]
