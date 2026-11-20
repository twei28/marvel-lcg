from cards.pack import *
from cards.pack.alien_vs_predator.commun import *

# Helpers du set « Alien vs. Predator » (ap001a-ap033). Voir le `__init__.py` du pack pour le scenario.


################################################################################
# Communs aux deux mechants
def ManiganceSurSaManigance(nom: str) -> 'Ability':
    """« [star] When <nom> schemes, place that threat on his/her side scheme instead of the main scheme, if able. »
    Fabrique des Wrecking Crew (`PlaceThreatOnCardWhenThisScheme`, modele 07002) ; « if able » : sans sa manigance en jeu, la
    menace va au complot principal. Advance (ap201) l'ecarte le temps de SA manigance (« Place this threat on the main
    scheme »)."""
    def sa_manigance(effect: 'Effect') -> 'Scheme2|None':
        if getattr(effect.world, '_ap_vers_le_complot', False):
            return None
        return ManiganceDe(effect, nom)

    return AbilityFactory.PlaceThreatOnCardWhenThisScheme(AbilityType.NonKeywordStar, sa_manigance)


def RetourneQuandVaincu() -> 'Ability':
    """« When Defeated: Flip this card. » Le retournement revele la face « Defeated » (son « When Revealed » part, puis elle se
    retire du jeu : `Villain.OnBeDefeated` ne cherche donc pas de stade suivant). SEUL mechant restant : pas de retournement,
    la defaite native fait gagner les joueurs (arbitrage du 25/10/2026, « sa face Defeated ne se joue pas »)."""
    def retourner(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Villain)
        Unused(message)
        this.card.Flip(effect)

    def l_autre_est_en_jeu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        Unused(message)
        return any(v is not effect.this for v in Mechants(effect))

    return AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", retourner, conditions=[l_autre_est_en_jeu])


def AvancerAuStade(effect: 'Effect', stade: int) -> bool:
    """« Advance to stage 3A / 4A » : saute directement a ce stade (le 2 reste dans le deck des complots, sans suite)."""
    complot = LeComplot(effect)
    if complot is None:
        return False
    cible = effect.world.main_schemes_deck.FindCard(CardFinder(stage=stade), card_type=MainScheme)
    if cible is None:
        return False
    effect.world.AdvanceMainScheme(complot, cible, effect)
    return True


def FaceVaincue(soin: int, autre: str, stade: int) -> List['Ability']:
    """Face « Defeated » : « When Revealed: Heal <soin>[per_hero] damage from <autre> and give him/her a tough status card.
    Advance to stage <stade>A. Remove each permanent side scheme and this card from the game. »"""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        Unused(message)
        survivant = MechantNomme(effect, autre)
        if survivant is not None:
            this.HealthUnits([survivant], soin * NombreDeJoueurs(effect), effect)
            Faces.GiveStatus([survivant], "Tough", effect)
            Villains.SetActive(survivant, effect)
        AvancerAuStade(effect, stade)
        a_retirer = ManigancesPermanentes(effect)
        if this.IsInPlay():
            a_retirer.append(this)
        if a_retirer:
            Faces.RemoveAllFromGame(a_retirer, effect)

    return [AbilityFactory.WhenThisRevealed(None, revele)]


################################################################################
# Alien Queen (ap001a standard, ap003a expert)
def CapacitesReine() -> List['Ability']:
    """« [star] Forced Response: After Alien Queen attacks and damages a character you control, shuffle a Xenomorph card into
    your deck. » (fabrique `AfterUnitAttackAndDamageUnit`, modele 27161 Kraven)."""
    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        MelangerUnXenomorph(message.GetToPlayer(), effect)

    return [
        ManiganceSurSaManigance(REINE),
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", "YouControlCharacter", blesse),
        RetourneQuandVaincu(),
    ]


################################################################################
# Predator Warlord (ap002a standard, ap004a expert)
def CapacitesWarlord() -> List['Ability']:
    """« [star] Forced Interrupt: When Predator Warlord attacks, either place 2 threat on the main scheme or he gets +1 ATK for
    this attack. » Le joueur attaque (a defaut le premier joueur) choisit (modele 21092 Proxima Midnight). « attacks » : toute
    attaque, alliee visee comprise (Predator's Prey, Trophy Taken)."""
    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Villain)
        joueur = message.property.against_player if message.property is not None else None
        if not Player.IsType(joueur):
            joueur = Worlds.GetFirstPlayer(effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 2 threat on the main scheme",
                                            lambda targets: this.PlaceThreatOnSchemes("MainScheme", 2, effect)),
            AbilityFactory.ForChoiceAbility("Predator Warlord gets +1 ATK for this attack",
                                            lambda targets: message.GainATKForThisAttack(+1, effect)),
        )

    return [
        ManiganceSurSaManigance(WARLORD),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", attaque),
        RetourneQuandVaincu(),
    ]


