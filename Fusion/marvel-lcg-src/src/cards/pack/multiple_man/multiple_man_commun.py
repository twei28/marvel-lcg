from cards.pack import *

# ===========================================================================
# Helpers COMMUNS du pack Multiple Man (Dupes, complots annexes en zone de victoire, recherche d'un Dupe).
# ⚠ Importe par le `__init__.py` de CHAQUE set et du pack (precedent `sentry_commun.py`) : un helper defini dans le `__init__.py` du PACK leve un NameError avale par le
# moteur (lecon hk005).
# ===========================================================================
NOM_DUPE = "Dupe"
NOM_HEROS = "Multiple Man"
NOM_JAMIE = "Jamie Madrox"
NOM_PRIME = "Madrox Prime"
NOM_AGENT = "Madrox, Agent of S.H.I.E.L.D."
NOM_TRAGEDY = "Prepare For Future Tragedy"
NOM_BAD = "Dupes Gone Bad"
NOM_EMPEROR = "Emperor Madrox"


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


def NomNet(face: 'CardFace') -> str:
    return face.paper.name.lstrip("* ").strip()


def EstDupe(face: 'CardFace|None') -> bool:
    """« a Dupe ally » = un ALLIE dont le NOM est Dupe (decision de lecture : Duplicate est un trait sans effet, RRG « Traits »)."""
    return face is not None and Ally.IsType(face) and NomNet(face) == NOM_DUPE


def DupesDuJoueur(joueur: 'Player') -> 'List[CardFace]':
    return [f for f in joueur.allies.Get() if EstDupe(f)]


def DupesEnJeu(effect: 'Effect') -> 'List[CardFace]':
    """Tous les Dupe en jeu (« for each Dupe ally in play »)."""
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Ally) if EstDupe(f)]


def EnVitrine(effect: 'Effect', nom: str) -> bool:
    """La carte de ce nom est-elle dans la zone de victoire ? (RECETTES §3bis : la capacite vit sur l'IDENTITE, la zone de victoire est une condition externe.)"""
    return any(NomNet(f) == nom for f in Worlds.VictoryDisplay(effect).GetAll())


def ChercherEtMettreUnDupe(effect: 'Effect', joueur: 'Player', *, different_de: 'CardFace|None' = None, epuise: bool = False) -> 'CardFace|None':
    """« Search your deck, hand, and discard pile for a Dupe ally and put it into play » (RRG « Search » : le deck consulte est melange ; `different_de` : « a DIFFERENT
    Dupe ally » = une autre carte que celle qui vient d'etre defaussee)."""

    def convient(eff: 'Effect', face: 'CardFace') -> bool:
        return EstDupe(face) and face is not different_de

    dupe = Search.PlayerCard(
        effect,
        joueur,
        include_player_deck=True,
        include_discard_pile=True,
        include_player_hand_cards=True,
        finder=CardFinder(card_type=Ally, name=NOM_DUPE, check_effect_fn=convient),
    )
    if dupe is not None:
        dupe.PutIntoPlay(joueur, effect, exhaust=True) if epuise else dupe.PutIntoPlay(joueur, effect)
    return dupe


def CapaciteSeparateLives() -> 'List[Ability]':
    """Separate Lives (les 4 Dupe) : « Exhaust this card → generate its printed resource to pay for an identity-specific card » (modele 21006 / `FacesCounter.GetPrintedResources`)."""

    def imprimee(effect: 'Effect', message: Any) -> 'Resources|None':
        Unused(message)
        return FacesCounter.GetPrintedResources([effect.this])

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            for_card=CardFinder(card_class="IdentitySpecific"),
            resources_fn=imprimee,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]


def CapacitesPlateauJoueur(effet_reponse: 'Callable[[Effect, Player, CardFace], None]') -> 'List[Ability]':
    """Les trois complots annexes JOUEUR (Madrox Prime, Madrox Agent of S.H.I.E.L.D., Prepare For Future Tragedy) :
    - jouable depuis la main (`CanPlayThisSchemeCard`, modele `dt096`) ;
    - « Only a Dupe ally can remove threat from this scheme » : `ThreatCannotBeRemovedFromWhile("This", by_character=CardFinder(non_name=Dupe))` (modele `bc004`) ; DECISION UTILISATEUR (04/11) : les evenements
      et Reabsorb Dupe ne peuvent pas en retirer (leur `by_face` n'est pas un Dupe) ;
    - Hero Response : « After this side scheme is defeated, return the Dupe ally that defeated it to your hand → <effet> » (modele `dt096` : `WhenSchemeBeDefeated(HeroResponse, 'This', op)`).
    Le bonus « While ... is in the victory display » vit sur l'IDENTITE (RECETTES §3bis), pas ici."""

    def reponse(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurDeCetteCarte(effect)
        tueur = message.killer
        if joueur is None or not EstDupe(tueur):
            return
        # « return the Dupe ally that defeated it to your hand → » : le renvoi est le COUT de l'effet.
        if tueur not in Faces.ReturnToHand([tueur], "Owner", effect):
            return
        effet_reponse(effect, joueur, tueur)

    return [
        AbilityFactory.CanPlayThisSchemeCard(),
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(non_name=NOM_DUPE),
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.HeroResponse,
            'This',
            reponse,
        ),
    ]


# ---------------------------------------------------------------------------
# Bonus portes par l'IDENTITE (RECETTES §3bis : une capacite posee sur la manigance elle-meme ne part jamais une fois en zone de victoire). Les deux faces portent les bonus qui ne dependent pas de la forme
# (limite d'allies, Tenace des Dupe) ; la face HEROS porte ceux qui visent les stats du heros. Modele : `conan/conan/__init__.py::CapacitesCitadelle` (`ThisGainKeyword(fn, .., change_on_event=OnEvent.Victory(..))`).
# ---------------------------------------------------------------------------
def prime_en_vitrine(effect: 'Effect') -> bool:
    return EnVitrine(effect, NOM_PRIME)


def agent_en_vitrine(effect: 'Effect') -> bool:
    return EnVitrine(effect, NOM_AGENT)


def tragedy_en_vitrine(effect: 'Effect') -> bool:
    return EnVitrine(effect, NOM_TRAGEDY)


def _vitrine(nom: str) -> Any:
    return OnEvent.Victory(CardFinder(name=nom))


def BonusStatsHeros(nom: str, **stats: int) -> 'Ability':
    """« While <nom> is in the victory display, Multiple Man gains +N <stat> » : sur la face HEROS."""
    return AbilityFactory.ThisGainKeyword(
        lambda effect, ui: 1 if EnVitrine(effect, nom) else 0,
        change_on_event=_vitrine(nom),
        **stats,
    ).SetName(nom)


def CapacitesCommunesIdentite() -> 'List[Ability]':
    """Ce qui vaut quelle que soit la forme : limite d'alliés +1 (Agent), Tenace des Dupe (Tragedy)."""
    dupes = CardFinder(card_type=Ally, name=NOM_DUPE)
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", ally_limit=1, condition=agent_en_vitrine, change_on_event=_vitrine(NOM_AGENT)),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(dupes, toughness=1, condition=tragedy_en_vitrine, change_on_event=_vitrine(NOM_TRAGEDY)),
    ]
