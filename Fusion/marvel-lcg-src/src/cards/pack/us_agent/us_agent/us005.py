from . import *

# Roundhouse — evenement signature, x2 (8/15, 9/15). ATTACK. Cout 1, ressource [physical].
# Hero Action (attack): Deal 2 damage to an enemy. If you paid for this card using a Protection (green) or Justice
# (yellow) card, confuse that enemy.
#
# Cartes de reference :
#  - `jennika/tj004` Decisive Strike : « if you paid for this card with an ATTACK event » = `effect.context.paid_this_res_effects`
#    (les effets de ressource qui ont PAYE ; `e.this` = la carte payeuse). Recette RECETTES §7duovicies.
#  - `01053` Relentless Assault : « if you paid for this card using a [physical] resource » (une COULEUR, ce n'est pas notre cas).
#
# ⚠ Mots-pieges :
#  - « paid using a Protection or Justice CARD » : la CLASSE de la carte payeuse (`desc.Class`), pas la couleur de la ressource ;
#    une carte Basic / Aggression / Leadership / signature ne confond pas. OU entre les deux classes.
#  - « that enemy » : la meme cible que les degats ; elle doit etre encore en vie. La cible n'est PAS filtree par
#    `canbe_confused` : « Deal 2 damage to AN enemy » vise n'importe quel ennemi, la desorientation est un bonus.


def GetAbilities() -> Sequence['Ability']:

    def roundhouse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 2, effect)
        payee_par_protection_ou_justice = any(
            e.this != this and ClassCard.IsType(e.this) and e.this.IsClass("Protection", "Justice")
            for e in effect.context.paid_this_res_effects
        )
        if payee_par_protection_ou_justice:
            Faces.GiveStatus([e for e in effect.targets if not e.IsDefeated()], "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            roundhouse,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
