from cards.pack import *

# ===========================================================================
# Pack WICCAN — contenu custom de CptScorp (Marvel Champions Custom Project,
# Cycle 2), meme auteur qu'`iron_lad` et `scarlet_spider`. Set 129, prefixe
# `wc`. Billy Kaplan / Wiccan, sorcier adolescent des Young Avengers.
#
# ---------------------------------------------------------------------------
# MECANIQUE CENTRALE : compter les icones BOOST de la carte du DESSUS du deck
# de rencontre.
#
# Neuf cartes du pack en dependent (wc002, wc003/wc004, wc005/wc006/wc007,
# wc008, wc009/wc010, wc011/wc012, wc014, plus wc016 qui les rejoue et wc018
# qui les eteint). Wiccan joue meme avec cette carte FACE VISIBLE
# (« Clairvoyance », wc001a/wc001b).
#
# Deux briques du moteur suffisent, toutes deux deja utilisees par des cartes
# du depot :
#   - `player.LookAtDeck("EncounterDeck", 1, effect)` (game/player/action/
#     player_action.py:945) REGARDE le dessus du deck sans y toucher ;
#   - `FacesCounter.CountTotalBoostIcons(faces)` (game/operate/
#     faces_counter.py:142) compte les icones, en passant par
#     `HasBoostIcon.CountBoostIconsInternal` (donc en respectant les cartes
#     qui modifient le decompte, ex. 08006 Black Widow).
#
# Precedents exacts du depot, tous relus avant d'ecrire une ligne :
#   - `drs/doctor_strange/09003.py` (Astral Projection) : LookAtDeck +
#     CountTotalBoostIcons, base fixe + icones ;
#   - `agent_13/agent_13/ag004.py` (Infiltrate), meme couple, avec la
#     distinction REGARDER / DEFAUSSER explicitement commentee ;
#   - `scw/scarlet_witch/15004.py` (Hex Bolt) : paliers d'icones
#     (0/1, 2 ou plus), exactement la forme de wc005 et wc009 ;
#   - `gambit/gambit/37001b.py` (Remy LeBeau) : `CostFunc.LookAtDeck(
#     "EncounterDeck", 2, discard=1)`, la variante « regarder 2, defausser 1 »
#     de wc001b (ici la defausse est OPTIONNELLE, donc ecrite a la main).
#
# ---------------------------------------------------------------------------
# L'INTERRUPTEUR DE L'OBLIGATION (wc018)
#
# wc018 Avoiding the Demiurge propose « Boost icons cannot be counted for any
# Wiccan card effects until the end of the next player phase ». C'est un
# interrupteur GLOBAL : il doit eteindre le comptage de TOUTES les cartes du
# pack, pas d'une seule. Il vit donc ici, a cote du helper, et non dans
# wc018.py.
#
# Rendu : un attribut clairement nomme sur `effect.world`, comme le guide le
# recommande (§3.1 « Etat persistant maison ») et comme le fait deja
# `gwenpool/gwenpool/__init__.py` (`_gwenpool_manches_intrigue`). Le drapeau
# est leve par `EteindreLesBoosts`, qui enregistre en meme temps sur
# l'IDENTITE du joueur (jamais sur l'obligation, qui part a la defausse
# aussitot apres) une capacite temporaire `WhenPlayerPhaseEnd` qui le
# rabaisse. « Until the end of the NEXT player phase » : l'obligation se
# revele en phase du vilain, la prochaine fin de phase JOUEUR est donc bien
# celle visee par le texte imprime.
#
# ---------------------------------------------------------------------------
# PIEGE DE NOMMAGE — le `*` d'unicite
#
# `cards/paper.py:45-46` retire le prefixe « * » d'un nom unique
# (`is_unique = name.startswith("* ")` puis `name = name.lstrip("* ")`). Un
# `CardFinder(name="* Wiccan")` ne trouverait JAMAIS rien, en silence. Les
# constantes ci-dessous sont donc ecrites SANS l'etoile.
#
# PIEGE DE NOMMAGE — la collision « Hulkling »
#
# wc002 est un ALLIE nomme « Hulkling » ; `56029a` est un HEROS OFFICIEL du
# meme nom (pack `cw`, deck `hulkling.json`). Une recherche par nom n'est PAS
# bornee au joueur par defaut (`from_where` -> `get_InPlay`), lecon deja payee
# sur `wolverine_x23`. Toute recherche de « Hulkling » dans ce pack passe donc
# par `HulklingEnJeuPour(player, effect)`, qui borne au joueur.
# ===========================================================================

NOM_WICCAN = "Wiccan"
NOM_BILLY = "Billy Kaplan"
NOM_HULKLING = "Hulkling"
NOM_MORIDUN = "Moridun"
NOM_CLOAK = "Wiccan's Cloak"
NOM_NEW_VESSEL = "New Vessel"
NOM_DEMIURGE = "The Demiurge"

