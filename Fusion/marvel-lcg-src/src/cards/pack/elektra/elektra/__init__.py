from cards.pack import *

# ===========================================================================
# Helpers du set « Elektra » (heros officiel, Hero Pack MC63). Plan : .planning/elektra-heros/PLAN.md.
#
# LE PAQUET NINJA : six cartes de rencontre (63002 x2 Ninja Stars, 63003 x2 Ninja Strike, 63004 x2 Ninja Vanish),
# set « Elektra Ninja ». Elles vivent dans `joueur.additional_deck` (modele : le deck Sense de Daredevil FNE,
# `fne/daredevil/60001b.py`) : mises de cote par `BeginGameWithSetAside` sur 63001b, puis posees face cachee dans
# `additional_deck` et melangees. « Melanger la carte du dessus du paquet NINJA dans le paquet de rencontre » =
# `MelangerDessusNinja`. Pas d'obligation ni de set nemesis (non publies, decision du 13/11/2026).
# ===========================================================================

NINJA_IDS = ('63002', '63002', '63003', '63003', '63004', '63004')
SET_ELEKTRA = "Elektra"
NOM_SAI = "Elektra's Sai"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (meme helper que les packs ares / iron_fist)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    return None


def MelangerDessusNinja(joueur: 'Player', effect: 'Effect') -> bool:
    """« Shuffle the top card of the NINJA deck into the encounter deck. » Rend False si le paquet Ninja est vide."""
    paquet = joueur.additional_deck
    if paquet.GetSize() == 0:
        return False
    face = paquet.GetTop()
    if face is None:
        return False
    Faces.ShuffleAllTo([face], Worlds.GetEncounterDeck(effect), effect)
    return True


def PouvoirDeBase(message: 'Message2') -> 'str|None':
    """Le pouvoir de BASE que la carte de boost est en train de renforcer : `"ATK"`, `"THW"`, `"DEF"`, ou None si Elektra agit par une
    carte (evenement d'attaque, capacite...). Lit le message `WhenUnitWould...` de la puissance en cours (`message.would_message`)."""
    would = getattr(message, "would_message", None)
    if would is None or not Hero.IsType(getattr(would, "trigger", None)):
        return None   # un ENNEMI (Rhino) qui active n'est pas « Elektra utilisant un pouvoir de base »
    if hasattr(would, "is_base_attack"):
        return "ATK" if would.is_base_attack else None
    prop = getattr(would, "property", None)
    if prop is None or not getattr(prop, "is_basic_power", False):
        return None
    if isinstance(would, Message.WhenUnitWouldThwart):
        return "THW"
    if isinstance(would, Message.WhenUnitWouldDefend):
        return "DEF"
    return None


def ElektraDuJoueur(joueur: 'Player|None') -> 'CardFace|None':
    """« Elektra » = l'identite du joueur (les deux faces sont la meme carte)."""
    return joueur.GetIdentity() if joueur is not None else None


def DonnerEnBoostA(face: 'CardFace', cible: 'CardFace|None', effect: 'Effect') -> None:
    """« Give this card to Elektra as a facedown boost card. » : la carte part dans la pile de boost de l'identite."""
    if cible is None or not CanBoost.IsType(cible):
        return
    cible.GiveBoostCard(face, effect)


def MelangerDansPaquetNinja(face: 'CardFace', joueur: 'Player', effect: 'Effect') -> None:
    """« Shuffle this card into the NINJA deck. » : la carte rejoint `additional_deck`, face cachee, visible de son proprietaire."""
    paquet = joueur.additional_deck
    Faces.MoveAllTo([face], paquet, effect)
    paquet.Shuffle(effect)
    for f in paquet.Get():
        f.FlipTo(effect, face_up=False)
        f.card.visible.Set(joueur)


def GagnerIconeBoostCetteResolution(face: 'CardFace', valeur: int, effect: 'Effect') -> None:
    """« That card gains [boost icon]. » : la carte de boost compte `valeur` icone(s) de plus POUR CETTE RESOLUTION seulement. L'icone est
    retiree des que `AfterCardBecomeBoost` part pour cette carte (sinon une carte re-melangee garderait l'icone)."""
    face.GainBoostIcons(valeur, effect)
    face.effect.RegisterTemp(
        Ability(
            AbilityType.Temp0,
            Message.AfterCardBecomeBoost,
            [lambda effet, message: message.trigger == face],
            lambda effet, message: face.GainBoostIcons(-valeur, effect),
        ),
        unregister_after_exec=True,
        until_turn_end=True,
    )


def GagnerPouvoir(would_message: 'Message2', puissance: str, valeur: int, effect: 'Effect') -> None:
    """« She gets +N to that power for this use. » : ATQ, THW ou DEF selon le pouvoir de base en cours. Primitives du message `WhenUnitWould...`
    (`GainTHWForThisThwart`, `GainDEFForThisAttack`), les seules qui couvrent aussi la DEFENSE (`TemporaryGain` ne la connait pas)."""
    if puissance == "ATK":
        would_message.GainATKForThisAttack(valeur, effect)
    elif puissance == "THW":
        would_message.GainTHWForThisThwart(valeur, effect)
    elif puissance == "DEF":
        would_message.GainDEFForThisAttack(valeur, effect)
