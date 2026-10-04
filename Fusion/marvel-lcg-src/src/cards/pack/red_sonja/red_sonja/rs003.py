from . import *

# Savage Steel — evenement signature, x2 (2-3/15). ATTACK. Cout 3, ressource
# [R].
# Hero Action (attack): Deal 6 damage to an enemy. For each point of excess
# damage dealt by this attack, reduce the cost of the next event you play
# this phase by 1.
#
# CARTES DE REFERENCE
#  - `ar005` Ares' Battle Helm : « excess damage » = `AfterUnitDefeatedUnit
#    (is_from_attack=True, has_excess_damage=True)`, `message.excess_damage`.
#    Encapsule dans `DegatsExcedentairesDeCetteAttaque` (`__init__.py` de ce
#    dossier) pour ne pas dependre d'une amelioration/allie permanent.
#  - `dz003` "A Little Girl's Dream" : `Worlds.UpdateNextCardPlayCost(joueur,
#    -N, effect, finder=CardFinder(card_type=Event), in_this="Phase")` pour
#    « reduce the cost of the next event you play this phase by N ».
#
# TEXTE CONTRE CODE
#  ⚠ « For each point of EXCESS damage » : seulement si l'ennemi est VAINCU
#    par cette attaque, jamais un simple degat encaisse (definition
#    officielle de l'exces).
#  ⚠ « the next event you play THIS PHASE » : `in_this="Phase"`, pas
#    "Turn"/"Round".
#  ⚠ Nombre variable ("for each point") : `Worlds.UpdateNextCardPlayCost`
#    prend une valeur fixe -- appele avec `-exces`, pas `-1` repete.

def GetAbilities() -> Sequence['Ability']:

    def savage_steel(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if not isinstance(joueur, Player):
            return

        exces = DegatsExcedentairesDeCetteAttaque(effect, effect.targets, 6)
        if exces > 0:
            Worlds.UpdateNextCardPlayCost(
                joueur, -exces, effect,
                finder=CardFinder(card_type=Event),
                in_this="Phase",
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            savage_steel,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
