from . import *

# Straight Cross — EVENEMENT 3 [energy], Taijutsu (TMNT Shinobi, Inkwire). ATTACK.
# Hero Action (attack): Deal 5 damage to an enemy. If you paid for this card with an ATTACK event, stun that enemy.
#
# Mots-cles : aucun (Stunned est un statut officiel, classe Taijutsu : shinobi.md).
#
# Cartes de reference : `jennika/tj004` Decisive Strike, MEME structure a un chiffre pres (3 degats -> 5) : degats puis
#   `Faces.GiveStatus(..., "Stunned", effect)` conditionne par `PayeAvecUnEvenement(effect, "ATTACK")`
#   (`RECETTES-MOTEUR` §13) ; `05015` Tackle pour la forme `Hero Action (attack)` + `SetTarget(Enemy)`.
#
# TEXTE CONTRE CODE
#  ⚠ « paid ... with an ATTACK EVENT » : un autre evenement ATTACK defausse comme ressource.
#  ⚠ « Deal 5 damage » PUIS « stun THAT enemy » : meme ennemi, apres les degats (un ennemi vaincu n'est plus
#    etourdi) ; obligatoire (pas de « may »).


def GetAbilities() -> Sequence['Ability']:

    def straight_cross(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 5, effect)
        if PayeAvecUnEvenement(effect, "ATTACK"):
            Faces.GiveStatus([e for e in effect.targets if not e.IsDefeated()], "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            straight_cross,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
