from cards.pack import *

# ===========================================================================
# Pack PATRIOT — helpers partages du set `Patriot`.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : TOUT PARLE D'ALLIES
#
# 12 des 17 cartes joueur dependent d'un allie en jeu. Will to Protect
# (pt001a) encaisse a leur place, Hawkingbird (pt002) leur donne +1 PV,
# Aided Defense (pt003/pt004) et Covered Fire (pt005/pt006) les epuisent ou
# les designent, Commander's Orders (pt009) et Follow My Lead (pt010) les
# servent, On Your Feet (pt011) les redresse ou les soigne, The Chosen Leader
# (pt014) les remplace, et Revenge (pt013) / Throwing Stars (pt015) /
# Working Together (pt016) s'attachent a eux. Sans allie en jeu, la moitie du
# pack est injouable : c'est VOULU, ce n'est pas un defaut a corriger.
#
# ---------------------------------------------------------------------------
# LA REGLE DE LA FLECHE — elle apparait sur SEPT cartes de ce pack
#
# `→` separe un COUT (a gauche) d'un EFFET (a droite), et la capacite ne se
# declenche QUE si le cout est integralement payable. Regle officielle,
# tranchee par l'utilisateur le 30/08/2026 apres une erreur sur `sd021`. Elle
# vaut AUSSI pour une capacite FORCEE (`11014` Temporal Shield, `11031`
# Chitauri Soldier, `16074` Biogram Image). Quand une carte veut deux
# CONSEQUENCES, elle les relie par « and » SANS fleche (`02021` Pumpkin
# Bombs).
#
# Concretement, dans ce pack, le cout est TOUJOURS rendu par un
# `SetCostFunc(...)` ou par un `.SetTarget(...)` obligatoire porte par la
# capacite elle-meme : le moteur ne propose alors PAS la capacite quand le
# cout n'a aucune cible legale (`CostFunc.Base.HasTargets`, cost_func.py:47).
# C'est la seule construction qui rend « cout impayable = rien ne se passe »
# sans le reecrire a la main. Les cartes concernees : pt001b, pt003/pt004,
# pt005/pt006, pt007, pt008, pt009, pt010, pt011, pt013, pt015, pt016, pt017,
# pt020.
#
# ---------------------------------------------------------------------------
# PIEGE DE NOMMAGE — le `*` d'unicite
#
# `cards/paper.py:45-46` retire le prefixe « * » d'un nom unique. Un
# `CardFinder(name="* Patriot's Shield")` ne trouverait JAMAIS rien, EN
# SILENCE. Les constantes ci-dessous sont donc ecrites SANS l'etoile.
#
# PIEGE DE NOMMAGE — la collision « Patriot »
#
# Le catalogue contient DEJA deux allies officiels nommes « Patriot » :
# `29016` (Rayshaun Lucas, Leadership, pack ironheart) et `56041` (Elijah
# Bradley lui-meme, Protection, pack cw). AUCUNE carte de ce pack ne fait de
# recherche par nom sur « Patriot » : les capacites visent `"This"`,
# `"YourHero"` ou `"YourIdentity"`, jamais un `CardFinder(name="Patriot")`.
# Le deck de depart exclut par ailleurs `29016` (voir `collision_note` dans
# deck/starter/patriot.json).
#
# PIEGE DE NOMMAGE — « Mr. Hyde » vs « Mister Hyde »
#
# `pt019` s'appelle « Mr. Hyde ». Le jeu contient DEJA `24035` « Mister
# Hyde » (set `Mister Hyde`, pack `hood`). Les deux CHAINES sont
# differentes : aucune collision moteur. On ne corrige rien cote `hood`.
#
# ---------------------------------------------------------------------------
# LA REGLE DE DECK-BUILDING « Leader » (pt001b)
#
# « During deck building you may include YOUNG AVENGER allies from any
# aspect. » Ce n'est PAS une capacite de jeu : le moteur ne valide jamais un
# deck au chargement (GUIDE §5.2). La regle vit dans le DECK-BUILDER,
# `public/js/deckbuilder/app.js`, fonction `exemptDeLaLimiteAspect(hero,
# carte)` (GUIDE §14.1) — exactement la ou vit deja *Arachnophilia* de
# Cassandra Webb. Elle est implementee la-bas et documentee ici ; il n'y a
# rien a coder dans pt001b.py pour elle.
#
# ⚠ Elle n'a AUJOURD'HUI aucune cible legale : les deux seuls allies YOUNG
# AVENGER du catalogue sont `il002` Stature et `wc002` Hulkling, tous deux de
# classe `Hero`, donc cartes signature d'autres heros, interdites de deck par
# PROCESSUS-HEROS §10. La regle ne mordra qu'a l'arrivee d'un allie YOUNG
# AVENGER d'aspect.
# ===========================================================================

# Noms ecrits SANS l'etoile d'unicite (voir le piege ci-dessus).
NOM_PATRIOT = "Patriot"
NOM_ELIJAH = "Elijah Bradley"
NOM_PATRIOTS_SHIELD = "Patriot's Shield"
NOM_ISAIAH = "Isaiah Bradley"
NOM_MR_HYDE = "Mr. Hyde"
NOM_MGH_DRUG = "MGH Drug"

# « When Patriot's Shield reaches 3 damage, discard it. » (pt012)
DEGATS_MAX_SUR_LE_BOUCLIER = 3


################################################################################
# « an upgrade that can be attached to an ally »
#
# Employe par pt002 (Response de Hawkingbird) et par pt010 (Follow My Lead).
# Le filtre n'est PAS « une amelioration » mais « une amelioration ATTACHABLE
# A UN ALLIE » : `CardFinder(canbe_attach_to=<un allie>)` appelle
# `Upgrade.CanAttachTo(face)` (card_type/upgrade.py:83), qui relit le
# selecteur de la capacite « Play » de l'amelioration. Une amelioration qui
# se pose sur l'identite est donc bien ecartee.
#
# Cartes qui passent le filtre dans le deck de depart Leadership : pt013
# Revenge, pt015 Throwing Stars, pt016 Working Together et `01074` Inspired.

def AmeliorationAttachableA(allie: 'CardFace') -> 'CardFinder':
    """`CardFinder` des ameliorations attachables a CET allie."""
    return CardFinder(card_type=Upgrade, canbe_attach_to=allie)


def UnAllieDeReference(player: 'Player|None', effect: 'Effect',
                       defaut: 'CardFace|None'=None) -> 'CardFace|None':
    """Un allie du joueur, pour servir de temoin au filtre ci-dessus.

    `canbe_attach_to` exige une FACE concrete, pas un type : on lui donne un
    allie reellement en jeu. `defaut` permet a l'appelant d'imposer le sien
    (pt002 se donne elle-meme, ce qui garantit une reponse meme si elle est
    le seul allie du joueur).
    """
    if defaut is not None:
        return defaut
    if player is None:
        return None
    allies = list(player.allies.Get())
    return allies[0] if allies else None
