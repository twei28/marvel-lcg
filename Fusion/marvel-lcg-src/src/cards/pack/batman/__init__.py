from cards.pack import *

# ===========================================================================
# Pack BATMAN — contenu custom de « ES » (DC Custom Content by ES), version « Sealed 6.12.2022 ». Prefixe `bm`
# (tools/prefixes_fanmade.json). TROIS sets : `Batman` (bm001a-bm013, dossier batman/batman/), `Batman Nemesis`
# (bm014-bm017) et `Batman Deterrence` (bm018-bm022, les 5 cartes du deck de dissuasion). bm023-bm025 : ressources Basic, sans module.
#
# LE PACK EN UNE PHRASE : LE DECK DE DISSUASION. Batman part avec 15 cartes de dissuasion (5 titres x 3), en choisit 8 au Setup,
# puis en MELANGE une a la fois dans le deck de rencontre (a chaque attaque ou contre, 3 par round au plus). Ces cartes sont des
# TRAITRISES au trait DETERRENCE : elles se revelent comme les autres et se jouent aussi en boost.
#
# CONCEPTION (aucune regle du moteur n'est changee) : le deck de dissuasion est `joueur.additional_deck` (le « Special deck » que le
# plateau dessine deja), sa defausse est `joueur.additional_discard_pile`. Chaque carte de dissuasion porte `card.bind_discard_pile` =
# cette defausse : une carte RESOLUE (revelee, ou retournee en boost) y retourne toute seule. Une carte defaussee SANS avoir ete resolue
# (deck rencontre defausse par un effet) va dans la defausse auxiliaire du livret : on la note, et on la remelange dans le deck de
# rencontre quand l'effet qui l'a defaussee a fini (`AfterResolveEffect`).
#
# ⚠ Les modules d'un set font `from . import *` et les `__init__.py` des sets font `from cards.pack.batman import *` : tout ce que
# les cartes appellent vit ICI (lecon hk005 : sinon NameError avale par le moteur).
# ===========================================================================

TRAIT_DISSUASION = "DETERRENCE"
IDS_DISSUASION = ["bm018"] * 3 + ["bm019"] * 3 + ["bm020"] * 3 + ["bm021"] * 3 + ["bm022"] * 3
MAX_MELANGES_PAR_ROUND = 3
TAILLE_DECK_DISSUASION = 8


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier : il leve un assert quand l'initiateur
    n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    try:
        return effect.GetInitiator()
    except Exception:
        return None


