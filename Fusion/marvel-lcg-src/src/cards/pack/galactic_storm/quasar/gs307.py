from . import *

# Righteous Fury — evenement signature (QUASAR 7/16 et 8/16, x2). ATTACK.
# Cout 3, [energy].
# Hero Action (attack): Deal 6 damage to an enemy. If this attack defeats that
#   enemy, ready Quasar.
#
# Cartes de reference :
#  - **`ag006`** Takedown / `th009` : `this.DealDamage(cibles, n, effect,
#    if_this_attack_defeats=fn)` (RECETTES §2, `fn` appele PAR unite vaincue).
#  - `05015` Tackle pour le montage `Hero Action (attack)` + `SetTarget(Enemy)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « If THIS ATTACK DEFEATS that enemy » : vaincu par ces 6 degats, pas
#    seulement endommage (`defeated` ≠ `damaged`, piege 45160).
#  - « ready **Quasar** » : l'identite du joueur, en forme heros (la carte ne
#    se joue qu'en forme heros : Hero Action).


def GetAbilities() -> Sequence['Ability']:

    def colere(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()

        def vaincu(unite: 'Unit2') -> None:
            Unused(unite)
            Faces.ReadyAll([joueur.GetIdentity()], effect)

        this.DealDamage(effect.targets, 6, effect, if_this_attack_defeats=vaincu)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            colere,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
