from . import *

# Foot Sweep — EVENEMENT 2 [energy], Taijutsu (TMNT Shinobi, Inkwire). THWART.
# Hero Action (thwart): Remove 3 threat from a scheme. Return each ATTACK event to your hand that you used to
#   pay for this card.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « Hero Action (thwart) : remove N threat from a scheme » : `04049` Clear the Area (`WhenInYourPlayTurn(
#    HeroAction, op).SetPlay().SetLabel('thwart').SetTarget(Scheme2)` + `this.RemoveThreatFromSchemes`) ;
#  - « each X event that you used to pay for this card » : `jennika/tj004` Decisive Strike lit
#    `effect.context.paid_this_res_effects` (la carte payee garde la liste des effets de ressource qui l'ont
#    payee, `.this` = la carte depensee) ; ici on en tire la LISTE des evenements ATTACK ;
#  - « return ... to your hand » : `Faces.ReturnToHand([...], joueur, effect)` (`54003` Black Widow).
#
# TEXTE CONTRE CODE
#  ⚠ « EACH ATTACK event ... that you used to pay » : tous les evenements ATTACK depenses pour cette carte, pas un
#    seul ; un evenement d'un autre trait (DEFENSE, THWART) ou une carte d'un autre type NE revient PAS.
#  ⚠ « Return ... to your HAND » : depuis la defausse (la carte depensee y est), pas depuis le jeu.
#  ⚠ « Remove 3 threat from A scheme » : une manigance au choix ; les cartes reviennent meme si la manigance
#    n'avait que 1 menace.
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def foot_sweep(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        if joueur is None:
            return
        en_defausse = joueur.discard_pile.Get()
        a_rendre: List['CardFace'] = []
        for paye in effect.context.paid_this_res_effects:
            carte = paye.this
            if (Event.IsType(carte) and carte != this and carte.HasTrait("ATTACK")
                    and carte in en_defausse and carte not in a_rendre):
                a_rendre.append(carte)
        if a_rendre:
            Faces.ReturnToHand(a_rendre, joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            foot_sweep,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