def ChoisirUnEnnemi(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    ennemis = Worlds.GetOnFieldEnemies(effect)
    if not ennemis:
        return None
    return joueur.AskChooseFace(ennemis, effect)


def EtatBm(face: 'CardFace') -> dict:
    """Le carnet de notes d'une carte du pack (resolue ou non, annulee par Intimidate, compte de melanges...)."""
    etat = getattr(face, "bm_etat", None)
    if etat is None:
        etat = {}
        face.bm_etat = etat
    return etat


def EstDissuasion(face: 'CardFace|None') -> bool:
    return face is not None and face.HasTrait(TRAIT_DISSUASION)


def BatmanEnJeu(effect: 'Effect') -> 'CardFace|None':
    """« If Batman is in play » : l'identite Batman (forme HEROS) d'un joueur, sinon None (Bruce Wayne n'est pas Batman en jeu)."""
    return Worlds.FindCardOnField(effect, name="Batman", card_type=Hero)


def ProprietaireDissuasion(face: 'CardFace') -> 'Player|None':
    return EtatBm(face).get("joueur")


def EnAttente(joueur: 'Player') -> list:
    """La defausse AUXILIAIRE temporaire du livret : les cartes de dissuasion defaussees sans avoir ete resolues."""
    attente = getattr(joueur, "bm_attente", None)
    if attente is None:
        attente = []
        joueur.bm_attente = attente
    return attente


def RemelangerEnAttente(joueur: 'Player', effect: 'Effect') -> None:
    """Fin de l'effet qui a defausse : « shuffle the deterrence card/s back into the encounter deck »."""
    attente = EnAttente(joueur)
    if not attente:
        return
    faces = list(attente)
    attente.clear()
    joueur.bm_remelanges = getattr(joueur, "bm_remelanges", 0) + 1
    for face in faces:
        EtatBm(face)["resolu"] = False
    Faces.ShuffleAllTo(faces, Worlds.GetEncounterDeck(effect), effect)
    # Le livret dit de remelanger la dissuasion dans le deck rencontre : c'est « a deterrence card is shuffled into the encounter deck » (Two-Face, verdict du 26/10/2026).
    for _ in faces:
        ApresMelange(effect)


def RangerSiNonResolue(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
    """Crochet pose sur chaque carte de dissuasion : une carte non resolue qu'un effet defausse part en attente, puis revient."""
    face = effect.this
    etat = EtatBm(face)
    if etat.get("resolu"):
        return
    joueur = etat.get("joueur")
    if joueur is None:
        return
    attente = EnAttente(joueur)
    if face in attente:
        return
    premiere = not attente
    attente.append(face)
    if premiere:
        RunAt.AfterResolveEffect(effect, message.by_effect, lambda: RemelangerEnAttente(joueur, effect))


def PreparerDissuasion(joueur: 'Player', face: 'CardFace') -> None:
    """Lie une carte de dissuasion a son joueur : defausse liee (carte resolue) et crochet de defausse non resolue."""
    face.card.bind_discard_pile = joueur.additional_discard_pile
    etat = EtatBm(face)
    etat["joueur"] = joueur
    if not etat.get("crochet"):
        etat["crochet"] = True
        face.effect.Registers(
            AbilityFactory.WhenCardWouldDiscard(AbilityType.Temp0, "This", RangerSiNonResolue).NoOutOfPlayLimit())


def MarquerResolue(face: 'CardFace') -> None:
    EtatBm(face)["resolu"] = True


def AnnuleSurge(face: 'CardFace') -> bool:
    """Intimidate / Utility Belt : « cancel its surge effect » (lu par la carte au moment de gagner surge)."""
    return bool(EtatBm(face).get("sans_surge"))


def SurgeDeLaDissuasion(effect: 'Effect') -> None:
    this = effect.this
    if AnnuleSurge(this):
        return
    ThisCardGainSurge(effect)


def BoostSupplementaireAnnule(face: 'CardFace') -> bool:
    return bool(EtatBm(face).get("sans_boost_sup"))


def MonterLeDeckDeDissuasion(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
    """Setup : « the player selects 8 of the 15 deterrence cards to form the deterrence deck »."""
    joueur = effect.GetInitiator()
    if joueur is None:
        return
    quinze = [f for f in joueur.set_aside_deck.Get() if EstDissuasion(f)]
    if not quinze:
        return
    def former(retenues: Sequence['CardFace']) -> None:
        retenues = list(retenues)[:TAILLE_DECK_DISSUASION]
        autres = [f for f in quinze if f not in retenues]
        if autres:
            Faces.RemoveAllFromGame(autres, effect)
        Faces.FlipAllTo(retenues, False, effect)
        Faces.MoveAllTo(retenues, joueur.additional_deck, effect)
        for face in retenues:
            PreparerDissuasion(joueur, face)
            face.card.visible.Set(joueur)
        joueur.additional_deck.Shuffle(effect)
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility("Choose 8 deterrence cards to form your deterrence deck", former)
        .SetTarget(quinze, range=(TAILLE_DECK_DISSUASION, TAILLE_DECK_DISSUASION), not_move=True, not_shuffle=True),
    )


def MelangesCeRound(joueur: 'Player', effect: 'Effect') -> int:
    carnet = getattr(joueur, "bm_melanges", None)
    ronde = effect.world.round_id
    if carnet is None or carnet[0] != ronde:
        carnet = [ronde, 0]
        joueur.bm_melanges = carnet
    return carnet[1]


def ApresMelange(effect: 'Effect') -> None:
    """« Forced Response: After a deterrence card is shuffled into the encounter deck » (Two-Face, nemesis) : le moteur n'a aucun
    message pour ce melange, c'est donc la fonction qui melange qui reveille Two-Face (2 fois par round au plus)."""
    deux = Worlds.FindCardOnField(effect, name="Two-Face", card_type=Minion)
    if deux is None:
        return
    etat = EtatBm(deux)
    ronde = effect.world.round_id
    if etat.get("ronde") != ronde:
        etat["ronde"], etat["fois"] = ronde, 0
    if etat["fois"] >= 2:
        return
    etat["fois"] += 1
    deux.GainUntilRoundEnd(effect, scheme=1, attack=1)


def MelangerUneDissuasion(effect: 'Effect', joueur: 'Player|None'=None) -> bool:
    """« Choose a deterrence card and shuffle it into the encounter deck », 3 fois par round au plus."""
    joueur = joueur or JoueurDeCetteCarte(effect)
    if joueur is None:
        return False
    if MelangesCeRound(joueur, effect) >= MAX_MELANGES_PAR_ROUND:
        return False
    deck = joueur.additional_deck
    if deck.GetSize() == 0:
        deck.ShuffleWithDiscardPile(False, effect)
    faces = list(deck.Get())
    if not faces:
        return False
    fait = {"ok": False}
    def melanger(choisies: Sequence['CardFace']) -> None:
        for face in choisies:
            etat = EtatBm(face)
            etat["resolu"], etat["sans_surge"], etat["sans_boost_sup"] = False, False, False
            PreparerDissuasion(joueur, face)
            Faces.ShuffleAllTo([face], Worlds.GetEncounterDeck(effect), effect)
            joueur.bm_melanges[1] += 1
            fait["ok"] = True
            ApresMelange(effect)
    MelangesCeRound(joueur, effect)
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility("Choose a deterrence card to shuffle into the encounter deck", melanger)
        .SetTarget(faces, range=(1, 1), not_move=True, not_shuffle=True),
    )
    return fait["ok"]


def EstUneResolutionDeDissuasion(effect: 'Effect', message: 'Message.AfterEffectResolved') -> bool:
    """Batarangs / Utility Belt : « after resolving the When Revealed effect or boost ability of a deterrence card »."""
    capacite = message.effect.ability
    return capacite.flags.IsType(AbilityType.WhenRevealed) or capacite.flags.IsType(AbilityType.Boost)


def IconesDesCartesDefaussees(effect: 'Effect', defaussees: Sequence['CardFace']) -> int:
    """Livret de l'auteur : « If an effect references icons on a deterrence card that would have ended up in the discard pile, use the top card of
    the discard pile instead, otherwise discard another card for the purposes of that effect. » Les cartes DEJA defaussees par l'effet (la dissuasion
    est deviee vers la defausse auxiliaire par `RangerSiNonResolue`) : une carte ordinaire compte ses propres icones ; une dissuasion est remplacee par
    la carte du dessus de la defausse rencontre telle qu'elle etait AVANT l'effet (jamais une carte que l'effet compte deja), et a defaut par une
    AUTRE carte qu'on defausse (le dessus du deck rencontre, en sautant et en deviant les dissuasions)."""
    lues = [f for f in defaussees if not EstDissuasion(f)]
    a_remplacer = len(defaussees) - len(lues)
    if a_remplacer:
        pile = Worlds.GetEncounterDiscardPile(effect)
        dessous = [c.face for c in reversed(pile.cards) if c.face not in lues]
        for _ in range(a_remplacer):
            if dessous:
                lues.append(dessous.pop(0))
                continue
            deck = Worlds.GetEncounterDeck(effect)
            while deck.GetTop() is not None:
                autre = deck.GetTop()
                Faces.DiscardAll([autre], effect)
                if not EstDissuasion(autre):
                    lues.append(autre)
                    break
    return FacesCounter.CountTotalBoostIcons(lues) if lues else 0


def ReactionDeSplitDecision(effect: 'Effect', joueur: 'Player|None') -> None:
    """Split Decision (nemesis) — Forced Interrupt : when a deterrence card is revealed, discard the top card of the encounter deck. If that card has an
    odd number of boost icons, add 2 threat to the main scheme. Pas de message « carte de dissuasion revelee » reutilisable : chaque carte de
    dissuasion appelle cette fonction au debut de son When Revealed."""
    split = Worlds.FindCardOnField(effect, name="Split Decision")
    if split is None:
        return
    deck = Worlds.GetEncounterDeck(effect)
    dessus = deck.GetTop()
    if dessus is None:
        return
    Faces.DiscardAll([dessus], effect)
    if IconesDesCartesDefaussees(effect, [dessus]) % 2 == 1:
        split.PlaceThreatOnSchemes("MainScheme", 2, effect)


def JoueurRevelation(effect: 'Effect', message: 'Message2') -> 'Player|None':
    joueur = None
    try:
        joueur = message.GetToPlayer()
    except Exception:
        joueur = None
    return joueur or JoueurDeCetteCarte(effect)


def ReduireLActivation(message: 'Message.WhenCardBecomeBoost', valeur: int) -> None:
    """Boost « reduce the damage / the threat of this activation by N » : l'activation du moteur lit `property.additional_value` (enemy.py:265,
    meme champ que « attacks with +2 ATK ») ; on l'abaisse, le moteur ne descend jamais sous 0."""
    prop = None
    if getattr(message, "would_atk_message", None) is not None:
        prop = message.would_atk_message.property
    elif getattr(message, "would_sch_message", None) is not None:
        prop = message.would_sch_message.property
    if prop is not None:
        prop.additional_value -= valeur
