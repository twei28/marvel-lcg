from . import *

# Decisive Strike — evenement signature, x2. ATTACK. Cout 2, [physical].
# Classe : Jennika ET Taijutsu (desc.Class = « Hero;Taijutsu »).
# Hero Action (attack): Deal 3 damage to an enemy. If you paid for this card with
#   an ATTACK event, stun that enemy.
#
# Cartes de reference :
#  - `05015` Tackle : `Hero Action (attack)` + `SetTarget(Enemy)`, degats puis
#    statut, condition sur le paiement ;
#  - `tl003` Uke Nagashi / `tl006` : « if you paid for this card with ... » lit
#    le paiement (ici des RESSOURCES : `GetPaidResources().HasColor`).
#    Ce texte-ci parle de CARTES (un EVENEMENT ATTACK defausse comme ressource) :
#    on lit les effets de ressource du paiement, `context.paid_this_res_effects`
#    (effect_context.py), dont `.this` est la carte qui a paye.
#
# ⚠ Mots-pieges :
#  - « paid for this card WITH AN ATTACK EVENT » : un evenement portant le trait
#    ATTACK, defausse de la main pour sa ressource ; Decisive Strike est elle-meme
#    un ATTACK, donc une AUTRE copie paie ; une carte d'un autre type ou d'un autre
#    trait ne compte pas ;
#  - « deal 3 damage » PUIS « stun THAT enemy » : le meme ennemi, apres les
#    degats (un ennemi vaincu n'est plus etourdi) ;
#  - libelle `(attack)`.


def GetAbilities() -> Sequence['Ability']:

    def decisive_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 3, effect)

        payee_par_un_attack = any(
            Event.IsType(e.this) and e.this.HasTrait("ATTACK") and e.this != this
            for e in effect.context.paid_this_res_effects
        )
        if payee_par_un_attack:
            Faces.GiveStatus([e for e in effect.targets if not e.IsDefeated()], "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            decisive_strike,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
