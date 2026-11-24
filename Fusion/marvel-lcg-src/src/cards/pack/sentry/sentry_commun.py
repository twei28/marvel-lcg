from cards.pack import *

# ===========================================================================
# Helpers COMMUNS aux trois sets du pack Sentry (balance counters, Duality Aspect, Void).
# ⚠ Importe par le `__init__.py` de CHAQUE set (precedent `cards/pack/aoa/infinites.py`) : un helper defini dans le `__init__.py` du PACK leve un NameError
# avale par le moteur (lecon hk005).
# ===========================================================================
NOM_EQUILIBRE = "balance"        # « balance counter » (Duality Aspect, set heros)
NOM_SUBMERSION = "overwhelm"     # « overwhelm counter » (Merged Sentry)
NOM_DUALITE = "Duality Aspect"
NOM_VOID = "Void"
NOM_SENTRY = "Sentry"
NOM_MERGED = "Merged Sentry"


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `effect.GetInitiator()` en premier : il leve un assert quand l'initiateur n'est pas un joueur)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    return None


def Dualite(effect: 'Effect') -> 'CardFace|None':
    """La carte Duality Aspect en jeu (une seule par partie solo ; en multi, la premiere trouvee)."""
    return Worlds.FindCardOnField(effect, name=NOM_DUALITE, card_type=Upgrade)


def CartesAvecEquilibre(effect: 'Effect') -> 'List[CardFace]':
    """Toutes les cartes en jeu qui portent au moins un balance counter."""
    return [f for f in Worlds.FindCardsOnField(effect)
            if CanPlaceCounter.IsType(f) and f.CastTo(CanPlaceCounter).GetCounters(NOM_EQUILIBRE) > 0]


def EquilibreEnJeu(effect: 'Effect') -> int:
    """« the number of balance counters in play » : la SOMME sur toutes les cartes en jeu (Duality Aspect, The Watchtower...)."""
    return sum(f.CastTo(CanPlaceCounter).GetCounters(NOM_EQUILIBRE) for f in CartesAvecEquilibre(effect))


def EquilibreSurDualite(effect: 'Effect') -> int:
    """« X = le nombre de balance counters sur Duality Aspect » (Golden Guardian, Void)."""
    dualite = Dualite(effect)
    if dualite is None or not CanPlaceCounter.IsType(dualite):
        return 0
    return dualite.CastTo(CanPlaceCounter).GetCounters(NOM_EQUILIBRE)


def PoserEquilibre(effect: 'Effect', nombre: int = 1) -> int:
    """Pose `nombre` balance counters SUR Duality Aspect (le message `WhenCardWouldBePlacedCounter` laisse The Watchtower les detourner)."""
    dualite = Dualite(effect)
    if dualite is None or nombre <= 0:
        return 0
    return Faces.PlaceCountersOn([dualite], nombre, NOM_EQUILIBRE, effect) or 0


def RetirerEquilibre(effect: 'Effect', nombre: int) -> int:
    """Retire jusqu'a `nombre` balance counters DE LA PARTIE : d'abord Duality Aspect, puis les autres cartes. Rend le nombre retire."""
    restant = nombre
    retires = 0
    cartes = CartesAvecEquilibre(effect)
    cartes.sort(key=lambda f: 0 if f.paper.name.lstrip("* ") == NOM_DUALITE else 1)
    for carte in cartes:
        if restant <= 0:
            break
        possede = carte.CastTo(CanPlaceCounter).GetCounters(NOM_EQUILIBRE)
        a_retirer = min(restant, possede)
        if a_retirer > 0:
            Faces.RemoveCountersOn([carte], a_retirer, NOM_EQUILIBRE, effect)
            restant -= a_retirer
            retires += a_retirer
    return retires


def TrouverEtRevelerVoid(effect: 'Effect', joueur: 'Player') -> 'CardFace|None':
    """« Find Void and reveal him. (If he is already in play, he engages you.) » : meme recette que Meticulous Targeting (ca016)."""
    void = Worlds.FindCardOnField(effect, name=NOM_VOID, card_type=Enemy)
    if void is not None:
        if Minion.IsType(void) and void.CastTo(Minion).engaged_player is not joueur:
            void.CastTo(Minion).EngagePlayer(joueur, effect)
        return void
    void = Search.EncounterCard(effect, joueur, include_discard_pile=True, include_set_aside=True, name=NOM_VOID)
    if void is not None:
        void.Reveal(joueur, effect)
    return void


# ---------------------------------------------------------------------------
# SPLIT / « Special » (insert du pack) : le Void resout le Special de la carte SPLIT du DESSUS de la defausse du joueur Sentry ; apres chaque Special resolu,
# Duality Aspect remelange la carte SPLIT dans le deck (ou, si Monster of Antithesis est en jeu, la glisse FACE CACHEE sous lui ; 5 cartes dessous = defaite).
# ---------------------------------------------------------------------------
NOM_MONSTER = "Monster of Antithesis"
CARTES_SOUS_MONSTER_POUR_PERDRE = 5


def JoueurSentry(effect: 'Effect') -> 'Player|None':
    """Le joueur qui joue Sentry / Robert Reynolds (son identite porte l'un des deux noms), sinon None."""
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is not None and identite.paper.name.lstrip("* ") in (NOM_SENTRY, "Robert Reynolds"):
            return joueur
    return None


def CartesSplitDansLaDefausse(joueur: 'Player') -> 'List[CardFace]':
    """Les cartes SPLIT de la defausse du joueur, du FOND vers le DESSUS (le dernier element est le dessus)."""
    return [f for f in joueur.discard_pile.Get() if f.HasTrait("SPLIT")]


def Monster(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name=NOM_MONSTER)


def RemelangerOuGlisser(effect: 'Effect', joueur: 'Player', carte: 'CardFace') -> None:
    """« shuffle that card into your deck » ; si Monster of Antithesis est en jeu : « place it facedown under this scheme instead » (son Forced Interrupt, applique ici
    parce que le moteur n'a pas de message « would be shuffled »). Cinq cartes dessous : les joueurs perdent la partie."""
    monstre = Monster(effect)
    if monstre is not None:
        monstre.TuckCardUnderHere(carte, effect)
        if len(monstre.GetPlacedCardArea().Get()) >= CARTES_SOUS_MONSTER_POUR_PERDRE:
            Worlds.SetGameOver(False, effect)
    else:
        Faces.ShuffleAllTo([carte], joueur.player_deck, effect)


def VoidEnJeu(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name=NOM_VOID, card_type=Enemy)


def AutresEnnemis(effect: 'Effect') -> 'List[CardFace]':
    """Les ennemis en jeu AUTRES que le Void."""
    return [e for e in Worlds.FindCardsOnField(effect, card_type=Enemy) if e.paper.name.lstrip("* ") != NOM_VOID]


def PersonnagesDuJoueur(joueur: 'Player') -> 'List[CardFace]':
    """« each character under your control » : l'identite et les allies en jeu du joueur."""
    return [f for f in joueur.GetControlCards() if f.IsInPlay() and (Hero.IsType(f) or AlterEgo.IsType(f) or Ally.IsType(f))]
