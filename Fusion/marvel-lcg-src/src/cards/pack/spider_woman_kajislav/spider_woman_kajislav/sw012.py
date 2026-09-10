from . import *

# * Century — ALLIE d'aspect PROTECTION, cout 4, 3 PV, CTR 1*, ATQ 2*,
# RES [mental]. ALIEN.
# Hero Interrupt: When Century would take less damage from an attack than his
#   remaining hit points, prevent all of that damage.
#
# ⚠⚠ IL SURVIT A TOUT CE QUI NE LE TUE PAS, ET SEULEMENT A CELA. Trois PV, et
# une attaque a 2 ne lui fait RIEN ; une attaque a 3 le tue net. C'est la carte
# la plus contre-intuitive du pack : plus l'ennemi frappe fort, plus elle est
# mauvaise.
#
# CARTES DE REFERENCE
#  - `03005` EM Shield / `bl006` Vampiric Reflexes :
#    `WhenUnitWouldTakeDamage(Interrupt, ..., is_from_attack=True)` +
#    `message.PreventDamage("All", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠⚠ « LESS damage ... THAN his remaining hit points » : strictement moins.
#    3 PV restants et 3 degats -> il encaisse et meurt. 3 PV et 2 degats ->
#    rien. Le temoin de test porte exactement sur cette frontiere.
#  ⚠ « from AN ATTACK » : `is_from_attack=True`. Une traitrise, un degat
#    indirect, un degat consecutif passent.
#  ⚠ On lit `message.will_take_damage` (sender_damage.py:748), c'est-a-dire ce
#    qu'il PRENDRAIT vraiment — apres Resistance et autres reductions — et non
#    l'ATQ brute de l'attaquant.
#  ⚠ `Hero Interrupt` : la capacite ne vaut qu'en forme heros, comme imprime.


def GetAbilities() -> Sequence['Ability']:

    def century(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        if message.will_take_damage < this.CastTo(Unit2).health:
            message.PreventDamage("All", effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "This",
            century,
            is_from_attack=True,
        ),
    ]
