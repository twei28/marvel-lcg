from cards.pack import *

# ===========================================================================
# Scenario SKRULL EMPIRE (Skrull Menace, Kajislav) — helpers partages.
#
# Regles propres (livret p. 8, « Emperors and Empresses ») :
#  - Un PAQUET MECHANT par stade, quatre mechants differents, dans un ordre
#    IMPOSE : Emperor Dorrek I au-dessus, puis Emperor Dorrek VII, Empress
#    R'Klll, et Empress S'Byll en dessous. Le mechant courant est la carte
#    revelee ; les autres attendent dans `scenario.villain_deck`. Les stades
#    suivants attendent dans la zone mise de cote (scenario json `set_aside`).
#  - Les mechants N'ONT PAS DE PV (desc HP « INF ») : l'environnement Skrull
#    Empire du stade porte le cadran (14 / 18 / 22 par joueur). Tout degat au
#    mechant va sur l'environnement, en compteurs 'damage' (precedent 21100a
#    Avengers Tower) ; le cadran est publie par `Environment.cadran_pv`
#    (environment.py, 15/10/2026).
#  - Environnement a 0 PV : lui et TOUS les mechants de son stade sont retires
#    de la partie ; on revele l'environnement et le premier mechant du stade
#    suivant, et les Overthrow mis de cote retournent dans le deck rencontre
#    (When Revealed des environnements II et III). Plus de stade : les joueurs
#    gagnent.
#  - Quand un mechant quitte la table (Overthrow, ou fin de stade), ses
#    attachements, statuts et autres elements partent avec lui ; seules les
#    cartes boost restent.
# ===========================================================================

ORDRE_MECHANTS = ("Emperor Dorrek I", "Emperor Dorrek VII", "Empress R'Klll", "Empress S'Byll")
NOM_ENVIRONNEMENT = "Skrull Empire"
PV_PAR_JOUEUR = {1: 14, 2: 18, 3: 22}
# ⚠ La classe Environment n'a PAS d'attribut Stage (pas de HasStage) : un
# « Stage » dans le desc d'un environnement fait tomber la creation de la
# partie. Le stade de l'environnement se lit donc sur son card_id.
STADE_ENVIRONNEMENT = {"sk086": 1, "sk087": 2, "sk088": 3}


def StadeEnv(env: 'CardFace') -> int:
    return STADE_ENVIRONNEMENT.get(env.paper.card_id, 0)


def _rang(face: 'CardFace') -> int:
    for i, nom in enumerate(ORDRE_MECHANTS):
        if face.IsName(nom):
            return i
    return len(ORDRE_MECHANTS)


def MechantsMisDeCote(effect: 'Effect', stade: int) -> List['CardFace']:
    """Les quatre mechants d'un stade encore mis de cote, dans l'ordre du livret."""
    faces = [f for f in Worlds.AsideDeck(effect).Get(True)
             if Villain.IsType(f) and f.printed_stage == stade]
    return sorted(faces, key=_rang)


def EnvironnementMisDeCote(effect: 'Effect', stade: int) -> 'CardFace|None':
    for f in Worlds.AsideDeck(effect).Get(True):
        if Environment.IsType(f) and f.IsName(NOM_ENVIRONNEMENT) and StadeEnv(f) == stade:
            return f
    return None


def EnvironnementEnJeu(effect: 'Effect') -> 'Environment|None':
    for f in Worlds.GetOnFieldCards(effect):
        if Environment.IsType(f) and f.IsName(NOM_ENVIRONNEMENT) and f.IsInPlay():
            return f.CastTo(Environment)
    return None


def PremierStade(effect: 'Effect') -> int:
    """1 en mode normal, 2 en expert : le plus petit stade mis de cote."""
    stades = [StadeEnv(f) for f in Worlds.AsideDeck(effect).Get(True)
              if Environment.IsType(f) and f.IsName(NOM_ENVIRONNEMENT)]
    return min(stades) if stades else 1


def PvMax(env: 'CardFace') -> int:
    return PV_PAR_JOUEUR.get(StadeEnv(env), 14) * env.card.world.GetPlayerNumIcon()


def ArmerCadran(env: 'CardFace') -> None:
    """Publie le cadran de PV de l'environnement (pastille et jauge du plateau)."""
    def cadran():
        maximum = PvMax(env)
        return max(0, maximum - env.GetCounters('damage')), maximum
    env.CastTo(Environment).cadran_pv = cadran


