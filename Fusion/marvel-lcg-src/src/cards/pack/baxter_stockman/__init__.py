from cards.pack import *
from cards.pack.donatello.donatello_nemesis import CapacitesEssaim

# ===========================================================================
# Scenario « Baxter Stockman » v3 (Inkwire, TMNT Villains / TMNT Modulars),
# pack `baxter_stockman`, prefixe de card_id `tx`. Fiche d'ensemble :
# .planning/tmnt/baxter-phase-a.md ; questions en attente :
# .planning/tmnt/baxter-questions.md.
#
#   tx001-tx003  Baxter Stockman I a III (vilain)
#   tx004a/b     Baxter's Laboratory (manigance principale ; la 1B porte le SPECIAL « Replicate »)
#   tx005-tx011  set de rencontre « Baxter's Lab »
#   tx012-tx014  set modulaire « Cyber Swarm »
#   tx015-tx016  set modulaire « High Speed »
#   tx017-tx018  set modulaire « Security Protocol »
#   dazed        6e carte d'etat du moteur (src/cards/pack/status/dazed.py)
#
# ⚠ HOMONYMES. « * Baxter Stockman » est AUSSI le SBIRE nemesis de Donatello (td015) :
# jamais de recherche par le nom seul, toujours par card_id (`IDS_BAXTER`) ou par type.
#
# ⚠ BASES AUTOMATIQUES (aucun script, lues dans `desc`) : Toughness (tx001-tx003), Hinder
# (tx010), Quickstrike (tx015), Guard et Patrol (tx017), Crisis et Acceleration (tx010,
# tx018 pour la Crise).
# ===========================================================================

IDS_BAXTER: List[str] = ["tx001", "tx002", "tx003"]
ID_PLAGUE = "tx007"            # Plague of M.O.U.S.E.R.S.
ID_MANIGANCE_B = "tx004b"      # Baxter's Laboratory, face 1B (porte le Special)
NOM_DU_SPECIAL = "Replicate"   # le nom imprime de la capacite Special (le journal lit « resolves Replicate »)
TRAIT_SWARM: 'CardFace.TRAITS' = "SWARM"

# « Place 1 ALL-PURPOSE counter on each SWARM minion » : FAQ officielle (MC4DB, 29/09/2026,
# deja notee dans gmw/16034) : « the card that an all-purpose counter is on defines the type of
# that counter ». Chaque sbire SWARM a SON compteur nomme, que le moteur retrouverait par
# `'all-purpose'` tant qu'il en porte un ; on le DONNE par card_id pour que le compteur reste du
# bon type meme quand le sbire n'en a plus (Roadkill Rodneys apres avoir retire ses cables).
COMPTEUR_DU_SBIRE: Dict[str, 'CardFace.COUNTER'] = {
    "tx007": "swarm",   # Plague of M.O.U.S.E.R.S.
    "tx012": "swarm",   # Flight of Flyborgs
    "tx013": "ooze",    # Superfly
    "tx015": "cable",   # Roadkill Rodneys
    "tx017": "shield",  # Auto Defense Bots
    "td016": "swarm",   # Plague of M.O.U.S.E.R.s (Donatello Nemesis)
    "td017": "swarm",   # Flight of Flyborgs (Donatello Nemesis)
}


def CompteurDe(face: 'CardFace') -> 'CardFace.COUNTER|Literal["all-purpose"]':
    """Le compteur nomme d'un sbire SWARM (voir COMPTEUR_DU_SBIRE), sinon `all-purpose`."""
    return COMPTEUR_DU_SBIRE.get(face.paper.card_id, "all-purpose")


def PlacerUnCompteurSur(face: 'CardFace', nombre: int, effect: 'Effect') -> None:
    Faces.PlaceCountersOn([face], nombre, CompteurDe(face), effect)


def ManiganceDuLabo(effect: 'Effect') -> 'MainScheme|None':
    """La manigance principale Baxter's Laboratory (face 1B en jeu), ou None."""
    for scheme in Worlds.GetMainSchemes(effect):
        if scheme.paper.card_id == ID_MANIGANCE_B:
            return scheme
    return None


def ResoudreLeSpecial(effect: 'Effect', joueur: 'Player') -> bool:
    """« (<joueur>) resolves the "Special" on the Baxter's Laboratory scheme. »

    Rend False quand la manigance n'est pas (ou plus) en jeu : rien a resoudre.
    """
    scheme = ManiganceDuLabo(effect)
    if scheme is None:
        return False
    return scheme.ResolveSpecialAbility(joueur, effect, name=NOM_DU_SPECIAL)


def AuDebutDeLaPhaseDuMechant() -> 'Ability':
    """« Forced Interrupt: When the villain phase begins, each player resolves the "Special" on
    the Baxter's Laboratory scheme. » (tx001, tx002, tx003 : mot pour mot le meme texte.)

    Chaque joueur, dans l'ordre du tour (le premier joueur d'abord), resout le Special : la
    manigance lit `message.GetToPlayer()` pour savoir QUI (« engaged with YOU », « deal YOURSELF »).
    """
    def chaque_joueur(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        Players.ForEachPlayer(effect, lambda joueur: ResoudreLeSpecial(effect, joueur))

    return AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, chaque_joueur)


def DefausserJusquAuSbire(effect: 'Effect') -> 'Minion|None':
    """« Discard cards from the top of the encounter deck until a minion is discarded. »

    On defausse la carte du dessus UNE A UNE (`Worlds.DiscardEncounterCards(1)`) jusqu'a tomber sur un
    sbire : c'est le moteur qui applique la regle du deck de rencontre VIDE (la defausse est melangee dans
    le deck, un pion Acceleration est pose, on continue).

    ⚠ PAS `Worlds.DiscardEncounterCardsUntil` : `Deck.DiscardUntil` rend None des que le deck se vide, meme
    quand la derniere carte defaussee est le sbire cherche, puis ne continue PAS apres le remelange du deck
    epuise (cas « un sbire en defausse, deck sans sbire » : le sbire n'etait jamais revele, mesure du
    16/10/2026). Bornee par le nombre de cartes du deck et de la defausse : aucune boucle sans fin si le
    jeu ne contient aucun sbire.
    """
    from game.player.action.player_action import PlayerAction
    deck = Worlds.GetEncounterDeck(effect)
    defausse = Worlds.GetEncounterDiscardPile(effect)
    borne = deck.GetSize() + defausse.GetSize() + 1
    trouve: 'Minion|None' = None
    for _ in range(borne):
        faces = Worlds.DiscardEncounterCards(1, effect)
        if not faces:
            break
        if Minion.IsType(faces[0]):
            trouve = faces[0]
            break
    # Meme publication que `Worlds.DiscardEncounterCardsUntil` : la fouille se lit sur la carte revelee.
    PlayerAction.NoterRecherche(effect.world, [trouve] if trouve else [], fouille_paquet=True)
    return trouve
