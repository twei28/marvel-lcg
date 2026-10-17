from . import *

# Double Kick — EVENEMENT 2 [mental], Taijutsu (TMNT Shinobi, Inkwire). ATTACK. THWART.
# Hero Action (attack/thwart): Deal 2 damage to an enemy and remove 2 threat from a scheme. If you paid for this
#   card with:
#   • A DEFENSE event, draw 1 card.
#   • A THWART event, draw 1 card.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « deal N damage to an enemy and remove N threat from a scheme » (deux cibles) : `18004` Crosscounter
#    (`SetTarget2(Enemy)` / `SetTarget3(Scheme2)`), `ma015` Break Through pour le double libelle
#    (`SetLabel('attack', 'thwart')`) ;
#  - « if you paid for this card with a <trait> event » : `jennika/tj004` (`PayeAvecUnEvenement`).
#
# TEXTE CONTRE CODE
#  ⚠ Deux PUCES INDEPENDANTES : une carte payee par un evenement DEFENSE pioche 1 ; payee par un evenement THWART
#    pioche 1 de plus ; une carte (Toss, Countercross) qui porte LES DEUX traits satisfait les DEUX puces
#    (lecture litterale, Q-T3 resolue le 17/10/2026, lecture confirmee). Plusieurs evenements du MEME trait ne repiochent pas :
#    la puce dit « A DEFENSE event », pas « each ».
#  ⚠ « 2 damage » et « 2 threat » : deux effets sans fleche, les deux se resolvent toujours.
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def double_kick(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 2, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 2, effect)

        if joueur is None:
            return
        if PayeAvecUnEvenement(effect, "DEFENSE"):
            joueur.DrawUp(1, effect)
        if PayeAvecUnEvenement(effect, "THWART"):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            double_kick,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
