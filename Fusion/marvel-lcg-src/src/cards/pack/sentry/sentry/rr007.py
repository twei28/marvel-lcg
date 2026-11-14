from . import *

# Molecularkinesis : AMELIORATION (SKILL. SPLIT. SUPERPOWER.), cout 2, [wild]. Classe Hero. (TEXTE MIS A JOUR le 03/11/2026 : l'ancien Response/Hero Action est abandonne.)
# Hero Interrupt: When an encounter card is revealed, cancel all of its effects and discard it. Then, discard this card and draw 1 card for each balance counter on Duality Aspect.
# Special: Discard 1 card from your deck and the encounter deck for each balance counter in play.
#
# CARTES DE REFERENCE
#  - « When an encounter card is revealed, cancel all of its effects and discard it » : `bkw/08008` (Grappling Hook) : `WhenPlayerRevealCard(HeroInterrupt, "You", type, "All", op)` + `message.CancelAllEffectsAndDiscardIt(effect)` ;
#    « discard this card » en COUT : `CostFunc.Discard("This")`. Fiche `docs/reference/mots-cles/cancel.md` si elle existe (annuler = les effets ne se resolvent pas).
#  - « draw 1 card for each » : `joueur.DrawUp(n, effect)`. Special : `joueur.DiscardDeckTopCards(n, effect)` + `Worlds.DiscardEncounterCards(n, effect)` ; `.NoOutOfPlayLimit()` (resolu depuis la defausse par le Void).
#
# TEXTE CONTRE CODE
#  « an ENCOUNTER card » : toute carte rencontre revelee (traitrise, sbire, complot annexe...) ; « cancel ALL of its effects and DISCARD it » : tous ses effets (When Revealed compris) sont annules et la carte est defaussee. « Then, discard THIS card » : paye en COUT (la carte
#  quitte le jeu avant la resolution : meme resultat). « for each balance counter on DUALITY ASPECT » (Interruption : Duality seule) ; Special : « IN PLAY » (somme de toutes les cartes). Chiffres : cout 2.


def GetAbilities() -> Sequence['Ability']:

    def annuler(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        joueur = JoueurDeCetteCarte(effect)
        n = EquilibreSurDualite(effect)
        message.CancelAllEffectsAndDiscardIt(effect)
        if joueur is not None and n > 0:
            joueur.DrawUp(n, effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect) or JoueurSentry(effect)
        n = EquilibreEnJeu(effect)
        if joueur is None or n <= 0:
            return
        joueur.DiscardDeckTopCards(n, effect)
        Worlds.DiscardEncounterCards(n, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "You",
            None,
            "All",
            annuler,
        ).SetCostFunc(CostFunc.Discard("This")),
        AbilityFactory.WhenResolveSpecialAbility("This", special).NoOutOfPlayLimit(),
    ]
