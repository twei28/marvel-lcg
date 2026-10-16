from . import *

# Brain Burn — EVENEMENT, cout 1, [wild]. SUPERPOWER. THWART. x2.
# Hero Action (thwart): Remove 2 threat from a scheme. You may remove 2 dredge counters
#   from Venus to confuse and stun an enemy.
#
# CARTES DE REFERENCE
#  - `tg003` / `42006` : `SetPlay().SetLabel('thwart').SetTarget(Scheme2)` +
#    `this.RemoveThreatFromSchemes(effect.targets, N, effect)`.
#  - `tr004` Headbutt : « stun / confuse that enemy » par `Faces.GiveStatus`.
#  - `01165` Eviction Notice : choix facultatif a cout (`MayChooseOneAbility` +
#    `ForChoiceAbility(...).SetCostFunc(...)`), helper `ProposerRetraitDragage`.
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY remove 2 dredge counters ... to confuse AND stun AN enemy » : facultatif
#    (bouton Passer), les DEUX statuts sur UN SEUL ennemi, choisi parmi ceux qui peuvent
#    en recevoir au moins un (un ennemi Stalwart n'est pas ciblable).
#  ⚠ Les 2 menaces sont retirees AVANT et independamment du choix.
#  Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def brain_burn(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)
        joueur = JoueurDeCetteCarte(effect)

        def desorienter_et_sonner(cibles: Sequence['CardFace']) -> None:
            vivants = [c for c in cibles if c is not None]
            if vivants:
                Faces.GiveStatus(vivants, "Confused", effect)
                Faces.GiveStatus(vivants, "Stunned", effect)

        ProposerRetraitDragage(
            effect, joueur, 2,
            "Remove 2 dredge counters to confuse and stun an enemy",
            desorienter_et_sonner,
            target=Enemy, canbe_status=["Stunned", "Confused"])

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            brain_burn,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
