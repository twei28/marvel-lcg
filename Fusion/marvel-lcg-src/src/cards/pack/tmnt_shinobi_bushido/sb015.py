from . import *

# Oathbreaker — EVENEMENT TACTIC, classe Bushido (Inkwire, TMNT Shinobi). Cout 0, [energy].
# Hero Interrupt: When an encounter card is revealed from the encounter deck, discard an OATH upgrade you control -> cancel all of
#   that encounter card's effects and discard it.
# « I will do what I must to save them all... » —Leonardo
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md) pour le trait OATH.
#
# Cartes de reference :
#  - « When an encounter card is revealed from the encounter deck, cancel all of its effects and discard it » :
#    `scw/scarlet_witch/15006` Warp Reality (`WhenPlayerRevealCard(HeroInterrupt, "AnyPlayer", EncounterCard, "All", op,
#    from_encounter=True).SetPlay().SetLabel().SetTarget("Trigger")` + `message.CancelAllEffectsAndDiscardIt(effect)`) ;
#  - cout « discard <X you control> » avec selecteur maison : `CostFunc.Discard(Select.From(fn))` ;
#  - « <amelioration> you control » (identite ET allies) : `joueur.GetControlUpgrade(CardFinder(trait=...))`.
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Interrupt » : forme heros seule ; AVANT la resolution de la carte revelee.
#  ⚠ « an encounter card is revealed FROM THE ENCOUNTER DECK » : seulement une carte revelee depuis le deck rencontre (`from_encounter`),
#    celle de n'importe quel joueur.
#  ⚠ « discard AN OATH upgrade YOU control -> » : COUT paye avant l'effet, UNE amelioration OATH sous son controle choisie par le
#    joueur (la defausse d'une carte a compteurs est permise, avec ses compteurs) ; sans OATH la carte n'est pas jouable.
#  ⚠ « cancel ALL of that card's effects AND discard it » : les DEUX (annuler tous les effets, puis la defausser) ; aucune icone de
#    boost a defausser (contrairement a 15006).


def GetAbilities() -> Sequence['Ability']:

    def oaths_sous_controle(effect: 'Effect') -> 'Sequence[CardFace]':
        joueur = effect.GetInitiator()
        if joueur is None:
            return []
        return list(joueur.GetControlUpgrade(CardFinder(trait="OATH")))  # type: ignore

    def oathbreaker(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.CancelAllEffectsAndDiscardIt(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            EncounterCard,
            "All",
            oathbreaker,
            from_encounter=True,
        ).SetPlay().SetLabel()
        .SetTarget("Trigger")
        .SetCostFunc(CostFunc.Discard(Select.From(oaths_sous_controle))),
    ]