# Les evenements [[SPELL]] du pack « qui comptent les icones de bonus d'une
# carte de rencontre » — la condition imprimee de wc016 Wiccan's Cloak. Liste
# etablie carte par carte sur le texte imprime : wc013 Transmutation est bien
# un SPELL, mais ne compte AUCUNE icone, elle en est donc exclue ; wc008
# Magic Manipulation en compte, elle y est, meme si elle se joue en alter-ego.
EVENEMENTS_QUI_COMPTENT_LES_BOOSTS = [
    "wc003", "wc004",           # Impenetrable Barrier
    "wc005", "wc006", "wc007",  # Magic Bolt
    "wc008",                    # Magic Manipulation
    "wc009", "wc010",           # Magic Portal
    "wc011", "wc012",           # Teleport
    "wc014",                    # Warping Reality
]

# Nom de l'attribut pose sur le monde par l'obligation wc018.
DRAPEAU_BOOSTS_ETEINTS = "_wiccan_boosts_eteints"


################################################################################
# Comptage des icones de bonus

def BoostsComptables(effect: 'Effect') -> bool:
    """Faux uniquement quand l'obligation wc018 a eteint le comptage."""
    return not getattr(effect.world, DRAPEAU_BOOSTS_ETEINTS, False)


def IconesBoostDuDessus(effect: 'Effect', player: 'Player|None'=None) -> int:
    """Nombre d'icones de bonus sur la carte du DESSUS du deck de rencontre.

    Rend 0 (et ne regarde meme pas le deck) quand l'obligation wc018 a eteint
    le comptage, et 0 quand le deck de rencontre est vide — deux resultats
    legitimes du texte imprime, pas des cas d'erreur a esquiver.
    """
    if not BoostsComptables(effect):
        return 0
    if player is None:
        player = effect.GetInitiator()
    if player is None:
        return 0
    faces = player.LookAtDeck("EncounterDeck", 1, effect)
    return FacesCounter.CountTotalBoostIcons(faces)


def EteindreLesBoosts(player: 'Player', effect: 'Effect') -> None:
    """Interrupteur de wc018 : plus aucune icone comptee jusqu'a la fin de la
    prochaine phase joueur. Enregistre sur l'IDENTITE du joueur, jamais sur
    l'obligation (qui est defaussee dans la foulee, ce qui emporterait ses
    capacites temporaires avec elle)."""
    setattr(effect.world, DRAPEAU_BOOSTS_ETEINTS, True)

    identite = player.GetIdentity()
    if identite is None:
        return

    def rallumer(eff: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        Unused(message)
        setattr(eff.world, DRAPEAU_BOOSTS_ETEINTS, False)

    identite.effect.RegisterTemp(
        AbilityFactory.WhenPlayerPhaseEnd(
            AbilityType.Temp2,
            rallumer,
        ),
        unregister_after_exec=True,
    )


################################################################################
# Recherches bornees (voir le piege de nommage ci-dessus)

def HulklingEnJeu(effect: 'Effect') -> bool:
    """Vrai si « Hulkling » est en jeu, en ALLIE ou en HEROS.

    Arbitrage de l'utilisateur du 30/08/2026 sur wc017 Royal Couple : le
    « Team-Up (Hulkling and Wiccan) » imprime est rendu comme une simple
    condition « Hulkling en jeu, allie OU heros », sans passer par la cle
    `desc.TeamUp` ni par `.SetTarget("TeamUp")` — meme traitement que `il023`
    Sudden Plan Change (Team-Up Stature and Iron Lad) chez le meme auteur.

    BORNAGE : la recherche ENUMERE explicitement les allies et les identites
    des joueurs (`Worlds.GetPlayers`), et ne passe JAMAIS par un
    `Worlds.FindCardsOnField(name="Hulkling")` nu. La distinction n'est pas
    cosmetique : une recherche par nom non bornee balaie tout `get_InPlay`,
    cartes de rencontre comprises (lecon `wolverine_x23`). Ici, les deux
    seules choses qui peuvent satisfaire la condition sont l'allie signature
    wc002 et le HEROS OFFICIEL Hulkling (`56029a`, pack `cw`, deck
    `hulkling.json`) — les deux lectures voulues d'un Team-Up, et rien
    d'autre.
    """
    for player in Worlds.GetPlayers(effect):
        identite = player.GetIdentity()
        if identite is not None and identite.IsName(NOM_HULKLING):
            return True
        for face in player.allies.Get():
            if face.IsName(NOM_HULKLING):
                return True
    return False


def MoridunEnJeu(effect: 'Effect') -> bool:
    """Vrai si l'attachement Moridun (wc020) est en jeu. Nom unique du pack,
    aucune collision connue : la recherche n'a pas besoin d'etre bornee."""
    return Worlds.FindCardsOnField(effect, name=NOM_MORIDUN) != []


def NewVesselEnJeu(effect: 'Effect') -> 'CardFace|None':
    """La manigance annexe New Vessel (wc019a) en jeu, ou None."""
    faces = Worlds.GetOnFieldSchemes(effect, CardFinder(name=NOM_NEW_VESSEL))
    return faces[0] if faces else None
