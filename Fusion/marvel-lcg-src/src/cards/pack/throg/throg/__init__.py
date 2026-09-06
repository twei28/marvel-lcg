from cards.pack import *

# ===========================================================================
# Helpers partages du set « Throg » (Rainy, set 159, prefixe `tg`).
#
# ⚠ TOUT LE PACK TOURNE AUTOUR D'UNE SEULE AMELIORATION : tg009 Frogjolnir.
# Elle est UNIQUE, Restreinte, coute 1, et CINQ des onze cartes du set heros
# la citent nommement :
#   - tg001a « Froglike Stamina » la RENVOIE EN MAIN pour redresser Throg ;
#   - tg002 Airborne Amphibian la REDRESSE avec le heros ;
#   - tg004 Hammer Throw l'INCLINE et la renvoie en main pour frapper a 6 ;
#   - tg009 elle-meme s'INCLINE pour donner +1 a un pouvoir de base ;
#   - tg001b « Worthy » va la CHERCHER, ou qu'elle soit.
# Le marteau fait donc l'aller-retour main <-> jeu en permanence, comme le
# Stormbreaker de beta_ray_bill (meme auteur, meme moteur economique).
#
# ⚠ LES DEUX FACES N'ONT PAS LE MEME NOM, contrairement a beta_ray_bill :
# « Throg » en heros, « Puddlegulp » en alter-ego. Les cartes qui nomment
# « Throg » ne visent donc QUE la forme heros (tg009 « THROG gains the AERIAL
# trait », tg010 « give THROG a tough status card »), et tg007 Foreverglade,
# qui nomme « Puddlegulp », ne vise QUE la forme civile. C'est exactement le
# piege `an002` Sera / `06007` Asgard de RECETTES-MOTEUR §3 : un NOM PROPRE
# ne designe qu'UNE face, « you » designe les deux.
#
# ⚠ HOMONYMES. Trois, tous verifies :
#   - tg004 « Hammer Throw » est le TROISIEME du depot, apres `06005` (Thor,
#     8 degats) et `br003` (Beta Ray Bill, 6 degats). Celui-ci fait 6 aussi,
#     mais RENVOIE le marteau en main au lieu d'aller le chercher.
#   - tg013 « * Alligator Loki » est un SBIRE nemesis, sans aucun rapport
#     avec `al001a`, le HEROS du pack `alligator_loki` (set 140).
#   - tg016 « Chomped » n'a rien a voir avec `al0xx` : c'est un attachement
#     de condition, pose sur l'identite.
# ===========================================================================

NOM_HEROS = "Throg"
NOM_ALTER_EGO = "Puddlegulp"
NOM_MARTEAU = "Frogjolnir"
NOM_MORSURE = "Chomped"
SET_HEROS: 'CardFace.SETNAMES' = "Throg"
COMPTEUR_ENNEMI: 'CardFace.COUNTER' = 'foe'

# Les trois pouvoirs de base d'un heros. `AfterUnitUseBasicPower` accepte
# aussi le litteral "Hero", qui vaut exactement cette liste (friend.py:385) ;
# on l'ecrit en clair pour que le texte imprime se relise sans detour.
POUVOIRS_DE_BASE: List["CardFace.BASIC_POWER"] = ["ATK", "THW", "DEF"]


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit.

    ⚠ NE PAS se rabattre sur `effect.GetInitiator()` en premier : il leve un
    assert quand l'initiateur n'est pas un joueur, et le moteur AVALE
    l'exception — la carte ne fait alors rien, et aucun outil ne le voit
    (leçon `Player.GetHero()`, pack lady_sif).

    ⚠ Passer le joueur EXPLICITEMENT quand la carte qui agit ne lui appartient
    pas : c'est le cas de l'obligation tg011 et de tout le set nemesis, cartes
    de RENCONTRE, pour lesquelles ce helper ne rend rien (leçon yd013 / dr010 /
    tt020 / br012).
    """
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def HerosDuJoueur(effect: 'Effect') -> 'CardFace|None':
    """La face HEROS (« Throg »), ou None si le joueur est en civil.

    Le filtre est le TYPE et non le nom : c'est plus sur, et ca reste juste le
    jour ou une identite alternative changerait le nom imprime.
    """
    joueur = JoueurDeCetteCarte(effect)
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None or not Hero.IsType(identite):
        return None
    return identite


def MarteauEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Frogjolnir sur le terrain, ou None.

    Lu par tg001a (qui le renvoie en main), tg002 (qui le redresse) et tg004
    (qui l'incline puis le renvoie).
    """
    return Worlds.FindCardOnField(effect, name=NOM_MARTEAU, card_type=Upgrade)


def EstCarteDeThrog(face: 'CardFace|None') -> bool:
    """« a Throg card » (tg008 Frog of Thunder).

    Le moteur a la primitive : `IsDeckBuildingClass` (card_player.py:169)
    verifie D'ABORD la classe `IdentitySpecific`, PUIS l'egalite litterale du
    `set_name`. Ne PAS comparer les noms a la main — et surtout pas se fier au
    nom « Throg », qui est aussi celui de la face heros.
    """
    if face is None or not ClassCard.IsType(face):
        return False
    return face.IsDeckBuildingClass(SET_HEROS)


def ResoudreWorthy(effect: 'Effect', joueur: 'Player|None') -> None:
    """Le corps de la capacite « Worthy » de tg001b.

    « FIND Frogjolnir and add it to your hand. » — « find » n'est pas
    « search your deck » : le mot couvre le deck, la defausse ET LE TERRAIN.
    Le marteau pose sur l'identite revient donc en main, ce qui est le cas
    utile en civil : on remonte le marteau pour le rejouer.

    ⚠ Contrairement au `Worthy` de `br001a`, AUCUN effet secondaire : Throg ne
    frappe personne en rappelant son marteau. Verifie sur le scan.
    """
    if joueur is None:
        return
    marteau = MarteauEnJeu(effect)
    if marteau is not None:
        Faces.ReturnToHand([marteau], "Owner", effect)
        return
    face = Search.PlayerCard(
        effect, joueur,
        include_player_deck=True,
        include_discard_pile=True,
        name=NOM_MARTEAU,
        card_type=Upgrade,
    )
    if face is not None:
        joueur.GainCard(face, effect)