################################################################################
# Complots
def PerdQuandAccompli() -> 'Ability':
    """« If this stage is completed, the players lose the game. » (3B, 4B) : sans cela le moteur passerait au complot suivant
    encore dans le deck (le 2 ou l'autre 3/4)."""
    def perdu(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        message.SetBeInstead(effect)
        Worlds.SetGameOver(False, effect)

    return AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.WhenCompleted, "This", perdu)


def StadeDuSurvivant(nom: str, trait: str) -> List['Ability']:
    """3B / 4B : « <nom> is the active villain. When Revealed: Each player searches the encounter deck and discard pile for a
    [[TRAIT]] minion and reveals it. If this stage is completed, the players lose the game. »"""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        survivant = MechantNomme(effect, nom)
        if survivant is not None:
            Villains.SetActive(survivant, effect)
        for joueur in Worlds.GetPlayers(effect):
            if effect.world.is_game_over:
                return
            ChercherEtReveler(effect, joueur, trait)

    return [AbilityFactory.WhenThisRevealed(None, revele), PerdQuandAccompli()]


def StadeQuiFouille(trait: str) -> List['Ability']:
    """3A / 4A : « When Revealed: Discard cards from the top of the encounter deck until a [[TRAIT]] attachment is discarded.
    Reveal it. » (modele 01192 Masterplan, `Worlds.DiscardEncounterCardsUntil`)."""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        DefausserJusquAReveler(effect, JoueurDuMessage(message, effect), trait=trait, card_type=Attachment)

    return [AbilityFactory.WhenThisRevealed(None, revele)]


################################################################################
# Manigances permanentes
def ManiganceSansMenacePerdLIcone() -> 'Ability':
    """« While there is no threat here, this scheme loses the [acceleration] icon. » (modele pd026 : bonus -1 dynamique, l'icone
    REVIENT avec la menace)."""
    def sans_menace(effect: 'Effect', faces: List['CardFace']) -> int:
        Unused(faces)
        return 1 if effect.this.CastTo(EncounterSideScheme).threat == 0 else 0

    return AbilityFactory.ThisGainKeyword(sans_menace, acceleration_icon=-1, change_on_event=OnEvent.Threat("This"))


################################################################################
# Attachements et actions des joueurs
def SbireTrouvable(effect: 'Effect', trait: str) -> bool:
    """Un sbire [[trait]] HORS JEU que « Find » peut atteindre (deck et defausse de rencontre, cartes de cote, decks et defausses des
    joueurs) : condition des actions « Find a X minion and reveal it → discard this card » (sans sbire, le cout ne se paie pas)."""
    tas = list(Worlds.GetEncounterDeckCards(effect)) + list(Worlds.GetEncounterDiscardPileCards(effect)) + \
        list(Worlds.GetSetAsideAreaCards(effect))
    for joueur in Worlds.GetPlayers(effect):
        tas += list(joueur.player_deck.GetAll()) + list(joueur.discard_pile.GetAll())
    return any(Minion.IsType(f) and f.HasTrait(trait) and not f.IsInPlay() for f in tas)


def TrouverEtReveler(effect: 'Effect', joueur: 'Player', trait: str) -> 'CardFace|None':
    """« Find a [[trait]] minion and reveal it » (regle Find du 23/10/2026, `game/operate/find.py`, modele pd008)."""
    sbire = Find.Find(effect, who_perform=joueur,
                      finder=CardFinder(card_type=Minion, trait=trait, check_face_fn=lambda f: not f.IsInPlay()))
    if sbire is not None:
        sbire.Reveal(joueur, effect)
    return sbire


def CibleMarquee(trait: str, action: 'Callable[[Effect, Player], Any]', condition: 'Callable[[Effect], bool]') -> List['Ability']:
    """Thermal Target / Facehugger : « Attach to your identity. Forced Response: After your turn ends, take 2 damage and place 2 threat on
    the main scheme. Alter-Ego Action: <action> → discard this card. » (modele 21029 Sap Power)."""
    def fin_de_tour(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        joueur.GetIdentity().TakeDamage(this, 2, effect)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    def chercher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        action(effect, effect.GetInitiator())

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.AfterPlayerTurnEnd(AbilityType.ForcedResponse, "You", fin_de_tour),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction,
                                                 conditions=[lambda effect, message: condition(effect)],
                                                 ex_operation=chercher),
    ]
