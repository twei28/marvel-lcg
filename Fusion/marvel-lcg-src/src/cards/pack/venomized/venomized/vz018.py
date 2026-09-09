from . import *

# Symbiotic Go All Out — EVENEMENT, cout 2, RES [mental]. ATTACK. SYMBIOTE.
# Requirement ([energy]).
# Hero Action (attack): Exhaust your hero -> deal damage to an enemy equal to
#   the total of your hero's THW, ATK, and DEF values.
#
# CARTE DE REFERENCE
#  - `29017` Go All Out (Meneur, pack ironheart) : MEME TEXTE, meme cout, meme
#    ressource, MEME `Requirement` [energy]. Corps repris tel quel.
#
# TEXTE CONTRE CODE
#  ⚠ « Requirement ([energy]) » ne se code PAS ici : c'est `desc.Requirement`
#    dans `cards.json` (valeur "Y"), lu nativement par le moteur. La rappeler
#    dans le module la ferait payer deux fois.
#  ⚠ « Exhaust your hero » est le COUT, pas l'effet -> `SetCostFunc`, sinon un
#    heros deja incline pourrait jouer la carte.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_go_all_out(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        heros = effect.GetInitiator().GetHero()
        this.DealDamage(effect.targets, heros.thwart + heros.attack + heros.defense, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            symbiotic_go_all_out
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("YourHero"))
        .SetTarget(Enemy),
    ]
