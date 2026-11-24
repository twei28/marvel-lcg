from . import *
# Rogue Heroics (Protection, evenement 2 [physical]). ATTACK. Alliance.
# Hero Action (attack): Exhaust a STARJAMMER character and a GUARDIAN character → deal X damage among enemies in play, where X is the
# combined ATK of the two exhausted characters. Stun each character damaged this way.
#
# Cartes de reference : sy021 Outlaw Justice / 48032 Gunboat Diplomacy (cout `Select.Alliance`, X = ATQ cumulee, repartition LIBRE) ;
# 01083 Mockingbird (`Faces.GiveStatus(.., "Stunned", ..)`).
# « Stun each character damaged THIS WAY » : les ennemis qui ont reellement perdu des PV (une Tenacite qui annule les degats : pas de
# Sonne) ; un ennemi vaincu n'est plus en jeu. Les PV sont releves AVANT/APRES chaque cible.
def GetAbilities() -> Sequence['Ability']:
    def rogue_heroics(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        initiator = effect.GetInitiator()
        x = 0
        for face in effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards:
            if HasAttack.IsType(face):
                x += face.attack
        def repartir(targets: List['CardFace']) -> None:
            avant = {t: t.health for t in set(targets)}
            this.DealDamage(targets, 1, effect)
            blesses = [t for t in avant if t.IsInPlay() and t.health < avant[t]]
            if blesses:
                Faces.GiveStatus(blesses, "Stunned", effect)
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "",
                repartir,
            ).SetLabel('attack')
            .SetTarget(Enemy, range=(0, x), repeat_rules="Health")
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rogue_heroics,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust(Select.Alliance(["STARJAMMER", "GUARDIAN"]))),
    ]
