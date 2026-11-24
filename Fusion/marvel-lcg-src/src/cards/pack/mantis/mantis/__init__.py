from cards.pack import *
# Helpers partages du set « Mantis » (⚠ un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
NOM_EMPATHETIC_ADVANTAGE = "Empathetic Advantage"
NOM_EA_PERSONNAGE = "Empathetic Advantage (character)"
NOM_MADONNA_ENNEMI = "The Celestial Madonna : Empathetic Advantage"
NOM_MADONNA_PERSONNAGE = "The Celestial Madonna : Empathetic Advantage (character)"
NOM_MANTIS = "Mantis"


def CarteMantis(face: 'CardFace') -> bool:
    """« a Mantis card » : une carte de classe Hero propre a l'identite (le deck de heros de Mantis ; jamais une carte d'aspect)."""
    return face.IsClass("IdentitySpecific")


def ChercherAuSommet(effect: 'Effect', joueur: 'Player', profondeur: int=3) -> 'CardFace|None':
    """« Search the top N cards of your deck for a card and add it to your hand. Shuffle your deck. »

    `Search.PlayerDeckTop` ouvre la fenetre de cartes sur les N du dessus et MELANGE le deck quand une carte en sort (SelectorEnd) : c'est le « Shuffle your deck »
    imprime. Modele : `jj013` (carte prise puis `GainCard`)."""
    face = Search.PlayerDeckTop(effect, joueur, profondeur)
    if face is None:
        return None
    joueur.GainCard(face, effect)
    return face


def RetirerUneMenace(effect: 'Effect', joueur: 'Player', source: 'CardFace', menaces: int) -> None:
    """« Remove N threat from a scheme » : le joueur choisit la manigance (modele `rc002`)."""
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            f"Remove {menaces} threat from a scheme",
            lambda cibles:
                source.RemoveThreatFromSchemes(cibles, menaces, effect),
        ).SetTarget(Scheme2),
    )


def SoignerUnAmi(effect: 'Effect', joueur: 'Player', source: 'CardFace', degats: int) -> None:
    """« heal N damage from a friendly character » (modele `01080` First Aid : cible `Friend`)."""
    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility(
            f"Heal {degats} damage from a friendly character",
            lambda cibles:
                source.HealthUnits(cibles, degats, effect),
        ).SetTarget(Friend, canbe_heal=True),
    )


# --- Empathetic Advantage (mt001a) : la limite « once per round » est COMPTEE a la main -----------------------------------------------------------------
# Une identite ne porte qu une capacite de ressource ; `LimitOncePerRound` ne se relance pas (Madonna). Le compteur de
# round du joueur (`world.stat.AddRoundCounter`, remis a zero en fin de round). The Celestial Madonna (mt010) a ses PROPRES moyens de paiement qui ne l'incrementent pas.
CLE_EMPATHETIC_ADVANTAGE = "mt_empathetic_advantage"


def EmpatheticAdvantageDisponible(effect: 'Effect') -> bool:
    joueur = effect.GetInitiator()
    return joueur is not None and effect.world.stat.GetRoundCounter(joueur, CLE_EMPATHETIC_ADVANTAGE) == 0


def PersonnagesConfusDuJoueur(joueur: 'Player') -> List['CardFace']:
    """« a character you control » portant le statut Desoriente (identite et allies)."""
    return [f for f in joueur.GetControlCharacters() if f.IsConfused()]


def EnnemisConfus(effect: 'Effect') -> List['CardFace']:
    """« an enemy » portant le statut Desoriente (vilain et sbires en jeu)."""
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsConfused()]


def DefausserUnConfus(effect: 'Effect', candidats: List['CardFace'], compter: bool=True) -> bool:
    """Cout d'Empathetic Advantage : le joueur CHOISIT la carte, un statut Desoriente en est defausse, et l'emploi est compte pour le round
    (`compter=False` pour The Celestial Madonna : « this use does not count against that ability's limit »).

    Faux (paiement abandonne) si rien n'a pu etre defausse. Modele `hc001a` Empowered : `CostFunc.Custom(None, fn)` + `AskChooseFaces`."""
    joueur = effect.GetInitiator()
    if joueur is None or not candidats:
        return False
    choisies = joueur.AskChooseFaces(candidats, (1, 1), effect, prompt="Empathetic Advantage : discard a confused status card")
    if not choisies:
        return False
    if choisies[0].DiscardConfused(effect, rule=1) <= 0:
        return False
    if compter:
        effect.world.stat.AddRoundCounter(joueur, CLE_EMPATHETIC_ADVANTAGE)
    return True


def ReserveConfus(ability: 'Ability', origine: str) -> 'Ability':
    """Annonce au moteur la reserve de cartes Desorientees que ce moyen de paiement consomme (voir `PlayerAction.SpendResource`) : Empathetic Advantage
    et The Celestial Madonna se partagent la MEME reserve par origine (« enemy » ou « character »), et ne peuvent pas payer ensemble s'il n'en reste qu'une."""
    if origine == "enemy":
        fn = lambda effet: EnnemisConfus(effet)
    else:
        fn = lambda effet: PersonnagesConfusDuJoueur(effet.GetInitiator()) if effet.GetInitiator() is not None else []
    ability.reserve_partagee = ("mt_confus_" + origine, fn)
    return ability
