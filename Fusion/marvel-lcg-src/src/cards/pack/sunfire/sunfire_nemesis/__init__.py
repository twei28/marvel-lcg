from cards.pack import *

# ===========================================================================
# Set nemesis « Sunfire Nemesis » (Silver Samurai et la Main).
#
# ⚠ L'OBLIGATION `sf010` Shame N'EST PAS ICI : son bandeau imprime dit
# « SUNFIRE », pas « ... NEMESIS ». Son `set_name` est celui du set HEROS, son
# module vit donc dans `sunfire/sunfire/`. Piege bt019 / nt012 / yd013 /
# dr010 / bk017 / tt020 / br012 / tg011 / sn011 / bc012 — onzieme fois.
#
# ⚠ LES TRAITS `HAND` ET `NINJA` SONT NEUFS AU DEPOT. Un trait ne se declare
# nulle part, mais `sf011` Hand Ambush lit `HAND` sur les sbires vaincus : si
# un futur pack ecrivait `Hand` ou `THE HAND`, la carte ne verrait rien. Le
# trait est ecrit en MAJUSCULES, comme tous les autres.
# ===========================================================================

TRAIT_MAIN: 'CardFace.TRAITS' = "HAND"

# ⚠⚠ LES NOMS S'ECRIVENT SANS L'ETOILE D'UNICITE. Le moteur la retire du nom
# effectif (`name = name.lstrip("* ")`) : un `CardFinder(name="* Silver
# Samurai")` ne trouve JAMAIS RIEN, ET EN SILENCE. Les deux cartes de ce set se
# cherchent l'une l'autre — `sf012` convoque sa katana, `sf014` convoque son
# porteur — donc avec l'etoile les DEUX etaient mortes. Trouve par les cas le
# 06/09/2026 ; le piege etait deja consigne dans `howard_the_duck`,
# `ms_america` et `patriot`, et paye une quatrieme fois ici.
NOM_SAMOURAI = "Silver Samurai"
NOM_KATANA = "Silver Samurai's Katana"


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError.

    ⚠ `Player.IsType(x)` fait `x.IsPlayer()` (player.py:303) : sur autre chose
    qu'un joueur — une FACE de carte, ou une zone — il leve un AttributeError
    que le moteur AVALE, et la carte devient inerte en silence. Deja paye sur
    `sf002` Atomic Fire avec `SetTarget("Players")`, repaye ici avec
    `GetOwnerPlayer()`. Un seul point d'entree pour tout le set nemesis.
    """
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur vise par une carte de RENCONTRE.

    ⚠ Ces cartes n'appartiennent a personne : `GetControlByOrOwner` ne rend
    pas de joueur. On passe donc par l'engagement (pour un sbire) puis par le
    joueur courant. Lecon yd013 / dr010 / tt020 / br012 / tg011 / sn011.
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        # ⚠⚠ LA PROPRIETE `engaged_player`, JAMAIS `GetEngagedPlayer()`.
        # L'accesseur leve `AssertionError` des que le sbire n'est pas engage
        # ET que sa zone n'a pas de joueur proprietaire (minion.py:145-149) —
        # ce qui est exactement le cas d'un sbire encore CARTE DE BONUS, donc
        # au moment ou `sf013` Hand Ninja se met en jeu par son etoile Boost.
        # Le moteur AVALE l'exception : la carte ne fait rien, et seul le
        # journal d'autoplay le dit. La propriete, elle, rend `None`
        # proprement (minion.py:152-156).
        # Trouve par l'autoplay du 06/09/2026, 3 tracebacks sur 8 parties —
        # aucun cas de test ne l'avait vu, parce qu'aucun ne mettait le ninja
        # en jeu depuis la zone de bonus. Meme famille que la lecon
        # `Player.GetHero()` du pack lady_sif.
        # On refait donc a la main ce que `GetEngagedPlayer` fait AVANT son
        # assert : le joueur engage, sinon le proprietaire de la zone.
        joueur = getattr(porteur, "engaged_player", None)
        if joueur is None:
            zone = getattr(porteur.card, "area", None)
            # ⚠ `GetOwner()` ET NON `GetOwnerPlayer()` : ce dernier porte lui
            # AUSSI un assert (`assert isinstance(owner, Player)`,
            # deck/deck.py:73), qui saute des que la zone n'appartient pas a un
            # joueur — la zone de bonus du VILAIN, precisement. Deuxieme assert
            # du meme trajet, trouve par le second autoplay du 06/09/2026 apres
            # que le premier eut supprime celui de `GetEngagedPlayer`.
            proprietaire = getattr(zone, "GetOwner", None)
            joueur = proprietaire() if proprietaire is not None else None
        if EstJoueur(joueur):
            return joueur
        if EstJoueur(porteur.GetControlByOrOwner()):
            return porteur.GetControlByOrOwner()
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return Worlds.GetCurrentPlayer(effect)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    Accesseur SUR, a employer partout a la place de `GetBindFace()`. Duplique
    ici depuis le `__init__.py` du set HEROS : les deux sets sont des modules
    distincts, `sunfire_nemesis` n'importe pas `sunfire`.
    """
    return getattr(face, "bind_face", None) if face is not None else None


def TrouverCarteDuSet(effect: 'Effect', joueur: 'Player|None',
                      nom: str, card_type: Any) -> 'CardFace|None':
    """Retrouver une carte du set nemesis, OU QU'ELLE SOIT.

    ⚠⚠ `Find.Find` NE VOIT PAS LE SET NEMESIS MIS DE COTE. Sa liste de zones
    (find.py:118-133) couvre le deck de rencontre, sa defausse, le terrain, le
    deck du joueur, sa main, sa defausse et `set_aside` — mais PAS
    `player.set_aside_nemesis_sets`, la pile ou le moteur range les cinq cartes
    nemesis a la mise en place (`player_setup.py`, et c'est la que `01190`
    Shadow of the Past va les chercher).

    Constate le 06/09/2026 : `sf012` Silver Samurai ne trouvait jamais sa
    katana, et `sf014` ne trouvait jamais son porteur. Les deux cartes se
    cherchent l'une l'autre, donc les deux etaient mortes — et aucune gate
    statique ne le voyait, seul le cas de test.

    On essaie donc le chemin normal, puis la pile nemesis a la main.
    """
    if joueur is None:
        return None
    face = Find.Find(effect, who_perform=joueur, name=nom, card_type=card_type)
    if face is not None:
        return face
    pile = getattr(joueur, "set_aside_nemesis_sets", None)
    if pile is None:
        return None
    for f in list(pile.GetAll()):
        if f is not None and f.IsName(nom):
            return f
    return None

