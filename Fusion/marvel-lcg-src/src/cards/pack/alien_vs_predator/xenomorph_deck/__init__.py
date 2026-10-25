from cards.pack import *
from cards.pack.alien_vs_predator.commun import *

# Helpers du set « Xenomorph Deck » (ap101-ap104 : Alien Scout, 4 versions x 4 exemplaires). Le deck est glisse sous Alien Queen a la
# mise en place (ap005a) ; la Reine en melange une carte dans le deck du joueur qu'elle blesse (ap001a).


def CapacitesScout(pioche: bool) -> List['Ability']:
    """Commun aux 4 versions :
    « Forced Interrupt: When you would draw or discard this card from your deck, [draw 1 card.] Deal this card to yourself as a facedown
    encounter card. » + « When Defeated: Place Alien Scout in your discard pile. »

    Modele 27087b Maze of Mirrors (`WhenPlayerWouldDrawCard` + `WhenCardWouldDiscard(from_player_deck=True)`, `SetBeInstead`,
    `DealEncounterCard`, `DrawUp(1)`), porte ici par la carte ELLE-MEME, qui vit dans le deck du joueur : `NoOutOfPlayLimit()` et
    `NoGameAreaLimit()` (comme `ThisGainIncite`) la rendent active hors jeu.
    La carte est distribuee AVANT la pioche de remplacement : piocher d'abord reprendrait la meme carte du dessus (meme ordre que 27087b ;
    le resultat imprime est identique). Un Scout atteint par une defausse le signale sur l'effet qui defausse
    (`_ap_scouts_interceptes`) : Alien Onslaught le compte (arbitrage 4 du 25/10/2026)."""
    def intercepter(effect: 'Effect', message: 'Message.WhenPlayerWouldDrawCard|Message.WhenCardWouldDiscard') -> None:
        this = effect.this
        joueur = this.card.area.GetOwner()
        if not Player.IsType(joueur):
            return
        message.SetBeInstead(effect)
        cause = getattr(message, "by_effect", None)
        if cause is not None and isinstance(message, Message.WhenCardWouldDiscard):
            cause._ap_scouts_interceptes = getattr(cause, "_ap_scouts_interceptes", 0) + 1
        joueur.DealEncounterCard(this, effect)
        if pioche:
            joueur.DrawUp(1, effect)

    def dans_le_deck_du_joueur(effect: 'Effect', message: 'Message.WhenPlayerWouldDrawCard') -> bool:
        return message.trigger is effect.this and message.trigger.card.area.flags.is_player_deck

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this
        joueur = JoueurDeLaScout(this, message, effect)
        effect.world._ap_scout_vers_defausse = (this.card, joueur)

    def apres_defaite(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Unused(message)
        en_attente = getattr(effect.world, "_ap_scout_vers_defausse", None)
        if not en_attente or en_attente[0] is not effect.this.card:
            return
        effect.world._ap_scout_vers_defausse = None
        carte, joueur = en_attente
        if carte.area.flags.is_attach_boost_area or carte.area is joueur.discard_pile:
            return
        Faces.MoveAllTo([carte.face], joueur.discard_pile, effect)

    return [
        AbilityFactory.WhenPlayerWouldDrawCard(AbilityType.ForcedInterrupt, "AnyPlayer", "This", intercepter,
                                               conditions=[dans_le_deck_du_joueur]).NoOutOfPlayLimit().NoGameAreaLimit(),
        AbilityFactory.WhenCardWouldDiscard(AbilityType.ForcedInterrupt, "This", intercepter,
                                            from_player_deck=True).NoOutOfPlayLimit().NoGameAreaLimit(),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.AfterUnitBeDefeated(AbilityType.NonKeyword, "This", apres_defaite).NoOutOfPlayLimit().NoGameAreaLimit(),
    ]


def JoueurDeLaScout(face: 'CardFace', message: 'Message.WhenUnitBeDefeated', effect: 'Effect') -> 'Player':
    """« your discard pile » : le joueur engage avec l'Alien Scout (c'est lui qui l'a recue), sinon celui qui l'a vaincue."""
    try:
        engage = face.CastTo(Minion).GetEngagedPlayer()
    except Exception:
        engage = None
    if Player.IsType(engage):
        return engage
    return JoueurQuiVainc(message, effect, face)
