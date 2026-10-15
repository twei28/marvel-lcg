from . import *

# Mole — AMELIORATION, cout 1 [wild]. TITLE.
# Hero Interrupt: When a TREACHERY card is discarded from the top of the encounter
#   deck, exhaust Mole → resolve that card's "When Revealed" ability.
#
# Cartes de reference :
#  - **`43031`** Cybermods / **`27087b`** : `WhenCardWouldDiscard(ForcedInterrupt, ...)`,
#    l'interruption de defausse (message.is_top : la carte etait au-dessus de sa pile).
#  - **`27083`** For Whom the Bell Tolls / **`27070`** : `Faces.ResolveAbility([carte],
#    joueur, AbilityType.WhenRevealed, effect)` = « resolve that card's When Revealed
#    ability » (resout l'effet SEUL, sans le reste de la revelation : ni surge ni
#    incitation, et la carte continue sa defausse).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « discarded FROM THE TOP OF THE ENCOUNTER DECK » : defausse depuis le dessus du deck
#    rencontre (defausse de sommet, « It's a Stinkin' Skrull! » cherche dans le deck : ce
#    n'est PAS le dessus ; Wrath of the Empire, A New Skrull Is Born le sont).
#  - « TREACHERY card » : type Treachery OU trait TREACHERY (decision du 15/10/2026).
#  - « Hero Interrupt » : forme heros seulement, et la carte part quand meme en defausse.
#  - « exhaust Mole » : cout.


def GetAbilities() -> Sequence['Ability']:

    def du_dessus_du_deck_rencontre(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> bool:
        if not message.is_top:
            return False
        zone = message.trigger.card.area
        return any(zone is deck for deck in Worlds.GetEncounterDecks(effect))

    def resoudre(effect: 'Effect', message: 'Message.WhenCardWouldDiscard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.ResolveAbility([message.trigger], effect.GetInitiator(), AbilityType.WhenRevealed, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenCardWouldDiscard(
            AbilityType.HeroInterrupt,
            FinderTraitrise(),
            resoudre,
            conditions=[du_dessus_du_deck_rencontre],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
