from cards.pack import *

# ===========================================================================
# NEW ULTIMATE WINTER SOLDIER (Dipsome, `uw`) — helpers partages du pack.
#
# LE MOTEUR DU PACK : « Discard 1 card from your hand AT RANDOM → <effet>, ...
# where X is equal to the numeral in the printed resource cost of that card ».
# Six cartes (uw004-uw008, uw013, uw016) le disent ; trois autres LISENT une
# defausse au hasard deja faite (uw002 Griffes, uw003 Phoenix, uw009 Mask).
#
# CE QUE LE MOTEUR FOURNIT (CORRECTIF du 25/10/2026, `player_action.py` et
# `world_stat.py`) :
#  - `joueur.DiscardRandomHandCards(1, effect, exclude=[carte jouee])` tire,
#    defausse, et pendant la defausse liste les faces tirees dans
#    `world.defausses_au_hasard` (c'est ce qui distingue une defausse AU HASARD
#    d'une autre dans `WhenCardWouldDiscard` / `AfterCardDiscard`) ;
#  - `world.stat.CountRandomDiscards(joueur)` : combien de cartes ce joueur a
#    defaussees au hasard CE ROUND (Wolverine's Claws).
# ===========================================================================
GRIFFES = "Wolverine's Claws"
GRIFFES_ID = "uw002"


def CoutImprime(face: 'CardFace|None') -> int:
    """« the numeral in the printed resource cost of that card » : 0 pour une carte sans cout imprime
    (ressource de base, carte d'identite)."""
    if face is None:
        return 0
    try:
        return max(0, int(FacesCounter.GetPrintedCost([face])))
    except Exception:
        return 0


def MainSansCetteCarte(effect: 'Effect') -> 'List[CardFace]':
    """La main du joueur, SANS la carte qu'il est en train de jouer (on ne se defausse pas soi-meme)."""
    joueur = effect.GetInitiator()
    return [face for face in joueur.hand_cards.Get() if face is not effect.this]


def UneCarteADefausser(effect: 'Effect', message=None) -> bool:
    """Condition des capacites dont le COUT est « discard 1 card from your hand at random » : il faut une AUTRE carte."""
    Unused(message)
    return len(MainSansCetteCarte(effect)) > 0


def DefausserAuHasard(targets: 'Sequence[CardFace]', effect: 'Effect') -> bool:
    """Le COUT « Discard 1 card from your hand at random → ». La carte tiree est gardee sur l'effet
    (`effect.uw_defaussee`) : le corps de la capacite en lit le cout imprime (X)."""
    Unused(targets)
    joueur = effect.GetInitiator()
    faces = joueur.DiscardRandomHandCards(1, effect, exclude=[effect.this])
    effect.uw_defaussee = faces[0] if faces else None
    return bool(faces)


def CoutDefausseAuHasard() -> 'CostFunc.Base':
    return CostFunc.Custom(None, DefausserAuHasard)


def XDeLaCarteDefaussee(effect: 'Effect') -> int:
    """X = « the numeral in the printed resource cost of that card »."""
    return CoutImprime(getattr(effect, "uw_defaussee", None))


def PayeeAvecLesGriffes(effect: 'Effect') -> bool:
    """« If you exhausted Wolverine's Claws to play this card » : la carte jouee a ete payee par la ressource des Griffes."""
    return any(
        getattr(e.this, "IsName", None) is not None and e.this.IsName(GRIFFES)
        for e in (getattr(effect.context, "paid_this_res_effects", None) or [])
    )


def DefausseAuHasard(message: 'Message.AfterCardDiscard|Message.WhenCardWouldDiscard') -> bool:
    """Cette defausse est-elle une defausse AU HASARD de la main ? (marque posee par `DiscardRandomHandCards`)."""
    return message.trigger in getattr(message.trigger.card.world, "defausses_au_hasard", [])


def MortParLeHeros(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
    """« After the attached minion is defeated BY WINTER SOLDIER » : le tueur est le HEROS du joueur qui a joue la
    carte (forme heros), ou un evenement de ce joueur (une attaque d'evenement : Deranged Burst...). Pas un allie,
    pas un sbire, pas l'alter ego."""
    joueur = effect.this.GetOwnerPlayer()
    if joueur is None:
        return False
    identite = joueur.GetIdentity()
    if not Hero.IsType(identite):
        return False
    tueur = message.killer
    if tueur is None:
        return False
    if tueur is identite:
        return True
    return Event.IsType(tueur) and tueur.GetOwnerPlayer() is joueur


def DeplacerSurUnAutreSbire(effect: 'Effect', message: 'Message.WhenUnitBeDefeated', joueur: 'Player', this: 'Upgrade') -> None:
    """« Winter Soldier may take 1 damage to attach this card to ANOTHER minion » : facultatif, il faut un autre sbire
    en jeu (le sbire vaincu n'en est pas un)."""
    vaincu = message.trigger
    if not any(Minion.IsType(f) and f is not vaincu for f in Worlds.GetOnFieldCards(effect)):
        return

    def deplacer(cibles: 'Sequence[CardFace]') -> None:
        joueur.GetIdentity().TakeDamage(this, 1, effect)
        this.AttachTo2(cibles[0], effect)

    joueur.MayChooseOneAbility(
        effect,
        AbilityFactory.ForChoiceAbility(
            "Take 1 damage → attach this card to another minion",
            deplacer,
        ).SetTarget(Minion, exclude=[vaincu]),
    )