def InstallerMechants(effect: 'Effect', stade: int) -> 'CardFace|None':
    """Revele le premier mechant du stade, empile les trois autres dans
    `villain_deck`. ⚠ Le DESSUS d'un deck est sa derniere carte (Deck.GetTop) :
    on empile donc S'Byll, puis R'Klll, puis Dorrek VII."""
    mechants = MechantsMisDeCote(effect, stade)
    if not mechants:
        return None
    premier, reste = mechants[0], mechants[1:]
    premier.Reveal(None, effect)
    paquet = Worlds.GetScenario(effect).villain_deck
    for face in reversed(reste):
        Faces.MoveAllTo([face], paquet, effect)
    return premier


def NettoyerMechant(effect: 'Effect', mechant: 'CardFace') -> None:
    """Defausse attachements et statuts du mechant qui s'en va (livret p. 8)."""
    attaches = list(mechant.GetAttachedAttachments()) + list(mechant.GetAttachedUpgrades())
    if attaches:
        Faces.DiscardAll(attaches, effect)


def MechantCourant(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindVillain(effect)


def RemplacerMechant(effect: 'Effect') -> bool:
    """Overthrow : le mechant courant quitte la partie, le suivant est revele.
    On REVELE le suivant AVANT de retirer l'ancien, pour qu'il y ait toujours
    un mechant en jeu pendant l'effet (sinon FindVillain rend None)."""
    ancien = MechantCourant(effect)
    paquet = Worlds.GetScenario(effect).villain_deck
    suivant = paquet.GetTop()
    if suivant is None:
        return False
    suivant.Reveal(None, effect)
    if ancien is not None and ancien.IsInPlay():
        NettoyerMechant(effect, ancien)
        Faces.RemoveAllFromGame([ancien], effect)
    return True


def FinDeStade(effect: 'Effect', env: 'CardFace') -> None:
    """L'environnement est tombe a 0 PV : fin du stade (livret p. 8)."""
    stade = StadeEnv(env)
    mechant = MechantCourant(effect)
    if mechant is not None:
        NettoyerMechant(effect, mechant)
    restants = list(Worlds.GetScenario(effect).villain_deck.Get(True))
    a_retirer = [f for f in [env, mechant] + restants if f is not None]

    suivant_env = EnvironnementMisDeCote(effect, stade + 1)
    if suivant_env is None:
        # Plus de stade : le dernier environnement est vaincu, les joueurs gagnent.
        effect.world.game_over.SetGameOverByRule("The Final Stage of the Villain was Defeated")
        return
    # ⚠ Ici on RETIRE D'ABORD, puis on installe : le premier mechant du stade
    # suivant porte souvent le MEME NOM unique que celui qui part (« * Emperor
    # Dorrek I » stade I -> stade II). Revele pendant que l'ancien est encore
    # en jeu, la regle d'unicite le defaussait aussitot (constate le 15/10/2026
    # par la sonde : sk071 fini dans la defausse rencontre, aucun mechant en
    # jeu). L'inverse de RemplacerMechant, ou les deux noms different toujours.
    Faces.RemoveAllFromGame(a_retirer, effect)
    InstallerMechants(effect, stade + 1)
    suivant_env.Reveal(Worlds.GetFirstPlayer(effect), effect)


def SoignerLeMechant(effect: 'Effect', source: 'CardFace', valeur: int) -> int:
    """« Heal X damage from the villain » : le mechant n'a pas de PV, c'est
    l'environnement qu'on soigne. Rend le nombre de degats reellement soignes
    (Long Live the Empire en a besoin pour son « if no damage was healed »)."""
    env = EnvironnementEnJeu(effect)
    if env is None or valeur <= 0:
        return 0
    soignes = min(valeur, env.GetCounters('damage'))
    if soignes:
        Faces.RemoveCountersOn([env], soignes, 'damage', effect)
    return soignes


def EnnemisSkrull(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait("SKRULL")]


def SbiresSkrull(effect: 'Effect') -> List['CardFace']:
    return [f for f in EnnemisSkrull(effect) if Minion.IsType(f)]


def PlanetesEnJeu(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Environment.IsType(f) and f.IsInPlay() and f.HasTrait("PLANET")]


def PaquetPlanete(effect: 'Effect') -> 'SetAsideDeck':
    return Worlds.ScenarioDeck(effect, "PlanetDeck")


def CreerPaquetPlanete(effect: 'Effect') -> None:
    """Le paquet PLANET : les 9 environnements PLANET mis de cote, melanges,
    faces cachees (precedent CreerPaquetsPiege, pack hunting_season)."""
    mechant = MechantCourant(effect)
    assert mechant, "le paquet PLANET se cree apres la revelation du premier mechant"
    paquet = PaquetPlanete(effect)
    paquet.Create(effect, mechant, type=DeckType.AdditionalDeck, has_discard_pile=False)
    faces = [f for f in Worlds.AsideDeck(effect).Get(True) if f.HasTrait("PLANET")]
    Faces.ShuffleAllTo(faces, paquet.deck, effect)


def RevelerPlanete(effect: 'Effect') -> 'CardFace|None':
    """« Reveal the top card of the PLANET deck. » Paquet vide : rien."""
    paquet = PaquetPlanete(effect)
    if not paquet.initialize:
        return None
    face = paquet.GetTopCard()
    if face is None:
        return None
    face.Reveal(Worlds.GetFirstPlayer(effect), effect)
    return face


def SbireSkrullDuDeckRencontre(effect: 'Effect') -> 'CardFace|None':
    """« Discard cards from the encounter deck until a SKRULL minion is
    discarded » (complots 2A/3A/4A, A New Skrull Is Born)."""
    return Worlds.DiscardEncounterCardsUntil(effect, trait="SKRULL", card_type=Minion)


def EnvironnementAbilities(avec_overthrow: bool) -> List['Ability']:
    """Les capacites communes aux trois stades de l'environnement Skrull Empire."""

    def armer(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        ArmerCadran(effect.this)

    def rediriger(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        # Les mechants n'ont pas de PV : leurs degats vont sur l'environnement.
        # Modele 39031 Undercover Mojo : SetBeInstead, puis le montant qui
        # aurait ete subi (`will_take_damage`, apres les preventions dont
        # Tough/Toughness).
        this = effect.this
        montant = message.will_take_damage
        message.SetBeInstead(effect)
        if montant > 0 and this.IsInPlay():
            Faces.PlaceCountersOn([this], montant, 'damage', effect)

    def tomber(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this
        Unused(message)
        if getattr(this, "skrull_empire_tombe", False):
            return
        this.skrull_empire_tombe = True
        # Immediat, meme au milieu d'une attaque : 11001 Kang se retire lui
        # aussi de la partie au moment exact de sa defaite (When Defeated),
        # donc en pleine resolution. Seule l'avance du complot y est differee,
        # ce qui ne nous concerne pas.
        FinDeStade(effect, this)

    def renverser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        faces = [f for f in Worlds.AsideDeck(effect).Get(True) if f.IsName("Overthrow")]
        if faces:
            Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    def rebellion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        cibles = list(effect.targets)
        for planete in cibles:
            planete.TreatAsIfBlankInternal(1, effect)

            def retablir(p=planete):
                if p.is_treat_as_if_blank:
                    p.TreatAsIfBlankInternal(-1, effect)
            RunAt.RoundEnd(effect, retablir)

    def cout_rebellion(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        # Modele 16073b The Grand Collection : MEME phrase de cout.
        initiateur = effect.GetInitiator()
        return initiateur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your hero",
                lambda cibles: Faces.ExhaustAll(cibles, effect),
            ).SetTarget("YourHero", canbe_exhaust=True),
            AbilityFactory.ForChoiceAbilityWithCost(Cost("2")),
        ) != []

    abilities = [
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", armer),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, rediriger),
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.ForcedResponse, "This", "damage", tomber,
            at_least=lambda effect: PvMax(effect.this),
        ),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, rebellion)
        .SetName("Incite Rebellion")
        .SetCostFunc(CostFunc.Custom(None, cout_rebellion))
        .SetTarget(Environment, trait="PLANET")
        .LimitOncePerRoundPerPlayer(),
    ]
    if avec_overthrow:
        abilities.append(AbilityFactory.WhenThisRevealed(None, renverser))
    return abilities
