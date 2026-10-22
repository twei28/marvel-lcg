from cards.pack.shadowland import *
from cards.pack.fne import PeutCouvrirLeCout


def PositionsDifferentes(effect: 'Effect') -> bool:
    """« If the positions are different » : les DEUX cartes sont en jeu et ne montrent pas la meme position."""
    return PositionDuVilain(effect) is not None and PositionDuHeros(effect) is not None and not PositionsIdentiques(effect)


def AbilitesPositionVilain() -> Sequence['Ability']:
    """Effets continus imprimes IDENTIQUEMENT sur les deux faces de sl003 (VILLAIN POSITION)."""

    def degats_moins_un(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return PositionsDifferentes(effect)

    def menace_non_retirable(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        return PositionsDifferentes(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("Character", attack=1, condition=PositionsIdentiques),
        AbilityFactory.ReduceCharacterTakeDamageBy("Character", 1, from_each_attack=True, conditions=[degats_moins_un]),
        AbilityFactory.ThreatCannotBeRemovedFromWhile(MainScheme, conditions=[menace_non_retirable]),
    ]


def ActionPositionHeros(branches: Callable[['Effect', 'Player', Callable[[], None]], Sequence['Ability']]) -> 'Ability':
    """« First Player Action : Resolve one of the effects below, then flip this card » (sl004a/b).
    `branches(effect, joueur, retourner)` rend les trois choix ; chacun appelle `retourner()` une fois SON effet resolu.
    Modeles : gmw/16143 (First Player Action d'un environnement), fne/60127 (choix payants)."""

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        joueur = message.GetToPlayer()

        def retourner() -> None:
            this.card.Flip(effect)

        joueur.ChooseAbilities(effect, *branches(effect, joueur, retourner))

    return AbilityFactory.WhenInYourPlayTurn(AbilityType.FirstPlayerAction, action)


def RechercherUnSbire(effect: 'Effect', joueur: 'Player') -> None:
    """« Searches the encounter deck and discard pile for a minion and reveals it. (Shuffle.) » : le deck ET la defausse de rencontre ; la recherche melange le
    deck ensuite (comportement de `Search.EncounterCard`). Rien si aucun sbire n'y est."""
    sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, card_type=Minion)
    if sbire is not None:
        sbire.Reveal(joueur, effect)


def AbilitesPvExpert() -> Sequence['Ability']:
    """« In expert mode, the villain gets +3[per_hero] hit points. »"""
    return AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
        Villain, health=1, get_new_value=lambda effect, face: 3 * Worlds.GetPlayerNumIcon(effect), expert_mode_only=True)


def AbilitesComplotAvecVilainRetourne(*, plus_sch_expert: bool, plus_pv_expert: bool) -> Sequence['Ability']:
    """Le texte COMMUN des complots sl001b et sl002b : en expert +1 SCH et +3[per_hero] PV ; « When the villain would be defeated on side A, instead flip it to side
    B, reset its hit points, and change the villain's position. Deal each player 1 facedown encounter card. » ; « If the villain is defeated on side B, the players
    win the game. » (UNE SEULE interruption pour les deux faces : deux interruptions separees se declenchent l'une apres l'autre sur le MEME message, et la seconde
    voyait deja la face B retournee par la premiere, donc declarait la victoire des la premiere defaite - constate le 22/10/2026)."""

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        monde = effect.world
        if getattr(monde, 'sl_retournement', False):
            # ⚠ PENDANT notre propre retournement : la face B arrive avec les degats de la face A et le moteur la juge un instant « vaincue » avant que ses PV soient
            # remis (constate le 22/10/2026) ; ce n'est PAS une defaite face B.
            return
        vilain = message.trigger
        face_a = str(vilain.paper.card_id).endswith('a')          # lu AVANT d'agir
        if not face_a:
            # Face B : le vilain est vraiment vaincu ; les joueurs gagnent. Le moteur ne le fait PAS seul : il ne declare la victoire que s'il ne reste AUCUN vilain de
            # cote (`scenario.py`, « The Final Stage of the Villain was Defeated »), or les 5 autres Dark Protege y sont toujours (modele 40104b).
            # ⚠ `IsDefeated` : l'interruption est reevaluee juste apres le retournement de la face A (PV remis, la carte est alors la face B) ; seule une face B
            # a REELLEMENT zero PV est vaincue.
            if vilain.IsDefeated():
                Worlds.SetGameOver(True, effect)
            return
        message.SetBeInstead(effect)
        monde.sl_retournement = True
        try:
            vilain.card.Flip(effect)
            # Les PV sont portes par la CARTE : on remet la face d'arrivee a son maximum APRES le retournement (wd057), sinon elle revient deja vaincue.
            vilain.card.face.CastTo(Villain).ResetHealth(effect)
        finally:
            monde.sl_retournement = False
        ChangerPositionVilain(effect)
        Players.ForEachPlayer(effect, lambda joueur: joueur.DealEncounterCards(1, effect))

    capacites: List['Ability'] = [AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Villain, vaincu)]
    if plus_sch_expert:
        capacites += AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Villain, scheme=1, expert_mode_only=True)
    if plus_pv_expert:
        capacites += AbilitesPvExpert()
    return capacites


def CartesControlees(joueur: 'Player') -> List['CardFace']:
    """« a card you control » en jeu : allies, ameliorations (y compris celles des allies) et soutiens. Ni l'identite ni la main."""
    allies = [c for c in joueur.GetControlCharacters() if Ally.IsType(c)]
    return allies + list(joueur.GetControlUpgrade()) + list(joueur.supports.Get())


def ChangerSiPasChange(effect: 'Effect') -> None:
    """« Change the villain's position if it has not changed this phase. » (9 cartes du set)"""
    ChangerPositionVilain(effect, si_pas_change_cette_phase=True)


def AuTenshu(effect: 'Effect') -> bool:
    """« If the villain's position is Atop the Tenshu » (sinon : The Streets Below). Faux si la carte de position n'est pas en jeu."""
    return PositionDuVilain(effect) == TENSHU
