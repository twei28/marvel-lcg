from cards.pack import *

# ===========================================================================
# Modulaire IMPERIAL GUARD (Galactic Storm, Kajislav) — gs091-gs113. Lot GS-4, 20/10/2026.
# Livret 1.2 p.8 et insert du set. 23 cartes ; une fois le set choisi pour un scenario, on n'en garde que NEUF : un
# environnement au hasard, six sbires au hasard et LES DEUX traitrises (`random_pick` du fichier
# data/encounter_sets/gs_imperial_guard.json, applique par `CardFactory.RandomPick` quand le deck rencontre est forme).
# Les environnements portent « Setup » : celui qui a ete garde commence la partie en jeu (aucun script pour cela, base
# automatique `desc.Setup`, fiche setup.md) ; il reste donc UN seul environnement SETTING en jeu.
#
# Regle commune aux dix-huit sbires : chaque « When Revealed » fait UN effet imprime ; « If you cannot » (ou une clause
# equivalente) renvoie a la capacite « Special » de l'environnement SETTING en jeu (`ResoudreLeSpecial`). « You » est le
# joueur a qui le sbire est revele (`message.GetToPlayer()`) : meme joueur quand Hobgoblin ou Imperial Formation resolvent
# le « When Revealed » d'un autre sbire (`Faces.ResolveAbility`, modeles sm 27083 / sk046).
# ===========================================================================

IG = "IMPERIAL GUARD"
SETTING = "SETTING"


def EnvironnementSetting(effect: 'Effect') -> 'CardFace|None':
    """L'environnement SETTING en jeu (il n'y en a qu'un : « When Revealed: Discard each other SETTING environment »)."""
    for face in Worlds.GetOnFieldEnvironment(effect):
        if face.IsInPlay() and face.HasTrait(SETTING):
            return face
    return None


def ResoudreLeSpecial(effect: 'Effect', joueur: 'Player') -> bool:
    """« resolve the "Special" ability on the SETTING environment ». Rien si aucun SETTING n'est en jeu."""
    environnement = EnvironnementSetting(effect)
    if environnement is None:
        return False
    return environnement.ResolveSpecialAbility(joueur, effect)


def QuandRevele(effet_imprime: Callable[['Effect', 'Player'], bool]) -> 'Ability':
    """Le « When Revealed » d'un sbire Imperial Guard : `effet_imprime(effect, joueur)` rend VRAI quand l'effet a pu
    etre resolu ; FAUX renvoie au Special de l'environnement SETTING."""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        if not effet_imprime(effect, joueur):
            ResoudreLeSpecial(effect, joueur)

    return AbilityFactory.WhenThisRevealed(None, revele)


def SbiresImperialGuard(effect: 'Effect', *, sauf: 'CardFace|None' = None) -> List['CardFace']:
    """Les sbires IMPERIAL GUARD EN JEU (hors `sauf`)."""
    return [f for f in Worlds.GetOnFieldMinions(effect)
            if f.IsInPlay() and f.HasTrait(IG) and f is not sauf]


def CartesAvecRessourceImprimee(cartes: Sequence['CardFace'], couleur: str) -> List['CardFace']:
    """Les cartes qui portent au moins une icone de cette couleur LA OU ELLES SONT (conversions comprises, comme
    binary/__init__.py `EnergieDeLaCarte`). Une carte sans ressource n'en porte aucune."""
    return [f for f in cartes if FacesCounter.GetPrintedResourcesCount([f], couleur) > 0]


def DefausserUneDeLaMain(effect: 'Effect', joueur: 'Player', couleur: str) -> bool:
    """« Discard a [<couleur>] resource from your hand » : une CARTE de la main portant l'icone, au choix du joueur."""
    candidates = CartesAvecRessourceImprimee(list(joueur.hand_cards.Get()), couleur)
    return DefausserUneParmi(effect, joueur, candidates)


def DefausserUneParmi(effect: 'Effect', joueur: 'Player', candidates: Sequence['CardFace']) -> bool:
    """Le joueur choisit une carte parmi `candidates` et la defausse. Faux s'il n'y en a pas ou si rien n'est defausse."""
    candidates = [f for f in candidates if f is not None]
    if not candidates:
        return False
    choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect)
    if choisie is None:
        return False
    return bool(Faces.DiscardAll([choisie], effect))


def EstSpecifiqueAuScenario(face: 'CardFace') -> bool:
    """« scenario specific » : carte de rencontre propre au scenario (Rick Jones, Lilandra...), classe `Encounter`."""
    return bool(face.IsClass("Encounter"))


def DefausserJusquAuSbireIG(effect: 'Effect') -> 'Minion|None':
    """« Discard cards from the encounter deck until you discard an IMPERIAL GUARD minion ». On defausse la carte du
    dessus UNE A UNE (`Worlds.DiscardEncounterCards(1)`), le moteur gerant le deck vide (modele baxter_stockman
    `DefausserJusquAuSbire` ; `Deck.DiscardUntil` rend None des que le deck se vide, meme sur la carte cherchee).
    Borne par la taille du deck et de la defausse : aucune boucle sans fin si le set n'a plus de sbire."""
    from game.player.action.player_action import PlayerAction
    deck = Worlds.GetEncounterDeck(effect)
    defausse = Worlds.GetEncounterDiscardPile(effect)
    borne = deck.GetSize() + defausse.GetSize() + 1
    trouve: 'Minion|None' = None
    for _ in range(borne):
        faces = Worlds.DiscardEncounterCards(1, effect)
        if not faces:
            break
        if Minion.IsType(faces[0]) and faces[0].HasTrait(IG):
            trouve = faces[0]
            break
    PlayerAction.NoterRecherche(effect.world, [trouve] if trouve else [], fouille_paquet=True)
    return trouve


def EnvironnementImperialGuard() -> 'Ability':
    """« When Revealed: Discard each other SETTING environment in play » (les trois environnements)."""

    def remplacer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        Worlds.DiscardEachOther(effect, effect.this, trait=SETTING, card_type=Environment)

    return AbilityFactory.WhenThisRevealed(None, remplacer)
