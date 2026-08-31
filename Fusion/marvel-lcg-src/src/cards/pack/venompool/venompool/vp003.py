from . import *

# Talk About Armed Assault — evenement. ATTACK. SUPERPOWER. Cout 2. x3
# Hero Action (attack): Deal 4 damage divided among enemies as you choose
#   (6 damage instead if the True Form upgrade is in play).
#
# Carte de reference : 13006 Wasp Sting (pack wsp). Elle rend « X degats
# repartis » par `SetTarget(Enemy, range=(1, N), repeat_rules="Health")` et
# 1 degat par selection : le joueur choisit N fois une cible, et
# `repeat_rules="Health"` autorise a reprendre la MEME cible tant qu'elle a
# des PV — c'est ce qui permet de mettre les 4 (ou 6) degats sur un seul
# ennemi, comme « as you choose » l'exige.
#
# Wasp Sting fournit aussi le montage a DEUX capacites mutuellement
# exclusives (GIANT / TINY) : `range` est fige a la construction de la
# capacite, on ne peut donc pas le calculer au moment du jeu. Meme montage
# ici, sur la presence de True Form.

def GetAbilities() -> Sequence['Ability']:

    def assaut(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            assaut,
            conditions=[TrueFormAbsent],
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 4), repeat_rules="Health"),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            assaut,
            conditions=[TrueFormInPlay],
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 6), repeat_rules="Health"),
    ]
