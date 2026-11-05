from . import *

# * Ego The Living Planet — ALLIE. LIVING. PLANET. COSMIC. THW 2, ATK 3, HP 7.
# (17/17). Linked (pc017 Ego, le sbire de meme nom) : mise de cote jusqu'a ce
# que le sbire soit vaincu (pc017.py, « When Defeated »).
#
# Texte imprime :
#  « Linked (Ego). This card does not count against your ally limit. »
#  « At the end of the round, each character here takes damage equal to my
#    ATK, then departs. »
#  « Action: Choose a minion -> that minion arrives here and I take damage
#    equal to that minion's ATK. »
#
# CARTES DE REFERENCE
#  - `AbilityFactory.ThisNotCountAllyLimit()` (friend.py) : « does not count
#    against your ally limit », fabrique dediee, rien a inventer.
#  - helper `PersonnagesÀLaPlanète` (__init__.py du pack, ajoute pour cette
#    carte) : seule carte du pack dont le texte agit sur TOUS les
#    personnages ici a la fois, a un moment qui n'est pas l'arrivee -- pas
#    une liste captee comme `pc016` Black Hole.
#  - `AbilityFactory.WhenRoundEnd` (turn_phase.py) : « At the end of the
#    round » (pas la phase, le ROUND entier).
#  - `ArriverA` : « that minion arrives here ».
#
# TEXTE CONTRE CODE
#  « each character HERE » : lu via `PersonnagesÀLaPlanète(effect, this)`,
#    jamais une liste figee a l'avance.
#  « takes damage equal to MY ATK » : `this.attack` (valeur ACTUELLE au
#    moment de la resolution, pas l'imprimee).
#  « THEN departs » : `Departir` pour chaque personnage, APRES le degat.
#  « I take damage equal to that minion's ATK » : `cible.attack` DU SBIRE
#    CHOISI, pas une valeur fixe.


def GetAbilities() -> Sequence['Ability']:

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        for personnage in PersonnagesÀLaPlanète(effect, this):
            this.DealDamage([personnage], this.attack, effect)
            Departir(effect, personnage)

    def accueillir_sbire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        if not effect.targets:
            return
        sbire = effect.targets[0]
        ArriverA(effect, sbire, this)
        this.DealDamage([this], sbire.CastTo(HasAttack).attack, effect)

    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.WhenRoundEnd(
            AbilityType.ForcedResponse,
            None,
            fin_de_round,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            accueillir_sbire,
        ).SetTarget(Minion)
        .SetName("Accueillir un sbire"),
    ]
