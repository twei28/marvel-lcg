from cards.pack import *
SENSE_DECK_IDS = ('60002', '60003', '60004', '60005', '60006')
def SelectSenseTopCard(effect: 'Effect') -> Sequence['CardFace']:
    initiator = effect.GetInitiator()
    face = initiator.additional_deck.GetTop()
    if face:
        return [face]
    return []
def PlaySenseUpgradeFree(player: 'Player', by_effect: 'Effect', *, any_number: bool = False, optional: bool = False) -> None:
    faces = player.additional_deck.Get()
    if not faces:
        return
    def action(targets: Sequence['CardFace']):
        for face in targets:
            face.CastTo(Upgrade).PutIntoPlay(player, by_effect)
    rng = ((0, len(faces)) if any_number else ((0, 1) if optional else (1, 1)))
    player.ChooseAbilities(by_effect, AbilityFactory.ForChoiceAbility('Choose an upgrade from the Sense deck and play it, ignoring its resource cost', action).SetTarget(faces, range=rng, not_move=True, not_shuffle=True))
def RafraichirDessusDeckAnnexe(effect: 'Effect', message: 'Message2') -> None:
    """Vide le cache `is_like_in_hand` des cartes ENCORE dans le deck annexe.

    CORRECTIF (25/09/2026, meme defaut que le signalement n°17 d'Echo,
    21/09/2026). `check_sense_top` (60001a.py) lit `additional_deck.GetTop()` :
    la reponse depend de QUELLE carte est actuellement au sommet, une donnee
    qui change des qu'une carte du deck annexe ENTRE ou SORT, sans que les
    AUTRES cartes du deck ne bougent elles-memes. Or `card.can_state.is_like_in_hand`
    (`card.py`) ne se remet a zero qu'au DEPLACEMENT de la carte elle-meme :
    la carte devenue nouveau dessus restait donc figee sur sa reponse
    precedente (souvent False, puisqu'elle n'etait pas au sommet la derniere
    fois qu'on l'a lue). Mesure et corrige le 25/09/2026
    (`tools/test_capacites.py`, cas « Sense the Top »).

    Les cinq cartes du deck Sense ne vivent QUE dans `additional_deck` ou en
    jeu (jouees) : tout deplacement de l'une d'elles signale donc un
    changement de dessus possible, sans condition supplementaire a verifier.
    """
    joueur = effect.this.GetControlByPlayer()
    if joueur is None:
        return
    for face in joueur.additional_deck.Get():
        if face is not None:
            face.card.can_state.is_like_in_hand = None
