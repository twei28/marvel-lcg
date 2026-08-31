from . import *

# Death's Embrace — attachement nemesis. SPELL. Boost 1 + etoile. x2
# Attach to your identity.
# Each card you play costs 1 additional resource.
# Hero Action: Exhaust your hero or spend [mental][energy][physical] ->
#   discard this card.
# [star] Boost: If this activation is a scheme, attach this card to the
#   first player.
#
# Cartes de reference (RECETTES) :
#  - 15026 Magical Suspension (nemesis OFFICIELLE de Scarlet Witch — le
#    clin d'oeil est sans doute voulu), quasi jumelle :
#    `AttachToFaceWhenPutIntoPlay("YourIdentity")` +
#    `EachCardYouPlayCostAdditionalResource(None, +1)` +
#    `PlayerActionToDiscardThis` ;
#  - « or spend ... » : DEUX actions de sortie (montage wd005), l'une paie
#    en epuisant le heros, l'autre en ressources B+Y+R ;
#  - le boost : an014 Disir — une carte de boost est rangee par le moteur
#    APRES son effet, on DETOURNE le rangement a venir
#    (`WhenCardWouldDiscard` temporaire) vers la mise en jeu chez le premier
#    joueur ; `during_scheme=True` porte le « if this activation is a
#    scheme » (boost.py:9).

def GetAbilities() -> Sequence['Ability']:

    def accrocher_au_premier_joueur(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        def rediriger(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            premier = Worlds.GetFirstPlayer(effet_temp)
            if premier is not None:
                this.PutIntoPlay(premier, effet_temp)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                rediriger,
            ),
            unregister_after_exec=True,
            until_turn_end=True,
        )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.EachCardYouPlayCostAdditionalResource(
            None,
            +1
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Exhaust("YourHero")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("BYR")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            accrocher_au_premier_joueur,
            during_scheme=True,
        ),
    ]
