from . import *

# * Michelangelo's Other Nunchuck — amelioration signature, x1 (15/15).
# NINJA. NUNCHUCK. WEAPON. Cout 1, ressource [energy]. Restricted.
# Each NUNCHUCK upgrade you control gains: "Hero Interrupt: When you would
#   take damage from an attack, exhaust this card -> reduce that damage by 1
#   and deal 1 damage to the attacking enemy."
#
# Regle de l'insert : « You may use either NUNCHUCK (or both) to reduce the
# damage you receive from an attack by 1 and deal 1 damage to that enemy. »
#
# Cartes de reference :
#  - meme montage « gagne une capacite » que tm011 (`50070`) ;
#  - prevenir 1 degat : `luke_cage/62010` Metal Bracer —
#    `WhenUnitWouldTakeDamage(HeroInterrupt, "You", op)` +
#    `message.PreventDamage(1, effect)` + `CostFunc.Exhaust("This")` ;
#  - « from an attack » : parametre `is_from_attack=True` de la fabrique
#    (damage.py:10) ; l'attaquant est `message.source` (sender_damage.py:721).
#
# ⚠ Mots-pieges :
#  - « EACH NUNCHUCK upgrade you control gains » : meme lecture que tm011.
#  - « when YOU would take damage » : l'identite (`"You"`), pas un allie.
#  - « from an ATTACK » : degats d'attaque seulement, pas d'effet de carte.
#  - « the ATTACKING ENEMY » : la source de l'attaque ; elle n'est visee que si
#    c'est un ennemi (`Enemy.IsType`).
#  - PreventDamage(1) retire 1 degat ; s'il y en avait 0 ou 1, rien d'autre
#    n'est reduit mais le 1 degat a l'ennemi part quand meme (cout paye).
#  - Les degats a l'ennemi viennent de CETTE carte (pas une attaque, donc pas
#    de Riposte en retour ; Robuste de l'ennemi s'applique).

def GetAbilities() -> Sequence['Ability']:

    def riposte_au_nunchuck(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)
        attaquant = message.source
        if attaquant is not None and Enemy.IsType(attaquant):
            effect.this.DealDamage([attaquant], 1, effect)

    interruption_donnee = AbilityFactory.WhenUnitWouldTakeDamage(
        AbilityType.HeroInterrupt,
        "You",
        riposte_au_nunchuck,
        is_from_attack=True,
    ).SetCostFunc(CostFunc.Exhaust("This"))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(trait="NUNCHUCK", card_type=Upgrade),
            control_by="You",
            given_abilities=[interruption_donnee],
        ),
    ]
