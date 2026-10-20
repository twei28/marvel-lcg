from . import *

# Holding Tank — ATTACHEMENT (Supreme Intelligence). Attache au mechant par le Setup de 1A (gs198a).
# Uses (7[per_hero] integrity counters). Victory 0.
# Reduce the amount of damage the villain takes from each attack by 2.
# Forced Response: After an enemy takes any amount of damage, remove 1 integrity counter from here.
#
# Cartes de reference :
#  - **`next_evol/40156`** Impervious : `ReduceCharacterTakeDamageBy(Villain, 1, this_attached_unit_only=True,
#    from_each_attack=True)` = « reduce the amount of damage attached villain takes from each attack by 1 ».
#  - **`determination/dt128`** MRVL Network : `AfterUnitTookDamage(..., Enemy, op)` = « after an enemy takes
#    damage » ; **`53029`** (fiche mots-cles/uses.md) : `Faces.RemoveCountersOn([this], 1, '<nom>', effect)`.
#  - Uses : base AUTOMATIQUE (`desc.Uses = "7*,integrity"`, fiche uses.md) : pions poses a l'entree en jeu,
#    sortie de jeu au dernier pion retire, AUCUN code.
#
# ⚠ Mots-pieges : « the VILLAIN » (Holding Tank est attache au mechant ; `this_attached_unit_only`) ; « from
# EACH ATTACK » (pas les degats hors attaque) ; « an ENEMY takes ANY amount of damage » (mechant OU sbire, une
# attaque ou non, un pion par prise de degats ; 0 degat = rien) ; « remove 1 integrity counter from HERE ».
# Victory 0 : le moteur DEFAUSSE une carte Uses vide a Victory 0 (has_uses.py, piege de la fiche uses.md) ;
# sans effet sur la partie (Holding Tank n'est pas un sbire KREE), consigne au gabarit.


def GetAbilities() -> Sequence['Ability']:

    def degats_subis(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        Faces.RemoveCountersOn([this], 1, 'integrity', effect)

    return [
        AbilityFactory.ReduceCharacterTakeDamageBy(
            Villain,
            2,
            this_attached_unit_only=True,
            from_each_attack=True,
        ),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            Enemy,
            degats_subis,
        ),
    ]
