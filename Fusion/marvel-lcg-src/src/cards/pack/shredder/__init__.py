from cards.pack import *

# ===========================================================================
# Helpers partages du pack SHREDDER (Inkwire, TMNT Enemies / Shredder v3,
# prefixe `ts`) : le vilain, son deck et ses trois ensembles modulaires
# (Chunin, Foot Goon Squad, Shadow of the Foot).
#
# ⚠ HOMONYMES : Foot Goon Squad contient Bebop (`ts201`) et Rocksteady
# (`ts205`) en SBIRES ; le vilain « Bebop & Rocksteady » du pack `tk` a ses
# propres card_id. Aucune recherche de ce pack ne passe par le NOM seul d'un
# personnage : toujours un `card_id` (`IDS_SHREDDER`, `IDS_KARAI`).
# ⚠ « Cloak X » = poser la carte d'etat Cloaked (fiches cloak.md, cloaked.md).
# L'encart du scenario (« Shredder Insert ») est de la REGLE, pas une carte :
# il est code ici et dans cloaked.py / can_status.py (une seule carte Cloaked par
# personnage, sauf Shredder : 2, 3 ou 4 selon son stade).
# ===========================================================================

IDS_SHREDDER = ["ts001", "ts002", "ts003"]
# « Karai » : la minion du set Chunin (ts101) et la Karai NEMESIS de Leonardo
# (tl015) sont le MEME personnage (meme titre, unique) : le texte imprime
# « Karai » designe l'une ou l'autre.
IDS_KARAI = ["ts101", "tl015"]


def TrouverShredder(effect: 'Effect') -> 'Villain|None':
    """Le vilain Shredder en jeu (par card_id, jamais par le nom)."""
    return Worlds.FindCardOnField(effect, card_ids=IDS_SHREDDER)


def Cloak(effect: 'Effect', face: 'CardFace|None') -> bool:
    """« Cloak <face> » : pose une carte d'etat Cloaked. Rend True si elle a ete
    posee (False : cible absente, ou deja au maximum de cartes Cloaked, voir
    `CanStatus.cloaked_max`)."""
    if face is None:
        return False
    return Faces.GiveStatus([face], "Cloaked", effect) > 0


def FaceCacheeAuPremierJoueur(effect: 'Effect', this: 'CardFace') -> None:
    """« Deal this card to the first player as a facedown encounter card »
    (boost). Modele tl015 / bw021 : une carte de boost est rangee par le moteur
    APRES la resolution de son effet ; on detourne donc son rangement
    (`WhenCardWouldDiscard` -> `SetToArea`) vers les cartes distribuees."""
    premier = Worlds.GetFirstPlayer(effect)
    if premier is None:
        return

    def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
        message2.SetToArea(premier.dealt_encounter_cards)

    this.effect.RegisterTemp(
        AbilityFactory.WhenCardWouldDiscard(AbilityType.Temp0, "This", rediriger),
        unregister_after_exec=False,
        until_round_end=True,
    )


def RevelerLePlusHautDeLaDefausse(effect: 'Effect', joueur: 'Player', finder: 'CardFinder2') -> 'CardFace|None':
    """« reveal the topmost <X> in the encounter discard pile » : rend la carte
    revelee, ou None si la defausse n'en contient pas."""
    face = Worlds.GetEncounterDiscardPile(effect).FindTopmost(finder)
    if face:
        face.Reveal(joueur, effect)
    return face


def ShredderAttaqueSansBoost(effect: 'Effect', joueur: 'Player', **rappels) -> None:
    """« Shredder attacks you. Do not give Shredder any boost cards for this
    activation. » (Disarming Assault, Shred)."""
    shredder = TrouverShredder(effect)
    if shredder:
        shredder.DoAttackYou(joueur, effect, property=AttackProperty(do_not_give_boost=True), **rappels)


def CapacitesDeShredder(stade: int, cartes_par_phase: int = 1) -> List['Ability']:
    """Le socle des trois stades : maximum de cartes Cloaked (1 + stade) et
    Reponse forcee « after the villain phase ends, give Shredder N cloaked
    status cards »."""
    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this
        for _ in range(cartes_par_phase):
            Cloak(effect, this)

    return [
        AbilityFactory.ThisCanHaveAdditionalCloaked(stade),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", fin_de_phase),
    ]


def EstUneAttaque(message: 'Message.WhenCardBecomeBoost') -> bool:
    """« If this activation is an attack » : le message de boost porte
    `would_atk_message` seulement pendant une attaque (sender_card.py)."""
    return isinstance(message.being_message, Message.WhenUnitBeingAttack)
