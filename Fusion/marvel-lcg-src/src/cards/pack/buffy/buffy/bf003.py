from . import *

# Slay Time — EVENEMENT (ATTACK), cout 2, [physical]. x2.
# Hero Action (attack): Deal 4 damage to an enemy. For each point of excess damage dealt to that enemy by this attack,
# reduce the resource cost of the next card you play this phase by 1.
#
# CARTES DE REFERENCE
#  - `13013` Into the Fray : `this.DealDamage(effect.targets, 4, effect, if_this_attack_deal_excess_damage=fn)` ; `fn(valeur)` recoit
#    l'EXCES de CETTE attaque (jamais celui d'une autre).
#  - `16169` Sure Gamble : `Worlds.UpdateNextCardPlayCost(joueur, -n, effect, in_this="Phase")` pour « the next card played this phase ».
#
# TEXTE CONTRE CODE
#  « an enemy » -> `Enemy` (vilain ou sbire). « excess damage » -> existe a la DEFAITE seulement (recette 7duodecies) : un
#    ennemi qui survit ne donne aucune reduction.
#  « the next card YOU play » -> le joueur qui joue Slay Time (`GetInitiator`), pas « Any » (Sure Gamble). « this phase » ->
#    `in_this="Phase"`. « by 1 for each point » -> reduction = exces. Chiffres : 4 degats, 1 par point.


def GetAbilities() -> Sequence['Ability']:

    def slay_time(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()

        def reduire_la_prochaine_carte(exces: int) -> None:
            if exces > 0:
                Worlds.UpdateNextCardPlayCost(joueur, -exces, effect, in_this="Phase")

        this.DealDamage(effect.targets, 4, effect, if_this_attack_deal_excess_damage=reduire_la_prochaine_carte)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            slay_time,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
