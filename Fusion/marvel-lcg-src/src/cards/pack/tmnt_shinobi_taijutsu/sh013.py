from . import *

# Roll With It — EVENEMENT 0 [mental], Taijutsu (TMNT Shinobi, Inkwire). NYC. TACTIC.
# Hero Response: After your hero defends, ready your hero.
# Hero Interrupt: When you spend this card to pay for an ATTACK event, put a DEFENSE event from your discard pile
#   on top of your deck.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « After your hero defends, ready your hero » : `core/01082` Indomitable (`AfterUnitDefendEnd(..., "YourHero", op)`
#    + `.SetTarget("YourHero", canbe_ready=True)`, `Faces.ReadyAll`) ; version evenement : `core/01077` Counter-Punch
#    (`.SetPlay()`) ;
#  - « When you spend this card to pay for an X event » : `32018` Defensive Energy (`WhenYouSpendThisCardToPlay(
#    HeroInterrupt, op, CardFinder2("DEFENSE", Event))`) ;
#  - « put a card from your discard pile on top of your deck » : `Faces.MoveAllToDeck([face], deck, "Top", effect)`
#    (`bt011`, RECETTES-MOTEUR §2), cible dans `YourDiscardPile` (`54003`).
#
# TEXTE CONTRE CODE
#  ⚠ Deux capacites DISTINCTES sur la meme carte : la Reponse se JOUE depuis la main (`SetPlay`), l'Interruption se
#    declenche quand la carte est DEPENSEE (elle n'est pas « jouee »).
#  ⚠ « After your hero DEFENDS » : apres toute defense du heros (pas seulement contre une attaque d'ennemi) ; « ready
#    your HERO » : le heros, pas l'identite alter-ego ; la Reponse n'est proposee que si le heros est incline.
#  ⚠ « When you spend THIS card to pay for an ATTACK event » : l'evenement paye porte le trait ATTACK ; « a DEFENSE
#    event from YOUR discard pile » : un evenement DEFENSE de votre defausse, pose sur le DESSUS du deck.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            Faces.ReadyAll([joueur.GetHero()], effect)

    def remettre(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Faces.MoveAllToDeck(effect.targets, joueur.player_deck, "Top", effect)

    return [
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "YourHero",
            redresser,
        ).SetPlay().SetLabel()
        .SetTarget("YourHero", canbe_ready=True),
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.HeroInterrupt,
            remettre,
            CardFinder2("ATTACK", Event),
        ).SetTarget(CardFinder2("DEFENSE", Event), from_where=["YourDiscardPile"]),
    ]
